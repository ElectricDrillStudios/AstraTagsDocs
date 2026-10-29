# Package Contents

Astra Tags includes the runtime tagging system, editor tools for working with tags, and two optional samples. The main parts of the package are described below, with links to the guides that explain how to use them.

## Main package subsystems

| Subsystem | What it provides | Learn more |
|---|---|---|
| Tag assets and hierarchies | Reusable tags with parent relationships, stable identities, descriptions, and visual settings | [Creating and Organizing Tags](workflows/creating-tags.md) |
| Tag sets | Collections of tag references, with exact and hierarchical matching and set operations | [Tag Sets and Matching](workflows/tag-sets.md) |
| Runtime containers | Reference-counted tags for gameplay states granted by multiple sources, with events and observers for changes | [Runtime container](introduction.md#runtime-container) |
| Boolean queries | Conditions that combine tag requirements, alternatives, and exclusions | [Tag query](introduction.md#tag-query) |
| Registry and configuration | The registry that lists the project's tags so the package can look them up quickly, plus settings for the editor tools | [Package Configuration and the Registry](workflows/package-configuration.md) |

## Editor tools

The Tag Manager provides a shared window for organizing the hierarchy, editing tags, and finding tagged assets. Inspector controls let you assign tags and recognize them by their colors and icons. Implement [`ITagged`](xref:ElectricDrill.AstraTags.ITagged) to use these tools with [your own assets and components](workflows/taggable-assets.md).

Open the Tag Manager through `Tools > Astra Tags > Tag Manager`.

## Samples and documentation

The package includes two optional samples:

- **Examples**: a gameplay demo with a tag hierarchy, a runtime container, and a query-based immunity check
- **Stress Test**: benchmarks for registry building and tag matching, with on-screen results and a JSON report

See [Import samples](installation-instructions.md#import-samples) to import either sample and build its scene.

