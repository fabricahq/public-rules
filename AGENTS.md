# Fabrica Public Rules Library agent guide

This repository is a [Code Rules](https://github.com/fabricahq/code-rules) library. The [README](README.md) explains what it contains and how to contribute.

## Rules

Write and revise rules with the [Code Rules rule rubric and template](https://code-rules.fabricahq.com/reference/rule-authoring/). When you add, remove, rename, or retitle a rule or group, update the README's rule count badge, group table, and rule lists to match. Before you push, run these from the repository root:

```sh
code-rules library check
uv run .github/scripts/check-readme.py
```

The **Check** workflow runs both on every pull request.
