"""Generate and maintain a changelog from Git commits."""

__version__ = "0.1.7"

import datetime
import re
import subprocess  # noqa: S404
from collections.abc import Generator
from dataclasses import dataclass
from typing import Annotated

import typer

# Regular expressions used to parse the changelog
RE_LINKS = re.compile(r"^\[.+?\]:")
RE_RELEASE = re.compile(r"^## \[(.+?)\](?: - (\d{4}-\d{2}-\d{2}))?$")
RE_SECTION = re.compile(r"^### (.+)$")
RE_REPO_URL = re.compile(r"^(?:git@|https://)([^/:]+)[:/](.+?)/(.+?)\.git$")
RE_PR_NUMBER = re.compile(r"\(#(\d+)\)")

# Changelog categories
CATEGORY_ADDED = "Added"
CATEGORY_CHANGED = "Changed"
CATEGORY_DEPRECATED = "Deprecated"
CATEGORY_FIXED = "Fixed"
CATEGORY_REMOVED = "Removed"
CATEGORY_SECURITY = "Security"
CATEGORY_UNCATEGORIZED = "Uncategorized"

# Commit prefixes per category
PREFIXES: dict[str, list[str]] = {
    CATEGORY_ADDED: ["feat"],
    CATEGORY_CHANGED: ["perf"],
    CATEGORY_DEPRECATED: [],
    CATEGORY_REMOVED: ["Revert"],
    CATEGORY_FIXED: ["fix"],
    CATEGORY_SECURITY: [],
}

# Commit prefixes to ignore and exclude from the changelog
IGNORED_PREFIXES = [
    "wip",
]

# Header of the changelog file
#
# See: https://keepachangelog.com/en/1.1.0/
CHANGELOG_HEADER = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""


@dataclass
class Commit:
    sha: str
    message: str


def run(command: str) -> str:
    """Runs a command and returns the output."""
    return (
        subprocess.check_output(  # noqa: S602
            command, shell=True, stderr=subprocess.DEVNULL
        )
        .decode("utf-8")
        .strip()
    )


def git_remote_url() -> str:
    """Gets the URL of the remote repository.

    The URL will be converted to the following format:

        https://<host>/<owner>/<repo>
    """
    try:
        output = run("git remote get-url origin")
        if m := RE_REPO_URL.match(output):
            return f"https://{m.group(1)}/{m.group(2)}/{m.group(3)}"
    except subprocess.CalledProcessError:
        pass
    return ""


def git_first_sha() -> str:
    """Gets the hash of the first commit in the repository."""
    return run("git rev-list --max-parents=0 HEAD")


def git_last_sha() -> str:
    """Gets the hash of the last commit in the repository."""
    return run("git rev-parse HEAD")


def git_tags() -> list[str]:
    """Fetches all Git tags sorted by creation date."""
    output = run("git tag --sort=-creatordate")
    return output.split("\n") if output else []


def git_commits(start: str, end: str) -> list[Commit]:
    """Gets commits between two refs as Commit objects."""
    range = f"{start + '..' if start else ''}{end or git_last_sha()}"
    output = run(f"git log --pretty=format:'%h %s' {range}")

    commits = []
    for line in output.splitlines():
        sha, msg = line.split(" ", 1)
        commits.append(Commit(sha, msg.strip()))
    return commits


def git_ref_date(ref: str) -> str:
    """Gets the date of a Git reference."""
    return run(f"git log -1 --format=%as {ref}")


def format_msg(url: str, commit: Commit | str) -> str:
    """Format commit message with PR or commit link."""
    # If it's already a string, it means that it was already formatted,
    # so just return it as is.
    if isinstance(commit, str):
        return commit

    msg = f"- {commit.message}"
    if match := RE_PR_NUMBER.search(msg):
        pull = match.group(1)
        msg = RE_PR_NUMBER.sub(f"([#{pull}]({url}/pull/{pull}))", msg)
    elif commit.sha:
        msg += f" ([{commit.sha}]({url}/commit/{commit.sha}))"
    return msg


# Entries of a changelog per category
Entries = dict[str, list[Commit | str]]


class Release:
    """Release of a specific version."""

    def __init__(self, version: str, entries: Entries, date: str = "") -> None:
        self.version = version
        self.date = date
        self.entries = entries

    @staticmethod
    def from_git(tag: str, parent: str) -> "Release":
        """Returns a `Release` object from a Git tag."""
        commits = git_commits(parent, tag)
        entries = classify_commits(commits)
        version = tag.removeprefix("v") if tag else "Unreleased"
        date = git_ref_date(tag) if tag else ""
        return Release(version, entries, date)

    def format(self, url: str) -> str:
        """Formats the release into the changelog format."""
        output = []
        output.append("")
        output.append(
            f"## [{self.version}]" + (f" - {self.date}" if self.date else "")
        )
        output.append("")
        for category, commits in sorted(self.entries.items()):
            if commits:
                output.append(f"### {category}")
                output.append("")
                output.extend(format_msg(url, c) for c in commits)
                output.append("")
        return "\n".join(output)

    def is_release(self) -> bool:
        """Returns `True` if the version is a release, `False` otherwise."""
        return self.version != "Unreleased"


# Changelog (list of releases)
Changelog = list[Release]


def read_all_lines(path: str) -> list[str]:
    """Reads all lines from a file."""
    try:
        with open(path) as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


def parse_changelog(path: str) -> Changelog:
    """Parses a changelog file into a list of releases."""
    version: str = ""
    date: str = ""
    sections: Entries = {}
    releases: Changelog = []

    for line in read_all_lines(path):
        if RE_LINKS.match(line):
            continue

        release_match = RE_RELEASE.match(line)
        if release_match:
            # If we're already tracking a release, save it before moving
            # to the next one...
            if version:
                releases.append(Release(version, sections, date))

            # Then start a new release
            version = release_match.group(1)
            date = release_match.group(2)  # Can be `None`
            sections = {}
            continue

        section_match = RE_SECTION.match(line)
        if section_match:
            section = section_match.group(1)
            sections[section] = []
            continue

        if line and version and sections and section in sections:
            sections[section].append(line)

    # Append the last tracked release
    if version:
        releases.append(Release(version, sections, date))

    return releases


def starts_with_any(string: str, prefixes: list[str]) -> bool:
    """Returns `True` if `string` starts with any of the `prefixes`."""
    return any(string.startswith(p) for p in prefixes)


def classify_commits(commits: list[Commit]) -> Entries:
    """Categorizes commits into changelog sections using Commit objects."""
    entries: Entries = {}

    def append(category: str, commit: Commit) -> None:
        entries.setdefault(category, []).append(commit)

    for commit in commits:
        if starts_with_any(commit.message, IGNORED_PREFIXES):
            continue
        for category, prefixes in PREFIXES.items():
            if starts_with_any(commit.message, prefixes):
                append(category, commit)
                break
        else:
            # These commits are kept even if they don't match any
            # category, otherwise their prefixes should be added to
            # `IGNORED_PREFIXES` to exclude them from the changelog.
            append(CATEGORY_UNCATEGORIZED, commit)

    return entries


def diff_url(url: str, base: str | None, head: str | None) -> str:
    """Returns the URL to compare two refs."""
    if head:
        version = head.removeprefix("v")
        path = f"compare/{base}...{head}" if base else f"releases/tag/{head}"
    else:
        version = "Unreleased"
        path = f"compare/{base}...HEAD" if base else "commits/main"
    return f"[{version}]: {url}/{path}\n"


def merge_changelogs(
    current: Changelog, new: Changelog, edit: bool
) -> Changelog:
    """Merges the current and new changelogs."""
    # If `edit` is `False`, use "Unreleased" from `current`; if `True`,
    # use it from `new`.
    existing = {r.version: r for r in current if r.is_release() or not edit}
    return [existing.get(r.version, r) for r in new]


def git_tag_ranges(last: str = "") -> Generator[tuple[str, str]]:
    """Generates Git ranges (base, head) for each tag."""
    tags = git_tags()
    if last:
        bases = [last, *tags, ""]
        heads = ["", last, *tags]
    else:
        bases = [*tags, ""]
        heads = ["", *tags]
    yield from zip(bases, heads, strict=True)


def git_changelog() -> Changelog:
    """Returns `Release` objects from a Git history.

    The range `<ref>..<None>` represents all commits from `<ref>` to
    `HEAD` (inclusive).

    The range `<None>..<ref>` represents all commits from the first
    commit up to `<ref>` (inclusive).
    """
    return [Release.from_git(head, base) for base, head in git_tag_ranges()]


def main(
    path: Annotated[
        str,
        typer.Argument(
            help="Path to the changelog file.",
        ),
    ] = "CHANGELOG.md",
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-u",
            help="GitHub URL of the repository.",
        ),
    ] = "",
    version: Annotated[
        str,
        typer.Option(
            "--release",
            "-r",
            help="Create a new release with the given version.",
        ),
    ] = "",
    edit_unreleased: Annotated[
        bool,
        typer.Option(
            "--unreleased",
            "-e",
            help='Edit the "Unreleased" section.',
        ),
    ] = False,
) -> None:
    """Generates or updates a changelog file."""
    changelog = merge_changelogs(
        parse_changelog(path), git_changelog(), edit_unreleased
    )

    # Try to get the repository URL from the Git remote if not provided
    url = url or git_remote_url()

    for r in changelog:
        if version.removeprefix("v") == r.version:
            print(f'Version "{version}" already exists in the changelog')
            raise typer.Exit()

    if version and changelog and not changelog[0].is_release():
        # Convert the "Unreleased" section into a release
        changelog[0].version = version.removeprefix("v")
        changelog[0].date = datetime.date.today().isoformat()
        # And add an empty "Unreleased" section
        changelog.insert(0, Release("Unreleased", {}))

    with open(path, "w") as file:
        file.write(CHANGELOG_HEADER)
        file.writelines(r.format(url) for r in changelog)
        if url:
            file.write("\n")
            file.writelines(
                diff_url(url, base, head)
                for base, head in git_tag_ranges(version)
            )


def app():
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
