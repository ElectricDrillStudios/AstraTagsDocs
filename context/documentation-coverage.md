# Documentation coverage

Map every public capability and type to an explanation or generated runtime reference. Planned page paths are plain code, not links to nonexistent files. Slice status lives only in the [state](documentation-state.md).

## Evidence conventions

- **Assigned**: destination and owning slice are known, but its detailed explanation has not been checked
- **Overview checked**: the introduction's limited conceptual claims were checked against source; this does not complete the owning workflow
- **Source checked**: the owning page's claims and examples were verified against the named source commit
- **Metadata checked**: the UID resolves in metadata generated from the documented source; distinguish isolated/local generation from a release-host build
- **Compiled / Unity checked**: record the actual snippet or procedure, environment, and result in the slice report

The baseline commit is recorded in the state. Below, `S01 baseline` means that exact commit. Paths in the Source column are relative to the package checkout, not this repository.

## Capability coverage

All destination paths are beneath `DocFx/MD/` unless stated otherwise.

| Capability or public surface | Destination | Owner | Source to verify | Evidence |
|---|---|---|---|---|
| Package purpose, vocabulary, matching direction | [Introduction](../DocFx/MD/introduction.md), root home | S01 | Manifest; `Runtime/GameTagSO.cs`, `TagSet.cs`, `TagRegistry.cs`, `TagCountContainer.cs`, `TagContainer.cs`, `TagQuery.cs`, `ITagged.cs`; relevant editor menu/settings/codegen paths and bridge assembly definitions | Overview and all authored xrefs checked at S01 baseline; isolated DocFX build and HTML link audit passed; see S01 report |
| Minimum Unity version, dependencies, install, sample import | [Requirements](../DocFx/MD/requirements.md), [Installation Instructions](../DocFx/MD/installation-instructions.md) | S02 | Manifest; runtime/editor/sample assembly definitions; maintainer-confirmed pure UPM distribution; Unity 6.2 UPM/sample guides | Source checked at the unchanged S01 baseline; maintainer confirmed Packages location and separate sample import; public procedure, prerequisites, success checks, and navigation complete; DocFX/link verification recorded in the [completion report](slices/S02.md#upm-completion-report-2026-10-16); no published-product installation or Unity sample import was executed |
| Important package directories and shipped content | [Package Contents](../DocFx/MD/package-contents.md) | S02 | Package tree, sample definitions/builders, and maintainer-confirmed UPM content selection | Source checked at the unchanged S01 baseline; public page describes selected Editor/Runtime/Samples~/manifest content, logical Packages location, and future PDF documentation; actual release artifact inspection/PDF generation remain release follow-ups |
| Tag identity, hierarchy, full path, stable ID, names, cycles | [Creating and Organizing Tags](../DocFx/MD/workflows/creating-tags.md) | S03 | `Runtime/GameTagSO.cs`; `Editor/TagNamingPolicy.cs`, `Editor/Tags/TagInspectorSections.cs`, `Editor/Windows/TagTextPrompt.cs`, `Editor/Windows/TagHierarchyView.cs` | Source checked at the unchanged S01 baseline; reproducible four-tag hierarchy, checked-action versus advisory name rules, trimmed/internal whitespace, case-insensitive sibling uniqueness, stable-ID regeneration, and cycle fallback documented. Reversed Inspector parent checks and unchecked reparenting collisions recorded in state F05/F06; no Unity interaction executed |
| Color, gradient, emoji/sprite icon authoring | [Creating and Organizing Tags](../DocFx/MD/workflows/creating-tags.md#configure-appearance) | S03 | `Runtime/TagIcon.cs`, `TagIconKind.cs`, `GradientDirection.cs`; `Editor/Tags/TagInspectorSections.cs`, `Editor/Icons/TagIconPicker.cs`, `Editor/Icons/TagIconResolver.cs` | Source checked at the unchanged S01 baseline; defaults, exact labels, gradient directions, emoji controls, sprite GUID/editor-only resolution and sub-sprite limitation checked. Four page API xrefs resolve in unchanged S01 metadata; DocFX/link audit passed apart from two registered missing captures; see [S03 report](slices/S03.md#execution-report-2026-10-16) |
| Settings, editor registry, runtime resource, rebuild and lookup | [Package Configuration and the Registry](../DocFx/MD/workflows/package-configuration.md) | S04 | `Runtime/TagRegistry.cs`; `AstraTagsSettings`/provider, `TagRegistryBuilder`, `TagRegistryBuildResult`, `TagRegistryEditor`, `TagCatalog`, Tag Manager; registry/builder/signature tests | Source checked at the unchanged S01 baseline; defaults, resource creation, editor/runtime selection, one-shot Active resolution (including null assignment and editor resets), reconciliation versus derived rebuild, case-sensitive lookups and failure values verified. Two final C# examples compiled against the unchanged runtime assembly and Unity 6000.2.10f1 CoreModule (0 warnings/errors); five distinct xrefs resolve in S01 metadata. DocFX/link audit passed apart from four registered missing captures across S03/S04; see [S04 report](slices/S04.md#execution-report-2026-10-16). No Unity interaction or tests executed |
| Exact/hierarchical matching; Any/All/None; null/empty inputs | `workflows/tag-sets.md` | S05 | `Runtime/TagSet.cs`; matching tests | Assigned |
| Mutation, ordering, enumeration, equality and normalization | `workflows/tag-sets.md` | S05 | `Runtime/TagSet.cs`; mutation and serialization tests | Assigned |
| Custom tagged ScriptableObjects/components and discovery | `workflows/taggable-assets.md` | S06 | `Runtime/ITagged.cs`; header injector and index discovery | Assigned |
| Runtime grants, counts, initial tags, lifecycle and live view | `workflows/runtime-containers.md` | S07 | `Runtime/TagContainer.cs`, `TagCountContainer.cs`; lifecycle tests | Assigned |
| Event timing, count/presence distinction, tag observation and disposal | `workflows/events-and-observers.md` | S08 | `Runtime/TagCountContainer.cs`, `TagContainer.cs`; event/observer tests | Assigned |
| Query observation | `workflows/events-and-observers.md` | S09 | Query observer paths and tests; expand the existing S08 page | Assigned |
| Query drawer, builder, All/Any/None, groups, negation, empty inputs | `workflows/tag-queries.md` | S09 | `Runtime/TagQuery.cs`, `TagQueryNode.cs`, enums; query drawer and tests | Assigned |
| Query-source interface, domain marker interfaces | `workflows/tag-queries.md` | S09 | `Runtime/ITagQuerySource.cs` and implementing containers | Assigned; listed under Unreleased in source changelog |
| Manager hierarchy operations, filters, shortcuts and bulk edits | `workflows/tag-manager.md` | S10 | Manager window, hierarchy view/model, inspector pane | Assigned |
| Asset index, ANY/ALL, descendants, scene limits, cancellation | `workflows/finding-tagged-assets.md` | S11 | Index, asset pane, settings provider and index tests | Assigned |
| Unity Search provider and safe delete | `workflows/finding-tagged-assets.md` | S11 | Search provider, asset modification processor | Assigned |
| Inspector header, pill modes, picker, reorder, bulk removal, preferences | `workflows/inspector-tagging.md` | S12 | Header injector, set drawer, multi-select popup, pills and preferences | Assigned |
| ID/index serialization, resolution, unknown values, registry requirements | `workflows/serialization.md` | S13 | `Runtime/TagSet.cs`; serialization tests | Assigned; check `ToIdArray()` independently of loading methods |
| Generated accessors, settings, name sanitization, changes and resolution | `workflows/code-generation.md` | S14 | Code generator/postprocessor and settings | Assigned |
| Masks, signatures, rebuilds, fallback, first use and steady state | `advanced/runtime-and-performance.md`, `advanced-topics.md` | S15 | Runtime implementations, allocation/equivalence tests | Assigned; do not repeat stale constant-time claims |
| Public registry rebuild/result, row decoration and pill drawing | `advanced/editor-extensions.md` | S16 | Public editor types, their actual access modifiers and call sites | Assigned; S04 checked the builder entry point and found that the public `TagRegistryBuildResult` type's properties are internal. Recheck the usable extension surface before writing result-consumption examples; no editor UIDs assumed in runtime metadata |
| Examples import, builder, output assets, controls and expected behavior | `samples.md`, `samples/examples.md` | S17 | Manifest; `Samples~/Examples/` | Assigned |
| Stress Test fixture, preset, measurements, HUD and report | `samples/stress-test.md` | S18 | `Samples~/StressTest/` | Assigned |
| Limitations, bridge status, version availability, migration and changelog | `limitations.md`, `migration-guide.md`, `changelog.md` | S19 | Current implementation, source changelog, bridge assemblies and release evidence | Assigned |
| Whole-manual links, API coverage, examples, navigation and registers | Entire site and all context registers | S20 | Assembled DocFX inputs/output and source baseline | Assigned |

## Runtime API type inventory

All UIDs in this inventory were confirmed against metadata generated from the S01 baseline in an isolated source project (.NET SDK 8.0.131, netstandard2.1, Unity 6000.2.10f1 CoreModule references, no editor conditional). Generation used DocFX 2.78.5 with warnings treated as errors and succeeded with no warnings or errors. The namespace plus 15 public type UIDs resolve; 307 total UIDs were generated, and every xref authored by S01 resolves. This is local source-metadata evidence, not a release-host build or host-versus-isolated comparison. See the [S01 report](slices/S01.md#execution-report-2026-10-16).

Constructors, public/protected members, overloads, enum values, and nested public types must also receive the complete explanation/coverage review in S20; confirming type UIDs does not complete their owning workflow slices.

| UID beneath `ElectricDrill.AstraTags` | Explanation owner | API evidence |
|---|---|---|
| `GameTagSO` | S03 | Identity, hierarchy and visual workflow source checked in S03; type UID resolves in unchanged S01 metadata |
| `TagRegistry` | S04 | Settings/registry workflow source checked in S04; type and Active/Rebuild/Signature member UIDs resolve in unchanged S01 metadata; lookup and explicit initialization examples compiled in isolation |
| `TagSet` and `TagSet.Enumerator` | S05 | Source declarations confirmed |
| `ITagged` | S06 | Source declaration confirmed |
| `TagContainer` | S07, S08 | Source declaration confirmed |
| `TagCountContainer` | S07, S08 | Source declaration confirmed |
| `TagQuery` | S09 | Source declaration confirmed |
| `TagQueryNode` | S09 | Source declaration confirmed |
| `TagQueryMode` | S09 | Source declaration confirmed |
| `TagQueryConnective` | S09 | Source declaration confirmed |
| `ITagQuerySource` | S09 | Source declaration confirmed; release availability pending |
| `TagIcon` | S03 | Visual authoring explanation source checked in S03; type UID resolves in unchanged S01 metadata |
| `TagIconKind` | S03 | Visual authoring explanation source checked in S03; type UID resolves in unchanged S01 metadata |
| `GradientDirection` | S03 | Visual authoring explanation source checked in S03; type UID resolves in unchanged S01 metadata |

`TagQueryOpCode` is internal at the baseline and is not a public API target. Do not add internal implementation types to the public reference merely to satisfy an inventory.

The HTML audit also checked namespace navigation: the local template hook resolves the entire `ElectricDrill.AstraTags` namespace as one xref, avoiding DocFX's otherwise broken link to an empty parent namespace.

## External follow-ups

Record source XML inaccuracies, release ambiguity, missing distributed-installation evidence, and manifest URL mismatches in the state and owning slice report. Do not copy private source, publish local checkout paths, or edit generated metadata to work around a source defect.
