---
title: "Derive a parsed value with a method instead of storing it beside its text"
whenToRead: "Before planning, writing, changing, or reviewing Go structs that keep a value's text and also need its parsed or normalized form, such as configuration settings, or code that parses such a field again or compares such values."
impact: "MEDIUM"
impactDescription: "A stored parsed copy can drift from the text it came from, so callers disagree about which field to trust, parse the text again, or compare spellings instead of meanings."
tags: "go, structs, parsing, invariants"
---

## Derive a parsed value with a method instead of storing it beside its text

Keep one authoritative representation of a value.
When a struct must keep a value's original text and parsing it is cheap and deterministic, derive the parsed form through one method instead of storing a second, independently writable field.

### Implementation

- Store the text in one field, and add one method that parses it and returns the parsed form.
- Match the method's result to what the type guarantees:
  - When the text can be invalid, as with an exported field that struct literals and assignments can set, report parse failures separately from absence, such as `(T, bool, error)` for an optional value.
  - Return `(T, bool)` only when the type guarantees valid text, for example because the field is unexported and a constructor validates it. Then false can only mean the value is absent.
- Validate the text where the struct is built, such as in the configuration parser, so users see the error early. The method still reports errors when the type doesn't guarantee validity.
- Send every caller that needs the parsed form through that method, and remove the other places that parse the same field.
- Compare canonical parsed values, not text, when meaning matters, such as deciding whether a setting changed.
  Use the type's semantic equality: `==` when parsing produces a canonical, comparable value, or an `Equal` method when field-by-field equality doesn't match the domain's meaning.
- Use the text only where the author's spelling should appear: writing the file back, messages, and records of what the author wrote.

This rule covers stored parsed or normalized copies of retained text. It doesn't cover:

- **Only the parsed form stored:** when nothing needs the original spelling, store the parsed form and format it for output.
- **Caches of costly parsing:** store both forms only when parsing is costly, and make construction and every later update keep them consistent, such as unexported fields that one constructor and one setter write together. Unexported fields alone don't guarantee that.
- **Values that need I/O:** a value derived through I/O, such as the commit a tag pointed to when it was fetched, is a snapshot of the outside world, not a function of the text. Store it as its own field and document what it records and when.
- **Other derived state:** indexes, aggregates, and caches that aren't a parsed form of retained text are outside this rule.

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
Comparing the text reports a change when the user rewrites `release/5` as `refs/tags/release/5`, though both are the same reference.

**Correct:**

```go
// GitRef is a canonical Git reference: a full tag name, such as refs/tags/release/5, or a lowercase
// commit SHA. ParseGitRef normalizes every accepted spelling, so == compares meaning.
type GitRef struct {
	Kind RefKind
	Name string
}

type Source struct {
	Name string
	// Ref is the tag or commit the user wrote, or empty when the source follows the newest release.
	Ref string
}

// GitRef returns the source's parsed ref. It returns false with a nil error when the source has no ref,
// and an error when Ref isn't a valid ref, which a struct literal or assignment can produce.
func (s Source) GitRef() (GitRef, bool, error) {
	if s.Ref == "" {
		return GitRef{}, false, nil
	}
	ref, err := ParseGitRef(s.Ref)
	if err != nil {
		return GitRef{}, false, err
	}
	return ref, true, nil
}

// SameRef reports whether ref is the same normalized reference as the source's ref.
func (s Source) SameRef(ref string) (bool, error) {
	own, ok, err := s.GitRef()
	if err != nil {
		return false, err
	}
	if !ok || ref == "" {
		return !ok && ref == "", nil
	}
	other, err := ParseGitRef(ref)
	if err != nil {
		return false, err
	}
	return own == other, nil
}
```

`Ref` is the only stored form, so no invariant links two fields.
Callers get the parsed form from `GitRef`, which keeps a missing ref and an invalid one apart.
`SameRef` compares canonical values, so rewriting `release/5` as `refs/tags/release/5` isn't a change.
It compares references, not the commits they resolve to: two different tags on one commit are still different choices.
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

For each struct that keeps a value's text, look for a field holding its parsed or normalized form.
Check that it's either replaced by a method or kept consistent by construction and every later update.
Check that a method returning `(T, bool)` can't hide a parse failure as absence.
Search for calls that parse the same field outside its method; each is a sign that the stored or derived form isn't trusted.
Check that comparisons that decide whether a value changed compare canonical parsed values with the type's semantic equality, not text.

These aren't violations:

- Two fields that are independent inputs, even when they're related.
- A snapshot derived through I/O, stored as its own documented field.
- A struct that mirrors an external format carrying both forms, as long as code reads the parsed form through one function.
