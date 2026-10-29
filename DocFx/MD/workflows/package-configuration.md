# Package Configuration and the Registry

In this guide we set Astra Tags up for a project: we adjust the package settings in `Edit > Project Settings > Astra Tags`, create the tag registry that the running game uses to look tags up, and then check that the game can find it. The guide assumes the package is [installed](../installation-instructions.md) and tag assets already exist. The small hierarchy from [Creating and Organizing Tags](creating-tags.md) works well as an example to check the result against.

As the [introduction](../introduction.md#tag-registry) describes, a [`TagRegistry`](xref:ElectricDrill.AstraTags.TagRegistry) is the asset that lists your project's tags. From that list it builds what the package needs for quick lookups: the runtime indices and the ancestor masks (precomputed data that speeds up hierarchical matching). The registry plays two roles that are easy to mix up. The editor tools need to know which registry asset to update, and the running game needs to be able to load one. They are separate steps, and this guide covers both.

## Configure the editor tools

Let's start with the settings used by the editor tools. Open `Edit > Project Settings > Astra Tags`. These project-scoped settings are saved in `ProjectSettings/AstraTags.json`; include that file in the Unity project's version control to share them with the team. Gameplay code does not read this settings file.

| Section and control | Default | Purpose |
|---|---|---|
| **Authoring > Default Tag Folder** | `Assets` | Destination for new root tags created in the Tag Manager. Use an existing folder under `Assets/`; child tags are created beside their parent. An invalid folder falls back to `Assets` |
| **Authoring > Editor Registry** | Unassigned | Asset written by the Tag Manager's **Tools > Rebuild Registry** action. When unassigned, that action looks for `Resources/AstraTags/TagRegistry` |
| **Authoring > Check a Name** | Empty | Checks a candidate's name syntax and displays advisories. It does not select a parent or check sibling-name collisions |
| **Editor Index > Scan Closed Scenes** | Disabled | Adds closed-scene tag references to the editor index using scene-level asset dependencies, without loading the scenes. Changing it rebuilds the editor index |
| **Code Generation > Generate Type-Safe Accessors** | Disabled | Enables automatic accessor generation; enabling it immediately regenerates the code |
| **Code Generation > Output Path** | `Assets/AstraTags.g.cs` | Project-relative generated C# destination under `Assets/`, ending in `.cs` |
| **Code Generation > Namespace** | Empty | Namespace of the generated accessors; empty uses the global namespace |
| **Code Generation > Root Class** | `AstraTags` | Name of the outer generated static class |

The code generation fields and **Regenerate Now** button are enabled only when **Generate Type-Safe Accessors** is on. They are optional for registry setup. **Scan Closed Scenes** affects asset discovery in the Editor, not the runtime registry or tag matching. See [tag naming rules](creating-tags.md#choose-valid-names) before using **Check a Name** as an authoring aid.

<!-- IMAGE MISSING: Capture Project Settings > Astra Tags with Authoring, Editor Registry, Editor Index and Code Generation controls visible, using the defaults before registry assignment. -->
![Astra Tags Project Settings with editor registry and authoring controls](../../images/package-configuration/project-settings.png)

## Create the runtime registry

Let's make one project registry available through the default resource lookup:

1. In the Project window, create `Assets/Resources/AstraTags` if it does not exist
2. Select that folder and use `Create > Astra Tags > Tag Registry`. Keep the asset name `TagRegistry`, giving `Assets/Resources/AstraTags/TagRegistry.asset`
3. Select the new registry and click **Rebuild from project** in its Inspector
4. Check the tag list, tag count and rebuild result. If the only project tags are the four from the creation guide, the registry contains `Damage`, `Damage.Fire`, `Damage.Fire.Burn` and `Damage.Ice`, in that order. Other project tag assets are collected too
5. Resolve any naming warnings using the [creation guide](creating-tags.md#choose-valid-names). Rebuilding reports naming issues but does not rename or reject the affected assets
6. In Project Settings, assign this same asset to **Editor Registry**, or leave the field unassigned to let the Tag Manager find it at the default resource path
7. Click **Rebuild from project** again. With no list changes, the result reads **up to date** and the builder does not dirty or save the asset

The game finds the registry through a resource key, `AstraTags/TagRegistry`, which the package exposes as `TagRegistry.ResourcePath`. The key leaves out the `Resources/` prefix and the `.asset` extension. Keep exactly one runtime registry at that key: an asset with a different name, or one placed in a subfolder beneath `AstraTags`, is not found by this lookup.

*Relative path:* `Astra Tags > Tag Registry`
<!-- IMAGE MISSING: Capture the TagRegistry Inspector after Rebuild from project with the four-tag example, tag count, hexadecimal signature, rebuild button and up-to-date result visible. -->
![Tag Registry Inspector with the project tag list and rebuild result](../../images/package-configuration/tag-registry.png)

The Tag Manager provides another entry point: open `Tools > Astra Tags > Tag Manager`, then choose **Tools > Rebuild Registry**. It uses **Editor Registry** first, then the default resource. If neither exists, its **No Tag Registry** dialog offers **Create**, which creates `Assets/Resources/AstraTags/TagRegistry.asset`, assigns it as the editor registry and populates it. If an editor registry already exists elsewhere, this action updates that asset without creating a runtime resource.

> [!IMPORTANT]
> **Editor Registry** only tells the editor tools which asset to update. It is separate from `TagRegistry.Active` and from the runtime resource key, and it does not move any asset into `Resources`. For the default setup, point both at the same asset.

## Keep the registered list current

The registry does not follow your tag assets on its own, so refresh it whenever the hierarchy changes. Run **Rebuild from project** after adding, deleting, renaming or reparenting tag assets, and before testing or building the game. The builder collects all project `GameTagSO` assets, sorts them by full path using ordinal comparison, removes null or duplicate list entries, and saves the registry only when its serialized list differs. Because it replaces the list with the collected project tags, a hand-picked subset is not preserved. The rest of this guide calls this refresh project reconciliation.

The Inspector result shows the tag count and counts of added (`+`), removed (`−`) or reordered (`~`) entries. Naming warnings appear below it. The Tag Manager's status bar shows the one-line result; inspect the registry itself to review naming warnings.

Two operations are both called a rebuild, and they do different jobs:

| Operation | Reads | Changes |
|---|---|---|
| Inspector **Rebuild from project** / Tag Manager **Rebuild Registry** | Project tag assets | Reconciles and, when needed, saves the serialized tag list; a changed list also triggers a runtime rebuild |
| [`TagRegistry.Rebuild()`](xref:ElectricDrill.AstraTags.TagRegistry.Rebuild) | The registry's existing serialized list | Reconstructs derived lookups, dense indices and ancestor masks in memory; does not discover project assets, sort the list or save it |

Editor code can run the project reconciliation too, through `TagRegistryBuilder.RebuildFromProject(registry)` in `ElectricDrill.AstraTags.Editor`; keep that call in editor-only code. Code that runs in the game uses `TagRegistry.Rebuild()` instead.

The registry builds its runtime lookups lazily, on the first access that needs them, such as `Count` or `Find`. In the Editor, changing the tag structure marks those lookups as outdated so they are rebuilt later, but that does not add newly created tags to the serialized list or remove deleted ones. Project reconciliation is still needed for that.

### Signature and indices

The Inspector shows the registry's [`Signature`](xref:ElectricDrill.AstraTags.TagRegistry.Signature) as a hexadecimal value. It is a content hash of the ordered tag IDs and their parent IDs, including the tag count, so rebuilding the same data gives the same signature (it is not a counter that advances on every click). Changing the membership, the order or a parent relationship changes the input to that hash. A rename on its own is not hashed directly, but it can change the order that project reconciliation produces.

Runtime indices belong to one ordered registry build, and adding or reordering tags can change them. For that reason, use stable tag IDs for anything that must persist, and keep compact index data together with the registry build that produced it. The signature only describes the registry; it cannot add a missing tag or repair an outdated list.

## Resolve the registry at runtime

At runtime, the game gets the registry through [`TagRegistry.Active`](xref:ElectricDrill.AstraTags.TagRegistry.Active). On its first read it calls `Resources.Load<TagRegistry>(TagRegistry.ResourcePath)` and caches the result, and later reads return that cached value (a missing resource is cached as `null` too). Read it during game initialization or gameplay rather than from a static field initializer, which might run before the intended setup.

Let's check the setup with a small component. For the default resource setup, attach it to a scene `GameObject`; in `Start` it checks the registry and looks up the example tag:

```csharp
using ElectricDrill.AstraTags;
using UnityEngine;

public sealed class RegistryLookupExample : MonoBehaviour
{
    private void Start()
    {
        var registry = TagRegistry.Active;
        if (registry == null)
        {
            Debug.LogError("No active Tag Registry. Check Resources/AstraTags/TagRegistry.");
            return;
        }

        var burn = registry.Find("Damage.Fire.Burn");
        if (burn == null)
        {
            Debug.LogError("Burn is not registered at Damage.Fire.Burn. Rebuild from project.");
            return;
        }

        var byId = registry.FindById(burn.Id);
        int index = registry.IndexOf(burn);
        Debug.Log($"{byId.FullPath}: index {index}, registry has {registry.Count} tags.");
    }
}
```

With only the four example tags, `Damage.Fire.Burn` resolves at index `2` and the count is `4`. The example reads the asset's actual ID instead of assuming that IDs are derived from names.

### Lookup APIs

The [registry API reference](xref:ElectricDrill.AstraTags.TagRegistry) provides the complete signatures:

| Member | Result and limits |
|---|---|
| `Find(string fullPath)` | Exact, case-sensitive dotted-path lookup; `null` for a missing or null path. It does not search descendants |
| `FindById(string id)` | Exact, case-sensitive stable-ID lookup; `null` for a missing or null ID |
| `GetAt(int runtimeIndex)` | Registered tag at that index; `null` for a negative or out-of-range index |
| `IndexOf(GameTagSO tag)` | Index in this registry; `-1` for a null or unregistered tag |
| `Count` / `Tags` | Distinct non-null registered tags, with `Tags` in runtime-index order |

Keep IDs and full paths unique: when duplicate keys exist, the corresponding lookup keeps the last entry encountered during the runtime build. The naming warnings from reconciliation help you spot path collisions, but fixing them is up to you. To check whether a tag belongs to a particular registry, use `IndexOf`; a tag's `RuntimeIndex` alone is not proof that it belongs to that registry.

### Explicit initialization and resolution timing

A project with its own bootstrap can hand the package an already loaded registry by assigning `TagRegistry.Active` explicitly, which also allows an asset outside the default resource path. For example, call this method from the game's startup sequence with the loaded registry, and start tag consumers only if it returns `true`:

```csharp
using ElectricDrill.AstraTags;
using UnityEngine;

public static class TagRegistryInitialization
{
    public static bool Initialize(TagRegistry registry)
    {
        if (registry == null)
        {
            Debug.LogError("Provide the project Tag Registry before starting tag consumers.");
            return false;
        }

        registry.Rebuild();
        TagRegistry.Active = registry;
        return true;
    }
}
```

The caller must obtain the populated asset through a serialized reference or the project's loading system, and must call the helper itself, since nothing runs it automatically. Invoke it before other components use tags or cache lookup results. A call in one component's `Awake` is not enough on its own, because it does not order that call before other components' `Awake` methods. The example's `Rebuild()` prepares existing entries; collecting missing project tags is the job of project reconciliation in the Editor.

Assigning `Active`, even with `Active = null`, pins that value and turns off automatic resource loading, so setting it to `null` is not a way to retry or reset. In the Editor, a domain reload or any play-mode transition releases the cached resolution, including when entering Play mode without a domain reload. Reapply explicit initialization after entering Play mode and before starting consumers, because an assignment made in edit mode does not survive these transitions. Player builds should not count on those editor transitions to retry a failed lookup.

Normal gameplay should use a single registry. If initialization has to replace a value that was already resolved, assign the replacement explicitly before consumers run and refresh any tag references or index data they already cached, because a later assignment does not update variables that received `null` or old lookup results.

## Recover from missing or stale data

| Symptom | Check and recovery |
|---|---|
| `TagRegistry.Active` is `null` | Verify the resource asset's type, name and location, or the explicit bootstrap reference. If the first resolution already failed, restart Play mode after fixing the asset, or explicitly assign the loaded registry before resuming consumers |
| Editor rebuild succeeds, but gameplay sees another registry or none | Compare **Editor Registry** with `Assets/Resources/AstraTags/TagRegistry.asset`. Update the runtime asset too, or deliberately supply the editor-selected asset through explicit initialization |
| `Find` or `FindById` returns `null` for an existing tag asset | Check the exact full path or ID and run **Rebuild from project** on the registry actually used by the game. Calling `Rebuild()` alone cannot register the asset |
| Rebuild reports naming warnings or a path resolves to the wrong tag | Fix invalid names and sibling/root collisions, then reconcile again. Also check for accidentally duplicated IDs; do not regenerate IDs used by saved data without considering their references |
| A rename, deletion or hierarchy change leaves old entries or indices | Reconcile the serialized list, then restart the relevant gameplay session and discard cached indices from the old registry build |
| Rebuild shows **up to date** but the signature did not advance | This is expected for unchanged data. Verify the needed tag's membership and lookup result rather than expecting a rebuild counter |

> [!NOTE]
> Many tag operations work without a registry. Without an active registry, hierarchical `TagSet` matching can follow parent references, and direct tag references and exporting their IDs with `TagSet.ToIdArray()` remain usable. Resolving IDs or registry-specific indices has different requirements, so consult the relevant [`TagSet` API members](xref:ElectricDrill.AstraTags.TagSet) before choosing a persistence format.
