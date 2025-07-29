# Keep A Changelog

**kacl** is a tool to generate a changelog based on your git commit history.

## Installation

You can install **kacl** using `pipx`:

```bash
pipx install kacl
```

## Usage

### Generate a changelog

```bash
kacl
```

### Update the **Unreleased** section

This will edit the **Unreleased** section of your changelog. It will be
generated from the commits since the last release.

```bash
kacl -e
```

### Create a new release

This will create a new release based on tag `v1.2.3`. If a **Unreleased** is
present, it will be moved to the new release section.

```bash
kacl -r v1.2.3
```

> [!NOTE]
> The `r` option can be combined with the `-e` option to create a new release
> based on the commits since the last release.
