# Documentation state

This is the sole source of slice status. Read it with the [plan](documentation-plan.md), [package notes](package-notes.md), and selected slice card before authoring.

## Current hand-off

- Last updated: 2026-10-16
- Active slice: none
- Next slice: [S03](slices/S03.md) (creating tags); S02 distribution questions are resolved by the maintainer-confirmed pure UPM route and separate Package Manager sample import
- Editorial progress: 2 of 20 slices done; all three S02 pages (Requirements, Package Contents, Installation Instructions) are authored, source/flow checked, and linked from manual navigation and the home; installation is also linked from the introduction
- Technical verification: final S02 DocFX build passed (0 warnings/errors); 37 Markdown files and 24 HTML pages passed local link/resource/anchor checks, reusing unchanged S01 API metadata. The UPM flow is supported by maintainer evidence and Unity 6.2 guidance; actual product installation/sample import remain an unexecuted release check. See the [completion report](slices/S02.md#upm-completion-report-2026-10-16)
- Images: no screenshots required by S01 or any S02 page; no S02 missing-image placeholders. Future captures remain in the [asset register](documentation-assets.md)

## Source baseline

| Field | Evidence |
|---|---|
| Inspected commit | `88fe1b27669aba87dc1f998dbae3088b19954284` |
| Local ref comparison | Checkout HEAD, `main`, and `origin/main` resolve to the same commit |
| Source worktree | Clean when S02 inspected it; no revision drift from S01 |
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
| S03 | planned | [Creating tags](slices/S03.md) |
| S04 | planned | [Configuration and registry](slices/S04.md) |
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

Append precise verification gaps here as they occur. Do not mark a slice blocked just because its future prerequisites have not yet been scheduled.

## Latest verification evidence

S02 completion (2026-10-16): DocFX 2.78.5 build passed with warnings treated as errors (0 warnings, 0 errors); 37 Markdown files and 24 HTML pages passed local link/resource/anchor checks. All three S02 pages render under `MD/`, resolve in manual navigation/home links, and installation is linked from the introduction. Context, archived drafts, operational pages, private-source markers, and duplicate `DocFx/MD/` output remain excluded. The source revision was reinspected and matches S01; its existing API metadata was reused. No actual product install/sample import, new compilation/metadata generation, toolkit test rerun, sample execution, release-host build, publication, PDF generation, or remote fetch was performed.

The following S01 foundation checks remain prior evidence:

- Toolchain: .NET SDK 8.0.131, DocFX 2.78.5, Unity 6000.2.10f1 CoreModule references; source copied into an isolated temporary project with editor conditionals excluded
- Runtime compilation: succeeded with 0 errors; 3 CS0649 warnings for Unity-serialized fields and the CS0419 XML warning above
- API metadata: generated from the restored isolated source project with `--noRestore --warningsAsErrors`, 0 warnings and 0 errors; 16 namespace/type UIDs in the coverage inventory resolve, including the nested enumerator; internal opcode excluded
- DocFX HTML: built with `--warningsAsErrors`, 0 warnings and 0 errors; all 21 HTML pages and 445 local links/resources/anchors checked
- Layout and isolation: home, manual, API, and logo paths verified; no duplicate source-prefixed manual, context/operational pages, or checked private-source markers in the output
- Markdown: all 30 repository Markdown files checked for local file links and one title outside code examples; 20 slice cards present
- No Unity GUI/play-mode workflow, release-host build, release API comparison, publication, or remote source fetch was performed

The API template hook fixes an observed DocFX link to the nonexistent parent namespace page. Future DocFX upgrades must retain or reverify this correction. Temporary preview artifacts are disposable and are not part of the public repository.
