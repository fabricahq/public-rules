---
title: "Derive a parsed value with a method instead of storing it beside its text"
whenToRead: "Before planning, writing, changing, or reviewing Go structs that hold one value in two forms, such as configuration text and its parsed or normalized form, or code that parses a struct field again or compares such values."
impact: "MEDIUM"
impactDescription: "A stored copy of a derived value can drift from its source, so callers disagree about which field to trust, parse the text again, or compare spellings instead of meanings."
tags: "go, structs, parsing, invariants"
---

## Derive a parsed value with a method instead of storing it beside its text

When a struct must keep a value's text, such as a setting spelled the way the user wrote it, store only the text and give the struct a method that returns the parsed form.
Don't add a second field for the parsed form that every writer must keep in step with the text.

### Implementation

- Validate the text where the struct is built, such as in the configuration parser, so every struct it returns holds valid text.
- Add one method that parses the text and returns the parsed form. For an optional value, return `(T, bool)`, where false means the value is absent.
  Document on the method that construction already validated the text, so parsing can't fail for a struct the parser returned.
- Send every caller that needs the parsed form through that method, and remove the other places that parse the same field.
- Compare parsed forms when meaning matters, such as deciding whether a setting changed.
  Use the text only where the author's spelling should appear: writing the file back, messages, and records of what the author wrote.

Store only the parsed form, with no text field, when nothing needs the original spelling; format it for output instead.
Store both forms only when parsing is costly or needs I/O, and then keep them in unexported fields that only a constructor sets.

### Rationale

Two exported fields that describe one value create an invariant, such as "nil exactly when `Ref` is empty", that nothing enforces.
Test fixtures, struct literals, and code that edits one field leave the other stale, and a reader can't tell which field is authoritative.
Callers that distrust the stored copy parse the text again, often with slightly different rules, and callers that compare the text treat two spellings of one value as a change.
A method gives the value one source of truth and one way to interpret it.
Parsing short text is typically far cheaper than the work around it, such as I/O, so deriving it on demand rarely costs anything measurable.

### Examples

**Incorrect (counterexample):**

```go
type Source struct {
	Name string
	// Ref is the tag or commit the user wrote, or empty when the source follows the newest release.
	Ref string
	// ParsedRef is Ref after parsing; it is nil exactly when Ref is empty.
	ParsedRef *GitRef
}

// In another package:
func refChanged(source Source, recorded string) bool {
	return source.Ref != recorded
}
```

Every constructor and fixture must set both fields.
Other packages parse `Ref` again because nothing guarantees `ParsedRef` is current.
Comparing the text reports a change when the user rewrites `release/5` as `refs/tags/release/5`, though both name the same tag.

**Correct:**

```go
type Source struct {
	Name string
	// Ref is the tag or commit the user wrote, or empty when the source follows the newest release.
	Ref string
}

// GitRef returns the source's ref, parsed and normalized, and false when the source has none.
// ParseConfiguration already validated Ref, so parsing can't fail for a source it returned.
func (s Source) GitRef() (GitRef, bool) {
	if s.Ref == "" {
		return GitRef{}, false
	}
	ref, err := ParseGitRef(s.Ref)
	return ref, err == nil
}

// SameRef reports whether ref names the same revision as the source's ref once both are parsed.
func (s Source) SameRef(ref string) bool {
	if ref == "" || s.Ref == "" {
		return ref == s.Ref
	}
	own, ok := s.GitRef()
	other, err := ParseGitRef(ref)
	return ok && err == nil && own == other
}
```

`Ref` is the only stored form, so no invariant links two fields.
Callers get the parsed form from `GitRef`, and `SameRef` compares meanings, so rewriting `release/5` as `refs/tags/release/5` isn't a change.
The configuration writer and messages still use `Ref`, the user's spelling.

**Also correct (no change needed):**

```go
type Job struct {
	Name    string
	Timeout time.Duration
}
```

Nothing needs the text the user wrote, so the struct stores only the parsed `time.Duration` and formats it for output.

### Validation

For each struct field computed from another field of the same struct, check that it's either replaced by a method or unexported and set only by a constructor.
Search for calls that parse the same field outside its method; each is a sign that the stored or derived form isn't trusted.
Check that comparisons that decide whether a value changed compare parsed forms, not text.

Two fields that are independent inputs aren't a violation, even when they're related.
A struct that mirrors an external format carrying both forms isn't a violation, as long as code reads the parsed form through one function.
