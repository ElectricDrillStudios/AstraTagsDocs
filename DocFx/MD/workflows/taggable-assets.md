# Integrating custom tagged assets

Implement [`ITagged`](xref:ElectricDrill.AstraTags.ITagged) to expose a custom object's tags to Astra Tags editor tools. The interface requires one getter, `TagSet Tags { get; }`. A serialized backing field stores the assignments; the getter returns that same set so the tools can read and edit it.

Let's create an ability asset and a component that both use this contract. They store authored categories directly. For reference-counted gameplay states, use [`TagContainer`](xref:ElectricDrill.AstraTags.TagContainer) instead.

## Before starting

Install the package and create the `Damage.Fire.Burn` tag from [Creating and Organizing Tags](creating-tags.md). Review [Tag Sets and Matching](tag-sets.md) for the distinction between a stored assignment and a hierarchical match.

Save the scripts below in your project's runtime scripts folder, outside any `Editor` folder. If that folder belongs to a custom assembly definition, reference `com.electricdrill.astra-tags.Runtime`. Wait for compilation to finish before creating an asset or adding the component.

A registry is not required to store direct tag asset references or implement `ITagged`. Keep the [package configuration](package-configuration.md) current for the editor catalog and other registry-dependent features.

## Create a tagged `ScriptableObject`

Save this script as `AbilityDefinition.cs`:

```csharp
using ElectricDrill.AstraTags;
using UnityEngine;

[CreateAssetMenu(fileName = "Ability", menuName = "Game Data/Ability")]
public sealed class AbilityDefinition : ScriptableObject, ITagged
{
    [SerializeField] private TagSet _tags = new TagSet();

    public TagSet Tags => _tags;
}
```

`[SerializeField]` makes the private field part of Unity's serialized asset data. The initialized field provides an empty, non-null set. The read-only property exposes the mutable set; it does not prevent the editor tools or gameplay code from adding or removing tags.

Return `_tags` directly. Returning `new TagSet()` or `new TagSet(_tags)` creates a different collection on each access, so header edits do not update the stored assignments. Keep the getter safe to call in Edit mode, without requiring `Start`, a running scene, or runtime services.

### Create an instance and assign a tag

1. Select a writable folder under `Assets` in the Project window
2. Choose `Create > Game Data > Ability` from its context menu and name the asset `FireAbility`
3. Select `FireAbility`; the Inspector header provides an interactive tag bar with a trailing **+** control, including when the set is empty
4. Expand **Tags** in the Inspector body, click the list's **+**, and assign the existing `Burn` tag asset to the new entry
5. Save the project assets and select the asset again to check the assignment

The set now stores one reference, `Damage.Fire.Burn`. The header displays its pill, and the expanded field shows **Tags (1)**. Matching Fire or Damage uses the hierarchy; those ancestors are not additional stored entries.

The header's **+** opens the hierarchical tag picker. Alternatively, use **+ Add Multiple Tags…** below the expanded list. Check the desired tags and confirm with **Add** (the button includes the selected count). On a single selected object, hover a pill to reveal its remove control, or drag pills to reorder them. Both the field and the header edit the same backing set.

*Relative path:* `Game Data > Ability`
<!-- IMAGE MISSING: Capture FireAbility created from AbilityDefinition with the Burn header pill and expanded Tags (1) field showing its asset reference. -->
![FireAbility Inspector with the Burn tag pill and serialized Tags field](../../images/taggable-assets/custom-asset.png)

## Add tags to a component

Use a `MonoBehaviour` when the assignments belong to a `GameObject` rather than a shared definition asset. Save this script as `TaggedObject.cs`:

```csharp
using ElectricDrill.AstraTags;
using UnityEngine;

public sealed class TaggedObject : MonoBehaviour, ITagged
{
    [SerializeField] private TagSet _tags = new TagSet();

    public TagSet Tags => _tags;
}
```

1. Add `TaggedObject` to a scene `GameObject` and select that `GameObject`
2. Expand the component's **Tags** field, add an entry, and assign `Burn`
3. Save the scene to persist the component's assignment
4. To create a tagged project asset, save the `GameObject` as a prefab under `Assets`; verify the assignment on the saved prefab

The component field remains editable through its property drawer. The interactive pill bar appears in the `GameObject` header, rather than each component header. It uses the first `ITagged` component returned by `GetComponent<ITagged>()` on that `GameObject`. It does not merge several components or inspect children for that bar. Select a child `GameObject` to edit its own header tags, or use the relevant component's **Tags** field.

Prefab indexing has a broader scope: it collects assignments from all `ITagged` components in the saved prefab hierarchy, including inactive children. A tag on a child can therefore make the prefab appear as a match even when the root's header does not display it.

## Where assignments are stored

| Edited object | Assignment storage |
|---|---|
| `FireAbility` `ScriptableObject` asset | Its serialized `_tags` field; every reference to that asset shares those assignments |
| Component in a saved prefab | The component's serialized field in the prefab asset |
| Component on a scene `GameObject` | The component's serialized field in the scene; edits on prefab instances can be instance overrides |

The editor index is a lookup cache, and the registry catalogs tag definitions. Neither replaces the owning object's serialized set. Save the owning asset, prefab, or scene after authoring changes. Play-mode mutations are not a save system, and an unsaved runtime object is not a project asset that the index can discover.

## Make the asset discoverable

The editor discovers concrete `ITagged` types derived from `ScriptableObject` or `Component`. It skips abstract types, interfaces, and generic type definitions. No additional registration attribute is required. The getter must return a non-null set with references to saved tag assets; an empty set produces no usage entry.

A serialized `TagSet` field alone gives a type the field drawer. A non-component Inspector can also display a read-only header summary of direct `TagSet` fields. Implementing `ITagged` provides the editable header contract and the type-discovery route used by the asset index. A plain serializable C# class implementing the interface does not become an independently indexed Unity asset.

| Object or asset | Discovery scope |
|---|---|
| Main `ScriptableObject` asset implementing `ITagged` | Reads the set returned by that asset's getter |
| Saved prefab | Combines assignments from `ITagged` components throughout its hierarchy; records a prefab-level result |
| `ScriptableObject` sub-assets or nested serializable objects | Not traversed independently; the reader loads the main asset and does not enumerate all sub-assets or nested fields |
| Scene `GameObject` instances | No live per-`GameObject` index; scene-file coverage depends on **Scan Closed Scenes** |
| Saved scene with **Scan Closed Scenes** enabled | Records direct tag-asset dependencies as scene-level matches, without opening the scene or attributing tags to objects; these dependencies are not limited to `ITagged` assignments |

**Scan Closed Scenes** is off by default in `Project Settings > Astra Tags`, under **Editor Index**. Enabling it does not turn the index into a runtime-object search. Use the main `ScriptableObject` asset for the discovery check below.

### Check the saved asset in the Tag Manager

1. Save `FireAbility` under `Assets` with its Burn assignment
2. Open `Tools > Astra Tags > Tag Manager` and allow the initial background indexing scan to complete
3. Select the actual `Burn` tag in the hierarchy; `FireAbility` should appear among the matching assets
4. If the saved assignment is missing from the results, choose `Tools > Rebuild Index` in the window's toolbar menu, wait for completion, then select Burn again

Use Burn itself for this check. A parent such as Fire requires **Include descendants** to match an asset that stores only Burn. The index updates through asset import/change processing; header display and indexed results need not refresh at the same instant. Rebuilding the registry is a different operation and does not rebuild the asset index.

If the asset still does not appear, check compilation, the main asset's concrete `ITagged` type, the getter's returned field, a non-null set, and a saved reference to the intended tag asset. Keep authoring examples under `Assets`: incremental index updates explicitly restrict paths to that folder, so package assets should not be assumed to have the same update coverage.
