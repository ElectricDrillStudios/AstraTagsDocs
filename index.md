---
_layout: landing
---

# Astra Tags

Astra Tags is a standalone hierarchical tagging system for Unity. Define reusable tags as `ScriptableObject` assets, assign them to your own objects, and use their hierarchy to answer gameplay questions.

For example, a tag set containing `Damage.Fire.Burn` also matches `Damage.Fire` and `Damage`. Combine tags into boolean queries, track tags granted by multiple gameplay sources, and react when a condition changes.

## Documentation

- [Installation Instructions](DocFx/MD/installation-instructions.md): install the UPM package and import its optional samples
- [Introduction](DocFx/MD/introduction.md): learn the vocabulary, matching model, and main package components
- [Creating and Organizing Tags](DocFx/MD/workflows/creating-tags.md): create a hierarchy and configure tag names, stable identity, and visuals
- [Package Configuration and the Registry](DocFx/MD/workflows/package-configuration.md): set up the registry that lists your project's tags so the running game can find them
- [Tag Sets and Matching](DocFx/MD/workflows/tag-sets.md): choose exact or hierarchical checks and modify stored assignments
- [Integrating Custom Tagged Assets](DocFx/MD/workflows/taggable-assets.md): expose serialized tags on custom assets and components to the editor tools
- [Requirements](DocFx/MD/requirements.md): check the minimum Unity version and package dependencies
- [Package Contents](DocFx/MD/package-contents.md): locate the runtime, editor tools, samples, and planned offline documentation
- [API reference](xref:ElectricDrill.AstraTags): look up runtime types and members

## Package features

- **Hierarchical tags:** organize tag assets into parent and child relationships, with stable identifiers and configurable Inspector visuals
- **Tag sets and queries:** match individual tags, groups of tags, or boolean expressions
- **Runtime containers:** retain a tag while one or more sources grant it, and observe changes in its presence
- **Editor tools:** author tags in the Tag Manager, assign them in Inspectors, and find tagged assets
- **Persistence and code generation:** serialize tag identifiers or registry indices, and optionally generate C# accessors
- **Samples:** explore a gameplay example and a configurable stress test

Astra Tags works independently of Astra Framework and does not require Odin Inspector.

## Support

For questions, feedback, or bug reports, contact [Electric Drill](mailto:electricdrill.info@gmail.com).
