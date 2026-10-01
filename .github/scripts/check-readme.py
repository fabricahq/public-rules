#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Check that README.md lists exactly the groups and rules in the library.

Checks the rule count badge, the group table, and the "Browse all N rules"
lists against the library files, and the totals against `code-rules library
check`. Run from the repository root with code-rules on PATH:

    uv run .github/scripts/check-readme.py
"""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

GROUP_ROOTS = ("practices", "techs")

errors = []


def fail(message):
    errors.append(message)


def field(path, text, key):
    """Read a string field from one YAML document, as Code Rules does.

    BaseLoader keeps every scalar a string, so values such as `yes` or `1.0`
    are not converted to other types.
    """
    value = yaml.load(text, Loader=yaml.BaseLoader).get(key)
    if not isinstance(value, str):
        raise ValueError(f"{path}: {key} must be a string")
    return value.strip()


def frontmatter(path):
    text = path.read_text()
    match = re.match(r"---\n(.*?\n)---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing frontmatter")
    return match.group(1)


def load_groups():
    """Return {group path: (name, {rule path: title})}, following the library format's discovery."""
    groups = {}
    for root in GROUP_ROOTS:
        for metadata in sorted(Path(root).glob("*/_group.yaml")):
            directory = metadata.parent
            rules = {}
            for rule in sorted(directory.rglob("*.md")):
                relative = rule.relative_to(directory)
                if relative.parts[0] == "assets" or relative == Path("README.md"):
                    continue
                rules[rule.as_posix()] = field(rule, frontmatter(rule), "title")
            groups[directory.as_posix()] = (field(metadata, metadata.read_text(), "name"), rules)
    return groups


def check_totals(groups):
    """Fail if this script and code-rules disagree about what the library contains."""
    result = subprocess.run(
        ["code-rules", "library", "check", "--json"], capture_output=True, text=True
    )
    response = json.loads(result.stdout)
    if not response.get("ok"):
        sys.exit(f"code-rules library check failed:\n{result.stdout}")
    value = response["value"]
    rules = sum(len(group_rules) for _, group_rules in groups.values())
    if (value["groupCount"], value["ruleCount"]) != (len(groups), rules):
        sys.exit(
            f"code-rules counts {value['groupCount']} groups and {value['ruleCount']} rules, "
            f"but this check found {len(groups)} and {rules}; update {__file__}"
        )


def plural(count):
    return f"{count} rule" if count == 1 else f"{count} rules"


def check_badge(readme, group_count, rule_count):
    expected = (
        f'<img alt="{group_count} groups, {rule_count} rules" '
        f'src="https://img.shields.io/badge/rules-{rule_count}-brightgreen">'
    )
    if expected not in readme:
        fail(f"rule count badge should be: {expected}")


def check_table(readme, groups):
    rows = re.findall(r"^\| \[([^\]]+)\]\(([^)]+)/\) \| (\d+) \|", readme, re.MULTILINE)
    seen = set()
    for name, path, count in rows:
        if path in seen:
            fail(f"group table lists {path} more than once")
        seen.add(path)
        if path not in groups:
            fail(f"group table lists {path}, which is not a group")
            continue
        expected_name, rules = groups[path]
        if name != expected_name:
            fail(f"group table names {path} {name!r}; _group.yaml names it {expected_name!r}")
        if int(count) != len(rules):
            fail(f"group table counts {count} rules in {path}; it has {len(rules)}")
    for path in groups.keys() - seen:
        fail(f"group table is missing {path}")


def check_rule_lists(readme, groups, rule_count):
    heading = f"### Browse all {rule_count} rules"
    if not re.search(rf"^{re.escape(heading)}$", readme, re.MULTILINE):
        fail(f"rule list heading should be: {heading}")

    blocks = re.findall(
        r"<summary><strong>([^<]+)</strong> · ([^<]+)</summary>(.*?)</details>", readme, re.DOTALL
    )
    seen = set()
    for name, summary_count, body in blocks:
        items = re.findall(r"^- \[(.+)\]\(([^)]+\.md)\)$", body, re.MULTILINE)
        links = {path: title for title, path in items}
        for path, count in sorted(Counter(path for _, path in items).items()):
            if count > 1:
                fail(f"rule list {name!r} links to {path} more than once")
        paths = {path.rsplit("/", 1)[0] for path in links} or {""}
        if len(paths) != 1 or next(iter(paths)) not in groups:
            fail(f"rule list {name!r} should link to the rules of exactly one group")
            continue
        path = paths.pop()
        if path in seen:
            fail(f"rule lists include {path} more than once")
        seen.add(path)
        expected_name, rules = groups[path]
        if name != expected_name:
            fail(f"rule list for {path} is named {name!r}; _group.yaml names it {expected_name!r}")
        expected_count = plural(len(rules))
        if summary_count != expected_count:
            fail(f"rule list for {path} says {summary_count!r}; it should say {expected_count!r}")
        for rule in rules.keys() - links.keys():
            fail(f"rule list for {path} is missing {rule}")
        for rule in links.keys() - rules.keys():
            fail(f"rule list for {path} links to {rule}, which is not a rule")
        for rule in links.keys() & rules.keys():
            if links[rule] != rules[rule]:
                fail(f"rule list names {rule} {links[rule]!r}; its title is {rules[rule]!r}")
    for path in groups.keys() - seen:
        fail(f"rule lists are missing {path}")


def main():
    groups = load_groups()
    check_totals(groups)
    rule_count = sum(len(rules) for _, rules in groups.values())
    readme = Path("README.md").read_text()
    check_badge(readme, len(groups), rule_count)
    check_table(readme, groups)
    check_rule_lists(readme, groups, rule_count)
    if errors:
        print("README.md does not match the library:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        sys.exit(1)
    print(f"README.md matches the library: {len(groups)} groups, {rule_count} rules.")


if __name__ == "__main__":
    main()
