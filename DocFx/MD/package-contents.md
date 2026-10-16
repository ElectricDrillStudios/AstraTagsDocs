# Package Contents

The planned Asset Store UPM release includes the runtime, editor tools, both samples, the package manifest, and PDF documentation for the manual and runtime API. The PDF will be prepared after the documentation is complete.

The package appears under **Packages > Astra Tags** in the Project window. The paths below are relative to its package root. See [Installation Instructions](installation-instructions.md) to install it and import the optional samples.

| Content | Purpose |
|---|---|
| `Runtime/` | Tag assets, tag sets, the registry, runtime containers, boolean queries, and icon configuration |
| `Editor/` | Tag authoring, assignment, discovery, settings, registry building, and code generation tools |
| `Samples~/Examples/` | Gameplay example scripts and an editor scene builder |
| `Samples~/StressTest/` | Benchmark scripts, configuration, an on-screen HUD, reporting, and an editor scene builder |
| `package.json` | Package identity, version, minimum Unity version, and sample declarations |
| PDF documentation | Offline manual and runtime API documentation; filenames and locations will be set when the PDF is generated |

See [Requirements](requirements.md) for the minimum Unity version and dependencies, and the [introduction](introduction.md) for the relationship between the runtime components.

## Runtime

The runtime assembly is `com.electricdrill.astra-tags.Runtime`, with types in the `ElectricDrill.AstraTags` namespace. Use the [runtime API reference](xref:ElectricDrill.AstraTags) for type definitions and signatures.

## Editor tools

The editor-only assembly is `com.electricdrill.astra-tags.Editor`. Its content includes:

- The Tag Manager and hierarchy editing tools
- Tag Inspectors, tag-set and query drawers, tag pills, and the hierarchical picker
- Project settings and registry building
- Tagged-asset indexing, Unity Search integration, and deletion checks
- C# accessor generation
- Icon selection tools and the emoji catalog

Open the main authoring window through `Tools > Astra Tags > Tag Manager`.

## Samples

Both samples contain runtime scripts and an editor scene builder. The scene builders generate scenes and supporting assets; the source sample folders do not contain prebuilt scenes.

| Sample | Scene-builder menu | Generated scene |
|---|---|---|
| Examples | `Tools > Astra Tags > Samples > Build Examples Scene` | `Assets/AstraTagsExamples/AstraTagsExamples.unity` |
| Stress Test | `Tools > Astra Tags > Samples > Build Stress Test Scene` | `Assets/AstraTagsStressTest/AstraTagsStressTest.unity` |

The generated scene paths are separate from the location where the sample scripts are installed. Save the current scene before running either builder: both create a new scene in single-scene mode.

The samples in `Samples~` remain inactive until imported through the Package Manager. Follow [Import samples](installation-instructions.md#import-samples) to copy either sample into `Assets` and make its scene-builder menu available.
