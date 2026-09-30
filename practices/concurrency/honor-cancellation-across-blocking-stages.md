---
title: "Honor cancellation across every blocking stage"
whenToRead: "When planning, implementing, changing, or reviewing operations that promise cancellation or deadlines and can wait for coordination, resources, I/O, or retries."
impact: "HIGH"
impactDescription: "Prevents canceled or expired operations from remaining blocked behind unrelated work."
tags: "concurrency, cancellation, deadlines, blocking"
---

## Honor cancellation across every blocking stage

Make every blocking stage of a cancellable operation responsive to the caller's cancellation and deadline. Preserve the time remaining before that deadline across stages.

### Scope and implementation

Apply this rule to operations whose contract includes cancellation or a bounded deadline. This rule concerns blocking waits; it does not require adding cancellation to APIs that do not promise it.

Account for waits before the main I/O call: shared initialization, locks or coordination, pool acquisition, retry delays, and cleanup that delays the caller's return.

Use cancellation-aware waits, or structure ownership so a canceled caller can leave while other work completes safely. Passing a cancellation token to I/O is insufficient when the caller first waits indefinitely for a lock.

When the caller sets a deadline, apply it to the whole operation. Stage-specific limits may shorten the remaining budget, but must not reset or extend it.

Shared work can outlive an individual waiter when other users still need it. Required cleanup can also continue under a separately owned, bounded lifecycle. Define that ownership explicitly, and do not make the canceled caller wait indefinitely for it.

### Rationale

A deadline bounds an operation only when it covers the whole path. An uninterruptible coordination wait can make a short timeout ineffective before any I/O begins.

Separating a waiter's lifetime from shared work also allows one caller to cancel without disrupting other callers.

### Examples

**Incorrect: cancellation begins after an uninterruptible wait**

1. Request A holds the initialization lock while opening a shared connection pool.
2. Request B waits for that lock, then plans to acquire a connection using its cancellation token.
3. B's caller cancels the request while A remains blocked.
4. B cannot return until A finishes and releases the lock, even though B has no remaining work to do.

The cancellation token reaches connection acquisition, but does not cover the earlier coordination wait.

**Correct: a waiter can leave shared initialization**

1. Request A starts shared initialization under the resource owner's lifecycle.
2. Request B waits for either initialization to finish or its own cancellation signal.
3. B's caller cancels the request, and B returns without waiting for A. The owner continues initialization for callers that still need it.
4. A caller that remains waiting uses the initialized pool with the time remaining before its original deadline.

The same contract applies when an operation waits for a connection, a retry delay, or resource retirement.

### Validation

- Hold shared initialization or another coordination stage behind a test-controlled signal. Cancel a waiting caller and verify it returns while that signal remains blocked.
- Exercise cancellation during resource acquisition and retry waits, using controlled signals or a fake clock where appropriate.
- Verify time spent in earlier stages reduces the budget available to later stages.
- Verify a canceled waiter does not interrupt shared work needed by another caller, and that owned cleanup still completes safely.
