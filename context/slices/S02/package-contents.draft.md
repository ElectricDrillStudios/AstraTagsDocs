# Package Contents (source-verified draft)

Authoring note: this draft is excluded from the public site. The following inventory describes source commit `88fe1b27669aba87dc1f998dbae3088b19954284`, not a verified Asset Store export. A [public Package Contents page](../../../DocFx/MD/package-contents.md) now describes the maintainer-confirmed planned selection: `Editor/`, `Runtime/`, `Samples~/`, `package.json`, and PDF documentation to be generated later. This internal file remains a source inventory, including folders outside that selection. The maintainer subsequently confirmed pure UPM distribution under Packages with a separate Package Manager sample-import action. Use the public page for current distribution guidance; this file retains source-only inventory for the historical report.

## Runtime

`Runtime/` contains the `com.electricdrill.astra-tags.Runtime` assembly, in the `ElectricDrill.AstraTags` namespace. It provides tag assets, tag sets, the registry, runtime containers, queries, and icon configuration types.

Use the [introduction](../../../DocFx/MD/introduction.md) for the relationships between these components and the [runtime API reference](xref:ElectricDrill.AstraTags) for their signatures.

## Editor tools

`Editor/` contains the editor-only `com.electricdrill.astra-tags.Editor` assembly and its resources. It includes:

- The Tag Manager and hierarchy editing tools
- Inspectors, tag-set and query drawers, tag pills, and the tag picker
- Project settings and registry building
- Tagged-asset indexing, Unity Search integration, and deletion checks
- C# accessor generation
- Icon selection tools and the emoji catalog

The source window is available through `Tools > Astra Tags > Tag Manager`. Its presence is a useful post-installation check once the distributed import route has been verified.

## Samples

The source manifest declares two samples. Each contains runtime scripts and an editor-only scene builder. The source tree contains no prebuilt sample scene; the builders create the scenes and supporting assets.

| Sample | Source directory | Scene builder | Generated scene |
|---|---|---|---|
| Examples | `Samples~/Examples/` | `Tools > Astra Tags > Samples > Build Examples Scene` | `Assets/AstraTagsExamples/AstraTagsExamples.unity` |
| Stress Test | `Samples~/StressTest/` | `Tools > Astra Tags > Samples > Build Stress Test Scene` | `Assets/AstraTagsStressTest/AstraTagsStressTest.unity` |

Examples creates a small tag hierarchy, a registry, and a demonstration GameObject. Stress Test creates a preset and a GameObject with a runner and an on-screen HUD.

These generated locations are defined by the builders; they are not evidence of the sample scripts' installation location. The Asset Store sample delivery/import mechanism remains to be checked.

## Conditional bridge definitions

`Bridge/` contains conditional runtime and editor assembly definitions for Astra Framework. No implementation is present at the inspected revision. This directory does not provide automatic conversion or interoperability between the packages' tag types.

## Source-only files to review during packaging

The source root also contains `package.json`, `CHANGELOG.md`, maintainer instructions, and `Tools~/generate-emoji-data.py`. The Python script generates emoji catalog data and is not referenced by the runtime, editor, or sample assembly definitions. Confirm which of these files are included in the final artifact before describing them as delivered package content.
