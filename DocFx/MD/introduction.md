# Introduction

Astra Tags is a standalone hierarchical tagging system for Unity. A tag represents a category or state defined by the project, such as a damage type, an ability category, or a temporary gameplay condition. Tags are reusable ScriptableObject assets that can be assigned to different objects.

The package combines runtime matching with editor tools for creating, assigning, and finding tags. Astra Framework and Odin Inspector are not required.

Follow [Installation Instructions](installation-instructions.md) to install the UPM package and import its optional samples.

## Astra Tags vocabulary

### Tag

A [GameTagSO](xref:ElectricDrill.AstraTags.GameTagSO) defines a single tag. It stores a stable identifier, an optional parent, a description, and visual properties such as color and icon.

The same tag asset can be referenced by many objects. Its meaning comes from the systems that use it. For example, a `State.Stunned` tag does not disable movement on its own; movement logic checks for the tag and decides how to respond.

### Hierarchy and full path

Each tag can have one parent. A root tag has no parent, and a project can contain multiple independent roots.

The full path joins the names along the parent chain with dots. For example, `Damage.Fire.Burn` describes a `Burn` tag whose parent is `Fire`, with `Damage` as the root. The hierarchy is defined by the parent references; the full path is computed from them.

Hierarchical matching follows that relationship upwards. Holding a child satisfies a question about one of its ancestors. Holding an ancestor does not imply that a particular child is present.

For a tag set containing only `Damage.Fire.Burn`:

| Question | Result |
|---|---|
| Does it contain `Damage.Fire.Burn`? | Yes |
| Does it contain `Damage.Fire` hierarchically? | Yes |
| Does it contain `Damage` hierarchically? | Yes |
| Does it contain `Damage.Fire` exactly? | No |
| Does it contain a sibling such as `Damage.Ice`? | No |

The inferred ancestors are matching results. They are not additional entries inserted into the set.

### Stable identifier and runtime index

A tag's stable identifier survives asset renames. Use stable identifiers when referring to tags in persistent data that must remain meaningful across builds.

A runtime index is assigned by a [TagRegistry](xref:ElectricDrill.AstraTags.TagRegistry). It identifies a tag within a particular registry build and supports compact serialization and matching masks. Keep index-based data tied to the registry build that produced it.

### Tag set

A [TagSet](xref:ElectricDrill.AstraTags.TagSet) is a serializable collection of distinct tag references. It can be embedded in a ScriptableObject, MonoBehaviour, or serializable class.

A set supports both exact membership checks and hierarchical matching. It also supports questions about whether any, all, or none of a group of tags are satisfied. Follow [Tag Sets and Matching](workflows/tag-sets.md) for construction, expected results, and collection operations.

### Runtime container

A runtime container tracks how many sources currently grant a tag. If two effects both grant `State.Stunned`, ending one effect leaves the tag active until the other effect also releases it.

[TagCountContainer](xref:ElectricDrill.AstraTags.TagCountContainer) provides this behavior in plain C#. [TagContainer](xref:ElectricDrill.AstraTags.TagContainer) exposes it as a MonoBehaviour with authored initial tags. Both provide events and observers for reacting to changes.

### Tag query

A [TagQuery](xref:ElectricDrill.AstraTags.TagQuery) combines tag conditions into a boolean expression. Conditions can require all, any, or none of their tags, and groups can combine or negate other conditions.

For example, an ability might require a tag under `Ability.Magic` and reject a tag under `State.Silenced`. The query describes the condition; the gameplay system decides what a match permits.

## How the package fits together

### Author tags and assign them to objects

Follow [Creating and Organizing Tags](workflows/creating-tags.md) to build a hierarchy and configure tag identity and appearance. Create tag assets from `Astra Tags > Tag` in Unity's asset creation menu. Use `Tools > Astra Tags > Tag Manager` to work with the hierarchy, edit selected tags, and inspect tagged assets.

Objects expose a [TagSet](#tag-set) to store their tags. Implementing [ITagged](xref:ElectricDrill.AstraTags.ITagged) gives the package's editor tools a common way to discover those tags. Use a [TagContainer](#runtime-container) when a GameObject needs tags that multiple gameplay sources can add and release.

### Configure the registry

The registry lists the project's registered tags and derives runtime lookups, indices, and ancestor masks. The active registry normally loads from `Resources/AstraTags/TagRegistry`.

The registry selected in the editor settings steers editor tooling. A runtime registry must also be available to the running game; selecting one in Project Settings alone does not provide that resource.

Follow [Package Configuration and the Registry](workflows/package-configuration.md) to create the resource, reconcile its tag list and verify runtime lookups.

When no active registry is available, tag-set matching can follow parent references instead. The registry also supports identifier resolution and generated C# accessors, so configuring it remains part of setting up a project.

### Evaluate gameplay conditions

Use a tag set to answer questions about assigned categories. Use a runtime container when independent sources grant the same state. Use a query when the decision combines several conditions.

Exact membership and hierarchical matching serve different purposes. For example, checking whether `Damage.Fire` is stored explicitly is different from accepting any tag beneath `Damage.Fire`.

### Find and maintain tagged assets

The Tag Manager and the `tag:` Unity Search provider help locate tagged project assets. Inspector controls display tags and provide a hierarchy-aware picker for assigning them.

Asset discovery uses an editor index. Runtime state and indexed project assets have different lifecycles; a tag added temporarily during gameplay does not become a saved asset assignment.

## Relationship to other tag systems

Astra Tags stores tag assets and tag sets independently of Unity's built-in GameObject tags. It does not replace or change a GameObject's built-in tag.

Astra Framework 2.x also contains its own Game Tags. Those types and collections are separate from Astra Tags. Sharing a similar name does not make their references interchangeable, and the package does not currently provide an automatic bridge between them.

## API reference

Use the [runtime API reference](xref:ElectricDrill.AstraTags) for type definitions, signatures, and member documentation. The conceptual distinctions above apply throughout the reference: tag assets define meaning, sets describe membership, containers track grants, and queries evaluate conditions.
