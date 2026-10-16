# Documentation state

This is the sole source of slice status. Read it with the [plan](documentation-plan.md), [package notes](package-notes.md), and selected slice card before authoring.

## Current hand-off

- Last updated: 2026-10-16
- Active slice: none
- Next slice: [S05](slices/S05.md) (tag sets)
- Editorial progress: 4 of 20 slices done; S04's Package Configuration and the Registry guide covers editor settings, resource creation, reconciliation, runtime resolution, lookup APIs and recovery, with navigation and entry links
- Technical verification: S04 DocFX build succeeded (0 errors; exactly 4 registered missing-image warnings across S03/S04); 39 Markdown files and 26 HTML pages checked for local links/resources/anchors, allowing only those four images. Both final C# examples compiled with 0 warnings/errors; all five distinct page xrefs resolve in unchanged S01 metadata, with all 16 runtime C# files matching its input byte for byte. See the [S04 report](slices/S04.md#execution-report-2026-10-16)
- Images: IMG03-01/02 and IMG04-01/02 are missing with marked public references and [register entries](documentation-assets.md); no screenshots were captured. S01 and S02 need none
- Source findings: F05/F06 remain open from S03; no GUI reproduction or package fix was performed. S04 checked one-shot Active resolution and the editor/runtime registry distinction without executing Unity lifecycle/resource checks; the public builder result's internal properties are flagged for S16 in coverage
- Session convention: each slice ends with a local commit under the maintainer's [standing authorization](package-notes.md#commit-at-the-end-of-every-slice), after checks and hand-off updates

## Source baseline

| Field | Evidence |
|---|---|
| Inspected commit | `88fe1b27669aba87dc1f998dbae3088b19954284` |
| Local ref comparison | Checkout HEAD, `main`, and `origin/main` resolve to the same commit |
| Source worktree | Clean when S04 inspected it; no revision drift from S01 |
| Manifest version | 1.0.0 |
| Release availability | The source changelog includes Unreleased changes; commit coverage does not establish release availability |
| Lock selection | Read `release-lock.yml`; the current branch ref can advance between sessions |
| Remote freshness | No network fetch was performed; remote head was not independently verified |

Do not copy a local checkout path into this public file. Recheck source drift at the start of each session and identify which coverage rows need another review.

## Slice status

| Slice | Status | Execution report |
|---|---|---|
| S01 | done | [Foundation](slices/S01.md) |
| S02 | done | [Installation and contents](slices/S02.md) |
| S03 | done | [Creating tags](slices/S03.md) |
| S04 | done | [Configuration and registry](slices/S04.md) |
| S05 | planned | [Tag sets](slices/S05.md) |
| S06 | planned | [Custom tagged assets](slices/S06.md) |
| S07 | planned | [Runtime containers](slices/S07.md) |
| S08 | planned | [Events and observers](slices/S08.md) |
| S09 | planned | [Boolean queries](slices/S09.md) |
| S10 | planned | [Tag Manager](slices/S10.md) |
| S11 | planned | [Finding tagged assets](slices/S11.md) |
| S12 | planned | [Inspector tagging](slices/S12.md) |
| S13 | planned | [Serialization](slices/S13.md) |
| S14 | planned | [Code generation](slices/S14.md) |
| S15 | planned | [Runtime model and performance](slices/S15.md) |
| S16 | planned | [Editor extensions](slices/S16.md) |
| S17 | planned | [Examples sample](slices/S17.md) |
| S18 | planned | [Stress Test sample](slices/S18.md) |
| S19 | planned | [Limitations and versions](slices/S19.md) |
| S20 | planned | [Integrated review](slices/S20.md) |

## Open dependencies and follow-ups

| ID | Owner | Condition and required next action |
|---|---|---|
| V01 | Release verification | Authoring questions resolved: pure UPM through the new Unity publisher portal, visible under Packages, with separate Package Manager sample import; contents confirmed by the maintainer. When the actual release artifact is available, install it in a disposable compatible project, run the documented tag/editor checks, import both samples, and verify compilation and builder menus. These interactive checks were not executed during authoring and remain explicit release evidence to collect |
| V02 | S19 | Resolve the difference between manifest version and Unreleased changes before assigning version-availability labels |
| V03 | S20 | Recheck source drift and runtime API/member coverage for the assembled manual. S01 checked 307 isolated metadata UIDs (including all authored xrefs); release-host generation and API comparison remain outside this milestone |
| F01 | Package maintainer | The package manifest's documentation/changelog URLs use the older host. Record a source-repository follow-up rather than editing private package code here |
| F02 | All sessions | Restore or reconcile customized home, navigation, and DocFX mappings after any template sync |
| F03 | Package maintainer | Isolated runtime compilation reports CS0419 for the ambiguous XML cref `Resources.Load` in `TagRegistry.Active`. Correct the XML in package source separately; S01 metadata and site builds pass with warnings treated as errors |
| F04 | Package maintainer | After the manual and API documentation are complete, generate their PDF documentation and include it in the UPM release as requested. Filename/location remain undecided; no PDF has been generated and this does not block S02 authoring |
| F05 | Package maintainer | S03 source inspection found reversed calls to `WouldCycleWithParent` in `TagInspectorSections.ShowParentMenu` and `SetParent`: valid ancestors can be hidden and invalid descendants offered; `GameTagSO.OnValidate` clears a cyclic parent to root. Verify in Unity and correct the call direction in package source with regression coverage. The guide documents the root-first workaround for an omitted ancestor and warns against choosing descendants; no GUI reproduction or package fix was executed |
| F06 | Package maintainer | Inspector reparenting skips `TagNamingPolicy.ValidateInHierarchy`, and direct Project-window creation/rename does not use the same enforcement as package creation/rename actions. Check sibling/root name uniqueness after imports and reparenting; assess consistent enforcement in package source. The S03 guide distinguishes policy, trimming, checked actions and advisory validation; no package fix was executed |

Append precise verification gaps here as they occur. Do not mark a slice blocked just because its future prerequisites have not yet been scheduled.

## Latest verification evidence

S04 (2026-10-16): source revision unchanged; inspected registry/runtime lookup and editor configuration/reconciliation implementations and relevant test source (not executed). Both final C# examples compile against the unchanged S01 runtime assembly and Unity 6000.2.10f1 CoreModule using .NET SDK 8.0.131 / netstandard2.1, with 0 warnings/errors. Five distinct S04 xrefs resolve in S01 metadata; all 16 runtime C# files match its source snapshot. DocFX 2.78.5 build succeeded with 0 errors and exactly 4 `InvalidFileLink` warnings matching the two missing captures each from S03 and S04. The audit checked all local links/anchors in 39 Markdown files and 527 local links/resources/anchors across 26 HTML pages, allowing only those four registered images and checking their page comments/register entries. New workflow URL, navigation/entry links, titles and output exclusions passed. No Unity GUI/play-mode/test/resource-loading execution, screenshot capture, new runtime compilation/metadata generation, release-host build, publication, toolkit test rerun or remote fetch was performed. V01 continues to own interactive registry/setup verification in the release artifact; local commits are now part of every slice's completion protocol.

S03 (2026-10-16): source revision unchanged; inspected identity/hierarchy/naming/icon/gradient implementation and exact editor labels. All 16 runtime C# files match the S01 metadata snapshot; four new xrefs resolve among its 307 UIDs. DocFX 2.78.5 build succeeded with 0 errors and exactly 2 `InvalidFileLink` warnings matching IMG03-01/IMG03-02. The audit checked 38 Markdown files (178 local links/anchors) and 25 HTML pages (504 local links/resources/anchors), allowing only the two registered missing screenshots and confirming their comments/register entries. Navigation, expected workflow URL, titles and output exclusions passed. No new compilation/metadata generation, Unity GUI/test execution, screenshot capture, toolkit test rerun, release-host build, publication or remote fetch was performed. F05/F06 are source findings awaiting package-side verification/correction, not executed regression tests.

S02 completion remains prior evidence: its DocFX build passed with warnings treated as errors (0 warnings/errors), and 37 Markdown files / 24 HTML pages passed local link/resource/anchor checks. All three S02 pages render under `MD/` and are linked from navigation/home; installation is also linked from the introduction. Maintainer evidence and Unity 6.2 guidance support pure UPM installation and separate sample import; actual product installation/sample import remain unexecuted release checks. No PDF was generated.

The following S01 foundation checks remain prior evidence:

- Toolchain: .NET SDK 8.0.131, DocFX 2.78.5, Unity 6000.2.10f1 CoreModule references; source copied into an isolated temporary project with editor conditionals excluded
- Runtime compilation: succeeded with 0 errors; 3 CS0649 warnings for Unity-serialized fields and the CS0419 XML warning above
- API metadata: generated from the restored isolated source project with `--noRestore --warningsAsErrors`, 0 warnings and 0 errors; 16 namespace/type UIDs in the coverage inventory resolve, including the nested enumerator; internal opcode excluded
- DocFX HTML: built with `--warningsAsErrors`, 0 warnings and 0 errors; all 21 HTML pages and 445 local links/resources/anchors checked
- Layout and isolation: home, manual, API, and logo paths verified; no duplicate source-prefixed manual, context/operational pages, or checked private-source markers in the output
- Markdown: all 30 repository Markdown files checked for local file links and one title outside code examples; 20 slice cards present
- No Unity GUI/play-mode workflow, release-host build, release API comparison, publication, or remote source fetch was performed

The API template hook fixes an observed DocFX link to the nonexistent parent namespace page. Future DocFX upgrades must retain or reverify this correction. Temporary preview artifacts are disposable and are not part of the public repository.
