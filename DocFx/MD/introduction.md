# Introduction

Astra Tags is a standalone hierarchical tagging system for Unity. A tag is a label you define for your project and attach to things in your game: a damage type, a class such as warrior, or a temporary condition such as being stunned. Tags are reusable `ScriptableObject` assets, so the same tag can be assigned to as many objects as you like.

A tag does nothing on its own. Its meaning comes entirely from the logic that looks for it, which is why tags can represent **anything**. Tags are also hierarchical: `Damage.Fire.Burn` is a kind of `Damage.Fire`, which in turn is a kind of `Damage`, so an object that only carries `Burn` can still answer a question about `Damage`.

The package pairs this runtime matching with editor tools for creating, assigning, and finding tags. Astra Framework is **not** required. Follow [Installation Instructions](installation-instructions.md) to install the package and import its optional samples.

## Astra Tags vocabulary

A handful of concepts come up throughout the manual, so let's introduce them one by one.

### Tag

A [`GameTagSO`](xref:ElectricDrill.AstraTags.GameTagSO) is a single tag. It stores a stable identifier (more on that below), an optional parent, a description, and visual properties such as a color and an icon or emoji.

Many objects can reference the same tag asset, and the tag never carries behavior itself. Give an enemy `State.Stunned` and nothing happens until your movement code checks for that tag and decides how to respond.

### Hierarchy and full path

Each tag can have one parent. A tag without a parent is a root, and a project can have as many independent roots as it needs (for example `Damage` and `State`).

The full path joins the names along the parent chain with dots. `Damage.Fire.Burn` is the `Burn` tag, whose parent is `Fire`, whose parent is the root `Damage`. You only ever choose the parent; the full path is worked out from it.

Matching takes advantage of this structure by walking up the hierarchy. If an object has `Damage.Fire.Burn`, asking whether it is `Damage.Fire` damage gets a yes, because a burn is a kind of fire damage. The opposite does not hold: an object tagged only `Damage.Fire` is not necessarily a `Burn`.

Objects keep their tags in a [tag set](#tag-set), described below. For an object that holds only `Damage.Fire.Burn`, the questions are answered as follows:

| Question | Result |
|---|---|
| Does it contain `Damage.Fire.Burn`? | Yes |
| Does it contain `Damage.Fire` hierarchically? | Yes |
| Does it contain `Damage` hierarchically? | Yes |
| Does it contain `Damage.Fire` exactly? | No |
| Does it contain a sibling such as `Damage.Ice`? | No |

`Damage.Fire` and `Damage` are not stored in the set, which holds only `Burn`. The ancestors are worked out at the moment you ask, which is why `Damage.Fire` is a hierarchical match but not an exact one.

### Tag set

A [`TagSet`](xref:ElectricDrill.AstraTags.TagSet) is a collection of tags that you add as a field to a `ScriptableObject`, a `MonoBehaviour`, or any serializable class. For example, a weapon can hold a set describing its damage types.

You can ask a set whether it contains a tag exactly or hierarchically, and whether it satisfies any, all, or none of a group of tags. Follow [Tag Sets and Matching](workflows/tag-sets.md) to build one and see what each question returns.

### Tag registry

Your tag assets can live anywhere in the project. The tag registry ([`TagRegistry`](xref:ElectricDrill.AstraTags.TagRegistry)) is a single asset that lists all of them in one place, so the package can look tags up quickly while the game runs. You create it once per project and refresh it whenever you add, remove, rename, or move tags within the hierarchy. [Package Configuration and the Registry](workflows/package-configuration.md) covers both.

### Stable identifier and runtime index

Every tag has a stable identifier that survives renaming its asset. Use it whenever you refer to tags in data that has to stay valid across builds, such as save files.

The registry also gives each tag a runtime index, a small number used for compact storage and quick matching. An index only makes sense together with the registry build that produced it, so keep index-based data together with that build.

### Runtime container

Some tags describe a state that several sources can grant at the same time. If two effects both grant `State.Stunned`, ending one effect leaves the tag active until the other effect also releases it. A runtime container keeps track of how many sources currently grant each tag, which makes this work.

[`TagCountContainer`](xref:ElectricDrill.AstraTags.TagCountContainer) provides this behavior in plain C#. [`TagContainer`](xref:ElectricDrill.AstraTags.TagContainer) exposes it as a `MonoBehaviour` with initial tags that you author on the component. Both provide events and observers for reacting to changes.

### Tag query

Some decisions depend on several tags at once. A [`TagQuery`](xref:ElectricDrill.AstraTags.TagQuery) combines tag conditions into a yes-or-no expression. A condition can require all, any, or none of its tags, and conditions can be grouped, combined, or negated.

For example, an ability might require a tag under `Ability.Magic` and be blocked by any tag under `State.Silenced`. The query only describes that condition; your gameplay code decides what a match allows.

## How the package fits together

A typical project uses the package in four steps, which the sections below follow in order.

### Author tags and assign them to objects

You start by creating tag assets from `Astra Tags > Tag` in Unity's asset creation menu and organizing them into a hierarchy. [Creating and Organizing Tags](workflows/creating-tags.md) guides you through it, including names, colors, and icons. `Tools > Astra Tags > Tag Manager` opens a window where you can work on the whole hierarchy at once, edit the selected tags, and inspect the assets that use them.

To give tags to your own objects, add a [`TagSet`](#tag-set) field to them. If the object also implements [`ITagged`](xref:ElectricDrill.AstraTags.ITagged), the package's editor tools can find its tags; [Integrating Custom Tagged Assets](workflows/taggable-assets.md) shows how. When a `GameObject` needs tags that several gameplay sources can grant and release, give it a [`TagContainer`](#runtime-container) instead.

### Configure the registry

Next comes the [tag registry](#tag-registry) introduced above. Setting it up is a one-time job: you create the registry asset, click **Rebuild from project** to fill it with your project's tags, and click it again whenever the hierarchy changes. [Package Configuration and the Registry](workflows/package-configuration.md) walks through each step and shows where to put the asset so your game can find it.

### Use tags in gameplay

At runtime, tags help you answer questions about your objects. Use a tag set to ask which categories an object belongs to, a runtime container when several independent sources can grant the same state, and a query when the decision combines several conditions.

Whichever you choose, keep the difference between exact and hierarchical matching in mind. Checking whether `Damage.Fire` itself is stored in a set is a different question from accepting anything beneath `Damage.Fire`, such as `Burn`.

### Find and maintain tagged assets

As a project grows, you will want to know where each tag is used. The Tag Manager and the `tag:` provider in Unity Search find the assets that carry a tag, and the Inspector displays tags and offers a hierarchy-aware picker for assigning them. These tools read the tags saved in your project's assets, so a tag that a script adds while the game is running is temporary and never appears as a saved assignment.

## Relationship to other tag systems

Astra Tags works independently of Unity's built-in `GameObject` tags: it does not replace them or change a `GameObject`'s built-in tag.

Astra Framework 2.x has its own built-in Game Tags. They are separate from Astra Tags: the similar name does not make their references interchangeable, and the package does not currently provide an automatic bridge between them.

Astra Framework 3.0 is not yet released. When it ships, Astra Framework will adopt Astra Tags and will no longer use its built-in tags.

## API reference

When you need exact type definitions, signatures, or member documentation, open the [runtime API reference](xref:ElectricDrill.AstraTags). The vocabulary above carries over to it: tag assets define meaning, sets describe membership, containers track grants, and queries evaluate conditions.
