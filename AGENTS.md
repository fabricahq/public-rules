# Fabrica Public Rules Library agent guide

This repository is a [Code Rules](https://github.com/fabricahq/code-rules) library. The [README](README.md) explains what it contains and how to contribute.

Use the Code Rules version that `.github/workflows/code-rules.yml` pins, so your checks match CI.

## Rules

Write and revise rules with the [Code Rules rule rubric and template](https://code-rules.fabricahq.com/reference/rule-authoring/). When you add, remove, rename, or retitle a rule or group, update the README's rule count badge, group table, rule lists, and install command to match.

## Change notes

Each rule has its own version, and library releases publish rule changes to projects. Once the library has published its first library release, a `release/1` tag, every new, changed, or retired rule needs a change note in `changes/`. Record it with `code-rules library change` in the same pull request as the rule change:

- **Changed rule:** `code-rules library change RULE_ID --bump major|minor|patch --summary '...'`. Choose the level from what the change does to the rule's obligation, as `code-rules library change --help` defines it. When unsure, choose the larger level.
- **New rule:** `code-rules library change RULE_ID --summary '...'`. A new rule starts at version 1.0.0, so it takes no `--bump`.
- **Retired rule:** delete the rule's Markdown file and asset directory, then run `code-rules library change RULE_ID --retire --summary '...'`, adding `--replaced-by NEW_RULE_ID` when another rule replaces it. A rename or move retires the old ID and adds the new one; see [Rename a rule](https://code-rules.fabricahq.com/guides/version-rules/#rename-a-rule).

Write each summary as one line for project maintainers deciding whether to update: what changed in the obligation or guidance, not how you edited the file. Group descriptions in `_group.yaml` and shared files in `assets/` are library-wide and need no note. Change notes stay in `changes/` permanently; to reword one before it's published, edit it. See [Version your rules](https://code-rules.fabricahq.com/guides/version-rules/) for the full workflow.

## Validate

Before you push, run these from the repository root:

```sh
code-rules library check
uv run .github/scripts/check-readme.py
```

`code-rules library check` fails when a rule change is missing a note or a note doesn't match a change, and otherwise previews the pending library release. The **Code Rules** and **README** workflows run these checks on every pull request.

## Library releases

The maintainer publishes library releases with `code-rules library release`, which tags `release/<number>` and creates the GitHub Release page. Your part ends at the pull request: you may preview a library release with `code-rules library release --dry-run`, and leave publishing, `release/*` tags, and GitHub Release pages to the maintainer.
