# Fabrica Public Rules Library

<p>
  <a href="LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://github.com/fabricahq/code-rules"><img alt="A Code Rules library" src="https://img.shields.io/badge/Code%20Rules-library-6f42c1"></a>
  <img alt="13 groups, 125 rules" src="https://img.shields.io/badge/rules-125-brightgreen">
</p>

Fabrica Public Rules Library is a collection of engineering rules that tell coding agents how to write and review production-grade code. Each rule covers one practice, such as reproducing a bug with a test before fixing it, or narrowing unknown values in TypeScript, with examples of what to do, what to avoid, and what a reviewer should check.

The rules are organized into groups. Practice groups (`practices/`) apply in any language, and technology groups (`techs/`) cover one language, framework, or tool. You choose the groups that match your stack, and you can leave out any rule you disagree with.

## What rules are included?

| Group | Rules | Description |
| --- | --: | --- |
| [Testing](practices/testing/) | 8 | Where to spend testing effort, and how to write tests that stay reliable |
| [Code design](practices/code-design/) | 3 | Structuring functions, modules, and folders so code stays readable |
| [Performance](practices/performance/) | 1 | Making code faster where measurement shows it matters |
| [READMEs](practices/readmes/) | 5 | Writing READMEs that say what a product does for the reader, get them to a first result, and fit the product's tier |
| [TypeScript](techs/typescript/) | 19 | Writing type-safe, maintainable TypeScript |
| [JavaScript](techs/javascript/) | 7 | Async work, browser APIs, and build-friendly code in JavaScript and TypeScript |
| [React](techs/react/) | 39 | Building correct, accessible, and fast React interfaces, on the client and server |
| [TanStack Query](techs/tanstack-query/) | 15 | Fetching, caching, and updating server data with TanStack Query |
| [TanStack Router](techs/tanstack-router/) | 10 | Typed routing, data loading, and navigation with TanStack Router |
| [Zustand](techs/zustand/) | 10 | Managing shared client state with Zustand |
| [Playwright](techs/playwright/) | 2 | Writing stable browser tests with Playwright |
| [Go](techs/go/) | 5 | Writing well-documented Go with useful errors |
| [Goose](techs/goose/) | 1 | Organizing SQL migrations managed by goose |

### Browse all 125 rules

<details>
<summary><strong>Testing</strong> · 8 rules</summary>

- [Choose tests by risk and cost](practices/testing/choose-tests-by-risk.md)
- [Cover empty inputs and boundaries](practices/testing/cover-boundary-cases.md)
- [Keep tests independent](practices/testing/keep-tests-independent.md)
- [Name tests for the behavior and the condition](practices/testing/name-tests-for-behavior-and-condition.md)
- [Run focused tests while iterating, and the full suite before finishing](practices/testing/run-focused-tests-while-iterating.md)
- [Test at the lowest layer that proves the behavior](practices/testing/test-at-the-lowest-layer.md)
- [Reproduce bugs with regression tests](practices/testing/test-bug-fixes-before-fixing.md)
- [Test observable behavior](practices/testing/test-observable-behavior.md)

</details>

<details>
<summary><strong>Code design</strong> · 3 rules</summary>

- [Express operations as meaningful steps](practices/code-design/express-operations-as-meaningful-steps.md)
- [Organize code by feature](practices/code-design/organize-code-by-feature.md)
- [Separate pure computation from effects](practices/code-design/separate-pure-computation-from-effects.md)

</details>

<details>
<summary><strong>Performance</strong> · 1 rule</summary>

- [Optimize measured hot paths by removing repeated work](practices/performance/optimize-measured-hot-paths.md)

</details>

<details>
<summary><strong>READMEs</strong> · 5 rules</summary>

- [Give a quick start that runs as written](practices/readmes/give-a-quick-start-that-runs-as-written.md)
- [Keep the README an entry point, and link to the full documentation](practices/readmes/keep-the-readme-an-entry-point.md)
- [Match the README's presentation to the product's tier](practices/readmes/match-presentation-to-product-tier.md)
- [Open with what the product does for the reader](practices/readmes/open-with-what-the-product-does.md)
- [State what the product does not do](practices/readmes/state-what-the-product-does-not-do.md)

</details>

<details>
<summary><strong>TypeScript</strong> · 19 rules</summary>

- [Annotate types at module boundaries and where they narrow](techs/typescript/annotate-types-at-boundaries.md)
- [Avoid silencing the type checker](techs/typescript/avoid-silencing-the-type-checker.md)
- [Comment the role, the result, and the hidden constraint](techs/typescript/comment-role-result-and-constraints.md)
- [Declare constants with as const, and satisfies when a type exists](techs/typescript/declare-constants-with-as-const.md)
- [Distinguish null from undefined](techs/typescript/distinguish-null-from-undefined.md)
- [Generate service types from their contracts](techs/typescript/generate-service-types-from-contracts.md)
- [Model distinct states as discriminated unions](techs/typescript/model-variants-as-discriminated-unions.md)
- [Narrow unknown values before use](techs/typescript/narrow-unknown-values.md)
- [Prefer literal unions over enums](techs/typescript/prefer-literal-unions-over-enums.md)
- [Prefer type aliases over interfaces](techs/typescript/prefer-type-aliases.md)
- [Preserve caller-owned data](techs/typescript/preserve-caller-owned-data.md)
- [Make properties and parameters required, and name them](techs/typescript/require-properties-and-name-parameters.md)
- [Import types with import type](techs/typescript/separate-type-imports.md)
- [Use Boolean() for explicit boolean coercion](techs/typescript/use-boolean-for-explicit-boolean-coercion.md)
- [Follow consistent naming conventions](techs/typescript/use-consistent-naming.md)
- [Use one array type syntax](techs/typescript/use-generic-array-types.md)
- [Use named exports](techs/typescript/use-named-exports.md)
- [Use predictable file names](techs/typescript/use-predictable-file-names.md)
- [Use template literal types for patterned strings](techs/typescript/use-template-literal-types-for-patterned-strings.md)

</details>

<details>
<summary><strong>JavaScript</strong> · 7 rules</summary>

- [Avoid layout thrashing](techs/javascript/avoid-layout-thrashing.md)
- [Await only on paths that need the result](techs/javascript/await-only-on-paths-that-need-the-result.md)
- [Defer non-critical browser work to idle time](techs/javascript/defer-non-critical-work-to-idle-time.md)
- [Keep dynamic import and file paths statically analyzable](techs/javascript/keep-import-and-file-paths-analyzable.md)
- [Start independent asynchronous work concurrently](techs/javascript/start-independent-async-work-concurrently.md)
- [Mark scroll-related listeners passive when they never cancel scrolling](techs/javascript/use-passive-scroll-and-touch-listeners.md)
- [Version and minimize data in browser storage](techs/javascript/version-and-minimize-browser-storage.md)

</details>

<details>
<summary><strong>React</strong> · 39 rules</summary>

- [Give every interactive element a role and an accessible name](techs/react/accessibility-roles-and-names.md)
- [Run app-wide initialization once per app load](techs/react/advanced-init-once.md)
- [Build complex components from composable parts](techs/react/architecture-compound-components.md)
- [Create explicit component variants instead of boolean mode props](techs/react/architecture-explicit-variants.md)
- [Stream slow data behind Suspense boundaries](techs/react/async-suspense-boundaries.md)
- [Avoid loading large barrel files](techs/react/bundle-barrel-imports.md)
- [Keep non-critical scripts off the critical path](techs/react/bundle-defer-non-critical-scripts.md)
- [Load heavy optional code on demand](techs/react/bundle-load-heavy-code-on-demand.md)
- [Share client data requests through a caching data layer](techs/react/client-share-data-requests.md)
- [Read the latest callbacks in Effects without resubscribing](techs/react/effects-read-latest-values-without-resubscribing.md)
- [Name generic components by capability, not by first caller](techs/react/generic-components-by-capability.md)
- [Name Effect and non-trivial Hook callbacks](techs/react/hooks-name-callbacks.md)
- [Avoid copying props to state](techs/react/official-avoid-copying-props-to-state.md)
- [Avoid unnecessary Effects](techs/react/official-avoid-unnecessary-effects.md)
- [Follow the Rules of Hooks](techs/react/official-follow-rules-of-hooks.md)
- [Keep components and Hooks pure](techs/react/official-keep-components-and-hooks-pure.md)
- [Accept ref as a prop in React 19](techs/react/react19-no-forwardref.md)
- [Use Activity to hide UI that should keep its state](techs/react/rendering-activity.md)
- [Use a boolean condition for conditional rendering](techs/react/rendering-conditional-render.md)
- [Skip off-screen rendering work in long lists](techs/react/rendering-content-visibility.md)
- [Render client-only preferences without a flash or hydration error](techs/react/rendering-hydration-no-flicker.md)
- [Suppress only expected hydration mismatches](techs/react/rendering-hydration-suppress-warning.md)
- [Hint critical resources with React DOM resource APIs](techs/react/rendering-resource-hints.md)
- [Subscribe to and depend on only the values you use](techs/react/rerender-depend-on-narrow-values.md)
- [Use functional updates when new state depends on old state](techs/react/rerender-functional-setstate.md)
- [Initialize expensive state lazily](techs/react/rerender-lazy-state-init.md)
- [Keep input responsive by marking non-urgent updates](techs/react/rerender-mark-non-urgent-updates.md)
- [Memoize deliberately](techs/react/rerender-memoize-deliberately.md)
- [Do not define components inside components](techs/react/rerender-no-inline-components.md)
- [Keep values that do not affect rendering in refs](techs/react/rerender-use-ref-transient-values.md)
- [Run post-response work after the response](techs/react/server-after-nonblocking.md)
- [Authenticate and authorize inside every Server Action](techs/react/server-auth-actions.md)
- [Deduplicate per-request server work with cache](techs/react/server-cache-react.md)
- [Pass only the data Client Components use](techs/react/server-minimize-serialized-props.md)
- [Keep request data out of shared module state](techs/react/server-no-shared-module-state.md)
- [Compose independent server data fetches as siblings](techs/react/server-parallel-fetching.md)
- [Reuse request-independent server data across requests](techs/react/server-reuse-request-independent-data.md)
- [Lift shared component state into a provider behind an interface](techs/react/state-lift-shared-state-into-providers.md)
- [Give repeated and persistent surfaces stable test ids](techs/react/testing-ship-stable-e2e-scope-test-ids.md)

</details>

<details>
<summary><strong>TanStack Query</strong> · 15 rules</summary>

- [Use initialData only for complete data](techs/tanstack-query/cache-placeholder-vs-initial.md)
- [Set staleTime from how fast data changes](techs/tanstack-query/cache-stale-time.md)
- [Reset query errors when an error boundary retries](techs/tanstack-query/err-error-boundaries.md)
- [Derive infinite query page params from the server's response](techs/tanstack-query/inf-page-params.md)
- [Invalidate or update every query a mutation changes](techs/tanstack-query/mut-invalidate-queries.md)
- [Read mutation state from other components with useMutationState](techs/tanstack-query/mut-mutation-state.md)
- [Make optimistic updates reversible, and decide them once](techs/tanstack-query/mut-optimistic-updates.md)
- [Make offline behavior explicit](techs/tanstack-query/offline-behavior.md)
- [Fetch a dynamic set of queries with useQueries](techs/tanstack-query/parallel-use-queries.md)
- [Derive component views of query data with a stable select](techs/tanstack-query/perf-select-transform.md)
- [Prefetch likely next data on user intent](techs/tanstack-query/pf-intent-prefetch.md)
- [Define hierarchical query keys and options in factories](techs/tanstack-query/qk-factory-pattern.md)
- [Key each query by every input it uses](techs/tanstack-query/qk-include-dependencies.md)
- [Pass the query's AbortSignal to the request](techs/tanstack-query/query-cancellation.md)
- [Prefetch on the server and hydrate the query cache](techs/tanstack-query/ssr-dehydration.md)

</details>

<details>
<summary><strong>TanStack Router</strong> · 10 rules</summary>

- [Provide shared dependencies through typed router context](techs/tanstack-router/ctx-router-context.md)
- [Throw notFound for missing resources and render it with notFoundComponent](techs/tanstack-router/err-not-found.md)
- [With TanStack Query, load route data into the Query cache](techs/tanstack-router/load-ensure-query-data.md)
- [Load route data in loaders, in parallel](techs/tanstack-router/load-use-loaders.md)
- [Use Link for navigation users can open, and redirect in the router](techs/tanstack-router/nav-link-component.md)
- [Mask modal routes with the resource's canonical URL](techs/tanstack-router/nav-route-masks.md)
- [Set app-wide navigation behavior in router defaults](techs/tanstack-router/router-default-options.md)
- [Validate search params with defaults at the route](techs/tanstack-router/search-validation.md)
- [Split route components out of the main bundle](techs/tanstack-router/split-route-code.md)
- [Register the router and read route data through typed route APIs](techs/tanstack-router/ts-route-type-inference.md)

</details>

<details>
<summary><strong>Zustand</strong> · 10 rules</summary>

- [Create stores once, outside render](techs/zustand/create-stores-at-module-scope.md)
- [Define typed state and named actions](techs/zustand/define-typed-state-and-named-actions.md)
- [Keep store state serializable](techs/zustand/keep-store-state-serializable.md)
- [Keep each store focused on one domain](techs/zustand/keep-stores-domain-focused.md)
- [Persist only safe, versioned state](techs/zustand/persist-only-safe-versioned-state.md)
- [Rehydrate persisted stores after React hydration](techs/zustand/rehydrate-persisted-stores-after-hydration.md)
- [Subscribe with narrow, stable selectors](techs/zustand/subscribe-with-selectors.md)
- [Reset stores between tests and test actions directly](techs/zustand/test-actions-and-reset-stores.md)
- [Update store state functionally and immutably](techs/zustand/use-functional-and-immutable-updates.md)
- [Use Zustand only for shared client state](techs/zustand/use-zustand-only-for-shared-client-state.md)

</details>

<details>
<summary><strong>Playwright</strong> · 2 rules</summary>

- [Synchronize with auto-waiting actions and web-first assertions](techs/playwright/auto-waiting-actions-and-web-first-assertions.md)
- [Scope locators by test id, then select controls by role and name](techs/playwright/domain-scope-and-user-facing-locators.md)

</details>

<details>
<summary><strong>Go</strong> · 5 rules</summary>

- [Comment struct fields whose meaning the type does not show](techs/go/comment-non-obvious-struct-fields.md)
- [Separate package documentation from file headers](techs/go/comments-package-doc-vs-file-header.md)
- [Add operation and identifier context to errors at boundaries](techs/go/errors-include-useful-diagnostic-data.md)
- [Expose error identity only for contract errors](techs/go/errors-use-contract-errors-deliberately.md)
- [Derive a parsed value with a method instead of storing it beside its text](techs/go/structs-derive-parsed-values-with-methods.md)

</details>

<details>
<summary><strong>Goose</strong> · 1 rule</summary>

- [Keep the SQL migration directory for migration files only](techs/goose/migrations-directory-contains-only-sql.md)

</details>

## How does it relate to Code Rules?

[Code Rules](https://github.com/fabricahq/code-rules) is the tool, and this repository is content for it:

- **Code Rules** is a command-line tool that manages the rules your agents follow in a project. It imports rules from libraries, pins each library to a version, and builds the guidance your agents read.
- **This library** is one collection of rules you can import with it. [Fabrica](https://fabricahq.com) wrote or curated these rules from its own experience and publishes them as versioned releases.

It's the same relationship as a package manager and a package. You install Code Rules once, then add this library to each project, alongside any others, such as your own team's rules.

## How do I use this repo?

1. [Install Code Rules](https://code-rules.fabricahq.com/start-here/install/) on your local computers.
2. [Set up your project](https://code-rules.fabricahq.com/start-here/set-up-project/) to use Code Rules.
3. Add this library as a source. Within the project directory, run the command below. It selects every group; delete the `--groups` lines you don't need.

   ```sh
   code-rules project add library fabrica \
     --repository https://github.com/fabricahq/public-rules.git \
     --groups practices/code-design \
     --groups practices/performance \
     --groups practices/readmes \
     --groups practices/testing \
     --groups techs/go \
     --groups techs/goose \
     --groups techs/javascript \
     --groups techs/playwright \
     --groups techs/react \
     --groups techs/tanstack-query \
     --groups techs/tanstack-router \
     --groups techs/typescript \
     --groups techs/zustand \
     --ref v1.1.0
   ```

   To take every group, including ones added in future versions, pass a single wildcard instead: `--groups '*'` for everything, `--groups 'practices/*'` for all practice groups, or `--groups 'techs/*'` for all technology groups. Quote the wildcard so your shell doesn't expand it. See [Select groups from each source](https://code-rules.fabricahq.com/guides/select-rules/#select-groups-from-each-source).

   You can also leave out individual rules from a group you import. See [Exclude a rule](https://code-rules.fabricahq.com/guides/select-rules/#exclude-a-rule).

4. Download the rules and build the guidance your agent reads:

   ```sh
   code-rules project sync
   ```

5. If you haven't already, [tell your agent to read the rules](https://code-rules.fabricahq.com/start-here/set-up-project/#5-give-the-rules-to-your-agent), then commit the `.code-rules/` directory.

## FAQs

### What does a rule look like?

A rule is a Markdown file. Its YAML frontmatter gives the rule a title, says when an agent should read it, and describes why it matters. Its body states one obligation, then gives implementation guidance, incorrect and correct examples, and the evidence a reviewer should look for. For a representative example, read [Reproduce bugs with regression tests](practices/testing/test-bug-fixes-before-fixing.md).

Every rule in this library follows the Code Rules [rule rubric and template](https://code-rules.fabricahq.com/reference/rule-authoring/).

### Do I have to follow every rule?

No. These rules are opinions on specific technologies and practices. In some cases, you may not be using that technology, or following that practice. In some cases, you may outright disagree with the rule.

Code Rules is designed to allow importing whatever collection of rules you want, so you can import one rule from this library, or all of them.

### What if I find a mistake in a rule?

Open a pull request that fixes it. See [How do I contribute?](#how-do-i-contribute) for how to check your change before you submit it.

These rules come from Fabrica's own real-world experience, and yours may differ. If a rule is wrong or incomplete, we welcome the fix, and everyone who uses Fabrica Public Rules Library benefits from it.

## How do I contribute?

Open a pull request!

Be sure to follow the [Code Rules authoring rubric](https://code-rules.fabricahq.com/reference/rule-authoring/), and validate the library from its root before you push:

```sh
code-rules library check
uv run .github/scripts/check-readme.py
```

The second command checks that this README still lists every group and rule. Pull request checks run both.

Maintainers review changes in pull requests. Releases are made with [Release Planner](https://github.com/fabricahq/release-planner): an agent drafts the notes in a release pull request, and merging it tags and publishes the release. The [release policy](.release-planner/policy.md) explains how versions are chosen and what counts as a breaking change. Released tags never move. For the file format, see [Rule and library format](https://code-rules.fabricahq.com/reference/rule-library-format/).

## License and sources

The library is [MIT licensed](LICENSE.md), with copyright attributed to Fabrica Systems LLC.

Some rules adapt material from third parties, and others draw on official documentation. Adapted rules carry attribution in their metadata, and [NOTICE.md](NOTICE.md) preserves the required third-party notices.
