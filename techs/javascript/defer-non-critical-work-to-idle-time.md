---
title: "Defer non-critical browser work to idle time"
whenToRead: "Before planning, writing, changing, or reviewing browser code that does secondary work in response to user input or page load, such as sending custom analytics events, persisting drafts, prefetching, or processing large data, or that decides when an analytics or performance-monitoring script loads."
impact: "MEDIUM"
impactDescription: "Secondary work done immediately after user input or during page load competes with rendering the response, making the interface feel slow."
tags: "javascript, browser, scheduling, requestIdleCallback, performance"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-request-idle-callback.md
    description: "Adapted from the Vercel Agent Skills rule js-request-idle-callback: moved from the React group, restructured to the rule template, and generalized the browser support guidance."
---

## Defer non-critical browser work to idle time

Schedule work that the user is not waiting for with `requestIdleCallback`, so it runs when the browser is idle instead of delaying the response to input or the first render of the page.

### Implementation

- Defer secondary work your own code triggers: custom analytics events such as `analytics.track()` calls, saving non-urgent state to storage, prefetching likely next resources, and non-urgent data processing.
- Pass a `timeout` when the work must eventually run even if the browser stays busy, such as sending a custom analytics event.
- Split large jobs into chunks that check `deadline.timeRemaining()` and reschedule themselves.
- `requestIdleCallback` is not available in every browser; check support for the project's target browsers and fall back to `setTimeout`.
- For work that starts during page load, wait for the `load` event and the next animation frame before requesting idle time. Before the first paint, the browser can have idle periods while it waits for resources, so `requestIdleCallback` alone can run the work before anything is on screen. Hidden tabs run no animation frames, so this work waits until the tab is shown.
- Do not defer work the user is waiting for, such as rendering the result of their action.
- Idle callbacks may never run if the user leaves the page; flush work that must not be lost, such as saving a draft, when the page is hidden.
- Loading a page-view or performance-monitoring script, such as a web analytics or real user monitoring beacon, is not deferrable work. Load it the way its vendor documents, usually as an `async`, `defer`, or `type="module"` script, which already stays off the rendering path. These scripts measure the page load themselves and report when the page is hidden, so loading one late loses visits that end before it runs and interactions that happen before it starts observing. Only the custom events your code sends through such a script are deferrable.

### Rationale

JavaScript runs on the same thread that handles input and rendering.
Doing secondary work right after an interaction, or while the page is still loading, delays the frame that shows the result.
Idle callbacks run in gaps when the browser has nothing more urgent to do, but during page load those gaps can come before the first paint.

### Examples

#### Application: Work after user input

Secondary work in an event handler runs before the browser can paint the response.

**Incorrect (counterexample):**

```ts
function handleSearch(query: string) {
  setResults(searchItems(query));
  analytics.track('search', { query });
  saveToRecentSearches(query);
}
```

Tracking and saving run before the browser can paint the results.

**Correct:**

```ts
const scheduleIdle: (callback: () => void) => void =
  typeof requestIdleCallback === 'function'
    ? (callback) => requestIdleCallback(callback, { timeout: 2000 })
    : (callback) => setTimeout(callback, 1);

function handleSearch(query: string) {
  setResults(searchItems(query));
  scheduleIdle(() => {
    analytics.track('search', { query });
    saveToRecentSearches(query);
  });
}
```

#### Application: Work that starts at page load

Code that runs while the page loads, such as a module script, may reach its first idle period before the first paint.

**Incorrect (counterexample):**

```ts
scheduleIdle(prefetchLikelyRoutes);
```

The idle callback can run while the browser waits for resources, before any content is painted.

**Correct:**

```ts
function scheduleAfterPaint(callback: () => void) {
  const afterNextFrame = () => requestAnimationFrame(() => scheduleIdle(callback));
  if (document.readyState === 'complete') afterNextFrame();
  else addEventListener('load', afterNextFrame, { once: true });
}

scheduleAfterPaint(prefetchLikelyRoutes);
```

The prefetch waits until the loaded page has painted a frame, then for idle time.

**Valid without deferral:**

```html
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "SITE_TOKEN"}'></script>
```

This is the vendor's documented snippet for a page-view beacon. The module script does not block rendering, and the beacon must run early to report visits and interactions, so it needs no change.

### Validation

Record a performance profile of the interaction or page load and check that deferred work runs after the result is painted. For page-load work, compare against the `paintTime` of the `first-contentful-paint` entry where the browser provides it; `startTime` is when the frame reached the screen, which can be later.
Check that a fallback exists for browsers without `requestIdleCallback`.

Running work immediately is not a violation when the user is waiting for its result.
Loading a page-view or performance-monitoring script in its vendor's documented non-blocking form is not a violation; deferring that load is.
