# Astra Tags documentation authoring plan

## Outcome and audience

Produce a complete English manual and a verified connection to the generated runtime API reference for Unity developers familiar with the Editor and C#. Readers must be able to install the package, configure it, use runtime and editor features, integrate their own assets, and run both samples. Conversations with the maintainer remain in Italian.

The approved unit of work is **one AI session per slice**, with a baseline of 20 slices. Each slice includes source inspection, authoring, examples or procedures, navigation, verification, and hand-off updates. This plan governs documentation work; it does not introduce GSD tooling, automatic execution, or GitHub issues.

The maintainer selected the physical `DocFx/MD/` layout used by AstraRpgHealthDocs, Unity Asset Store installation instructions, manual plus API coverage, and a separate register for missing screenshots. Publishing the site, preparing a release, changing package code, and the host-versus-isolated API comparison spike are outside this authoring milestone.

## Information architecture

Use Health's vocabulary and task-oriented workflows, while deriving all package behavior from Tags source. The structure follows the [Unity package documentation guidance](https://docs.unity3d.com/6000.2/Documentation/Manual/cus-document.html).

| Area | Authored location | Published location |
|---|---|---|
| Home and main navigation | Root `index.md`, `toc.yml` | Site root |
| Manual and its navigation | `DocFx/MD/` | `MD/` |
| Task guides | `DocFx/MD/workflows/` | `MD/workflows/` |
| Advanced material | `DocFx/MD/advanced/` | `MD/advanced/` |
| Sample guides | `DocFx/MD/samples/` | `MD/samples/` |
| Images | `DocFx/images/` | `images/` |
| Runtime API | Generated metadata | `api/` |
| Authoring context | `context/` | Excluded |

Keep the root landing page as the publishing host's entry point. Use explicit content and resource mappings to preserve `MD/` URLs without duplicating pages; see [DocFX configuration](https://dotnet.github.io/docfx/docs/config.html). Include only the root landing/navigation inputs, authored manual, generated API, and image resources. Never include context or operational files through a broad root glob.

The completed manual navigation uses: Introduction; Workflows; Advanced Topics; Limitations; Requirements; Package Contents; Samples; Installation Instructions; Changelog; Migration Guide. Advanced Topics and Samples each provide an overview and links to their detailed guides. Add only existing, substantive pages to navigation and cross-links. Keep unpublished destinations in the coverage matrix, not as broken links on public pages.

Each workflow explains prerequisites, concept, ordered procedure where needed, expected result, a focused example, relevant properties, caveats, and API links. Do not duplicate the reference member by member. The generated reference covers the runtime assembly already selected by the lock. Document public editor extension points manually and use inline type names where metadata has no UID.

## Slice roadmap

Paths below are relative to `DocFx/MD/` unless noted otherwise. Each linked card defines source reads, acceptance, and the session hand-off. State is recorded only in [documentation-state.md](documentation-state.md).

| Slice | Deliverable | Depends on | Risk | Observable outcome |
|---|---|---|---|---|
| [S01](slices/S01.md) | Context system, DocFX layout, root home, `introduction.md` | None | High | Home and introduction render at the intended URLs; operational context is absent from the site |
| [S02](slices/S02.md) | `requirements.md`, `installation-instructions.md`, `package-contents.md` | S01 | High | A new user can follow the verified Asset Store installation path |
| [S03](slices/S03.md) | `workflows/creating-tags.md` | S01 | Medium | A user creates a valid hierarchy and configures tag identity and appearance |
| [S04](slices/S04.md) | `workflows/package-configuration.md` | S03 | High | A user configures editor tooling and a registry available at runtime |
| [S05](slices/S05.md) | `workflows/tag-sets.md` | S03, S04 | Medium | Examples distinguish exact membership, hierarchical matches, and set operations |
| [S06](slices/S06.md) | `workflows/taggable-assets.md` | S05 | Medium | A custom asset exposes tags to the editor tools |
| [S07](slices/S07.md) | `workflows/runtime-containers.md` | S04, S05 | Medium | Releasing one of two grants keeps a tag active until the last grant ends |
| [S08](slices/S08.md) | `workflows/events-and-observers.md` | S07 | Medium | A user distinguishes count changes, presence changes, and observer transitions |
| [S09](slices/S09.md) | `workflows/tag-queries.md`; query-observer addition to S08 | S05, S08 | High | The same condition can be configured in the Inspector and built in C# |
| [S10](slices/S10.md) | `workflows/tag-manager.md` | S03, S04 | Medium | A user manages a hierarchy through the Tag Manager |
| [S11](slices/S11.md) | `workflows/finding-tagged-assets.md` | S06, S10 | High | A user finds assignments and understands index and scene coverage |
| [S12](slices/S12.md) | `workflows/inspector-tagging.md` | S06, S10 | Medium | A user assigns tags and chooses pill display preferences |
| [S13](slices/S13.md) | `workflows/serialization.md` | S04, S05 | High | Examples distinguish persistent IDs from registry-specific indices |
| [S14](slices/S14.md) | `workflows/code-generation.md` | S03, S04 | High | A user generates and resolves an accessor with its runtime prerequisites |
| [S15](slices/S15.md) | `advanced-topics.md`, `advanced/runtime-and-performance.md` | S05, S09, S13 | High | Runtime costs and fallback behavior are described without unsupported guarantees |
| [S16](slices/S16.md) | `advanced/editor-extensions.md` | S06, S10, S11 | Medium | Minimal examples use supported public editor extension points |
| [S17](slices/S17.md) | `samples.md`, `samples/examples.md` | S07, S09 | Medium | A user can run Examples and recognize expected scene behavior |
| [S18](slices/S18.md) | `samples/stress-test.md` | S15, S17 | Medium | A user can run the stress test and interpret each measured phase |
| [S19](slices/S19.md) | `limitations.md`, `changelog.md`, `migration-guide.md` | S02 through S18 | High | Version availability and compatibility are explained without invented releases or bridges |
| [S20](slices/S20.md) | Integrated editorial, link, build, and API review | S01 through S19 | High | The complete manual is navigable and all verification gaps are accounted for |

Use numeric order by default. If a slice is blocked, another may run only when all its listed dependencies are done. Stay within one slice in the session. An interrupted session resumes its unfinished slice before advancing, unless the state records a genuine external block. Do not quietly expand scope or erase incomplete work to make a slice appear finished.

## Context and session protocol

| Artifact | Owns |
|---|---|
| [Package notes](package-notes.md) | Stable package terminology, source-discovery hints, authoring conventions, entry links, sync cautions |
| This plan | Approved scope, decisions, page ownership, dependencies, completion rules |
| [State](documentation-state.md) | Sole slice-status table, active/next slice, source baseline, blockers, outstanding technical checks |
| [Coverage](documentation-coverage.md) | Feature/type-to-page mapping and source/API verification evidence |
| [Assets](documentation-assets.md) | Screenshot specifications, paths, capture instructions, availability |
| `slices/SXX.md` | Slice instructions and dated execution reports, including exact resume steps |

At session start:

1. Read the repository instructions, required context guides, package notes, state, and selected slice card
2. Check the documentation worktree and locate the package using the lock; verify the source revision and report drift
3. Confirm dependencies and set the selected slice to `in_progress` in the state
4. Read only the source areas relevant to that slice and verify user-visible labels before drafting

At session end:

1. Review the page as a new reader taking the named action, and fix missing prerequisites or ambiguous steps
2. Update navigation and links for the pages actually written
3. Update source evidence in coverage and any image requirements in the asset register
4. Append a dated execution report to the card with changed files, inspected commit/symbols, commands/results, gaps, and next steps
5. Update the state, recording `done`, `blocked`, or the remaining `in_progress` work and the next eligible slice
6. Review and commit all slice changes locally, following the [standing commit authorization](package-notes.md#commit-at-the-end-of-every-slice); report the commit and worktree status without asking for confirmation again

Status values are `planned`, `in_progress`, `blocked`, and `done`. Cards and coverage do not maintain competing slice-status fields. Pending external verification can coexist with editorial completion only when prominently recorded in the state and hand-off; a failed acceptance check must not be hidden as an optional check.

## Verification and completion

For every slice, verify names, signatures, behavior, labels, links, anchors, API UIDs, and image paths against the same inspected source revision. Record source inspection, compilation, metadata generation, and interactive Unity checks separately. Execute meaningful checks once; repeat them after relevant edits or unresolved failures.

- S01 runs the existing toolkit tests because it changes template integration, and proves the layout through an actual DocFX preview
- Compile substantive C# examples in an isolated Unity validation environment when available; do not mutate an existing user's project merely to validate docs
- Check matching direction, null/empty input behavior, missing or incomplete registries, reference counts, observer transitions, and disposal in their owning slices
- Verify each serialization method's actual prerequisites and filtering behavior; do not infer all methods from a broad comment
- Verify codegen naming, regeneration, and runtime resolution; distinguish first-use work from warmed-up evaluation in performance claims
- S20 validates the lock and builds the assembled manual/reference without publishing; release publication and the API comparison spike remain separate work
- Use `IMAGE MISSING` comments and real intended image references as required by the style guide, with a matching register entry; do not create substitute screenshots

The final report separates **editorial completion**, **technical verification**, and **image completion**. All public features and types must map to a manual explanation or generated reference. No public page is left empty, no failed link is silently accepted, and no unexecuted test is reported as passed.

## Known risks and decisions

- The initial source baseline is recorded in the state, not inferred from `package.json` version alone. The manifest says 1.0.0 while the changelog also has Unreleased changes
- Install from the Unity Asset Store as the user-selected primary route. S02 must verify the actual distributed format and sample-import flow. If that evidence is unavailable, block those specific acceptance criteria and proceed only with independent slices
- Treat existing package working notes as leads: some type names, matching implementation descriptions, and serialization prerequisites are stale
- The bridge assembly definitions have no bridge implementation at the baseline. Explain independence and compatibility without promising a future release
- The package manifest currently points to the older documentation host. Record the mismatch as a package follow-up; keep this site's identity from `astra-docs.json`
- Root home, root navigation, and DocFX configuration are template-managed. Reconcile their package customizations after sync; do not change shared instruction files to store authoring state
- Missing screenshots are allowed during text authoring and remain visible in the asset register

Approved scope and choices were established on 2026-10-16. Change this plan only for an explicit scope change or a documented implementation finding that requires a correction; preserve the reason in the affected slice report.
