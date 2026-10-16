# Creating and organizing tags

Create a small tag hierarchy, give each tag a clear meaning, and configure its appearance in the Inspector. For the matching model and terminology, see [Hierarchy and full path](../introduction.md#hierarchy-and-full-path).

## Before starting

Complete [Installation Instructions](../installation-instructions.md) and let Unity finish compiling. Create a folder such as `Assets/Tags` for the project's tag assets. A registry is not required to create and edit tags.

The steps below use single-tag selection in the Project window. The tag Inspector contains **Identity**, **Hierarchy**, **Visual**, and **Usage** sections. **Open in Tag Manager** opens the selected tag in `Tools > Astra Tags > Tag Manager`, whose editing pane uses the same sections.

## Create a parent and its children

Let's build `Damage.Fire.Burn` and a sibling branch, `Damage.Ice`:

1. Select the project's tag folder in the Project window
2. Open the asset creation menu and choose `Astra Tags > Tag`; name the new asset `Damage`
3. Select `Damage` and leave **Parent** set to **(root)** in **Hierarchy**
4. Create another tag asset named `Fire`; in its Inspector, open **Parent** and select `Damage`
5. Create `Burn`; set its **Parent** to `Fire` beneath `Damage` in the parent menu
6. Create `Ice`; set its **Parent** to `Damage`
7. Select `Burn` and check that its breadcrumb reads `Damage › Fire › Burn`

The resulting hierarchy is:

| Asset name | Parent | Full path |
|---|---|---|
| `Damage` | (root) | `Damage` |
| `Fire` | `Damage` | `Damage.Fire` |
| `Burn` | `Damage.Fire` | `Damage.Fire.Burn` |
| `Ice` | `Damage` | `Damage.Ice` |

Name each asset with its own segment, such as `Burn`, rather than the full dotted path. The hierarchy comes from **Parent**, independently of the folder containing the asset. Moving an asset between project folders does not change that relationship.

For `Burn`, enter a **Description** such as “Fire damage applied over time.” The description records the tag's intended meaning; gameplay code decides what the tag does.

*Relative path:* `Astra Tags > Tag`
<!-- IMAGE MISSING: Capture Burn's Inspector with its stable Id, Damage > Fire > Burn breadcrumb, Parent, Description, and Visual controls visible. -->
![Burn tag Inspector showing identity, hierarchy, description, and visuals](../../images/creating-tags/tag-inspector.png)

### Change the hierarchy safely

Select a tag and choose a new **Parent**, or choose **(root)** to detach it. Renaming a tag or changing its parent also changes the full paths of its descendants. For example, renaming `Fire` to `Flame` makes `Burn`'s full path `Damage.Flame.Burn`.

A tag cannot be its own parent or be parented under one of its descendants. If editor validation encounters a cyclic parent assignment, it logs a warning and clears that tag's parent to make it a root. Check the breadcrumb after changing a parent.

> [!CAUTION]
> The current **Parent** menu can omit a valid ancestor and offer a descendant that cannot be assigned safely. If an intended ancestor is missing, first choose **(root)**, then choose that ancestor. Do not choose a descendant to rearrange a branch: validation can clear the parent instead of retaining the previous relationship.

Parent changes do not check sibling-name collisions in this Inspector. Before moving a tag, ensure that its name is unique under the destination parent (including the root level). Resolve any duplicate names rather than treating identical full paths as interchangeable tags.

## Choose valid names

Use the **Name** field in **Identity** to rename an existing asset. The Inspector rename and Tag Manager creation/rename actions check names against the project's tag catalog:

| Name or situation | Result |
|---|---|
| Empty or whitespace-only name | Not accepted |
| `Fire.Burn` | Rejected: a dot is reserved for the hierarchy separator |
| Leading or trailing whitespace | Invalid under the naming policy; Inspector and Tag Manager text entry trim it before validation |
| `Fire` and `fire` under the same parent | Rejected by checked creation/rename actions (comparison ignores case) |
| Two roots named `Damage` | Rejected by checked creation/rename actions |
| `Fire` under two different parents | Allowed: the full paths differ |
| `Fire Damage` | Allowed without an identifier warning; internal whitespace is accepted |
| `Fire-Damage` or a name starting with a digit, such as `2Fire` | Allowed with a warning about generated C# identifiers |

Letters, digits, and underscores are accepted without that warning when the name does not start with a digit. Internal whitespace is also accepted; generated identifiers replace it with underscores. Other characters trigger an advisory and are sanitized by code generation. A valid display name is not necessarily the exact generated C# identifier.

> [!NOTE]
> Direct Project-window creation or renaming does not use all of these checked actions. The tag's validation warns about invalid name syntax but does not rewrite it or enforce sibling uniqueness. Use the package's **Name** field for subsequent renames and check names after imports and parent changes.

## Preserve stable identity

The read-only **Id** field in **Identity** displays the tag's stable identifier. Unity editor validation assigns it when it is empty. **Copy** copies it to the clipboard.

Renaming a tag, moving its asset, or changing **Parent** preserves its `Id`. Its `FullPath` can change, so use stable IDs for persistent data that must survive those edits. The tag ID is separate from Unity's asset GUID and from the registry-assigned runtime index; see [Stable identifier and runtime index](../introduction.md#stable-identifier-and-runtime-index).

**Regenerate** opens a **Regenerate tag id** confirmation dialog. Use it only when deliberately repairing a duplicated tag ID, for example after an asset import. Choose **Cancel** to keep the current ID.

> [!WARNING]
> Confirming **Regenerate** assigns a new identity. Saved data, network messages, or custom scene data that store the old tag ID no longer resolve to this tag through that ID. Regeneration does not migrate those values. Ordinary Unity object references use a separate asset identity; changing the tag ID does not replace the asset.

Select only the tag being repaired: if multiple tag assets are selected, confirming **Regenerate** changes every selected tag's ID.

## Configure appearance

Appearance belongs to each tag. Set it on the individual assets whose pills should change; assigning a parent does not copy its visual settings to its children.

In **Visual**, configure the following fields:

| Inspector field | Purpose |
|---|---|
| **Color** | Flat pill color, or the start color when a gradient is enabled |
| **Use Gradient** | Switch between a flat color and a two-color fill |
| **End Color** | Gradient end color; shown when **Use Gradient** is enabled |
| **Direction** | Gradient direction; shown when **Use Gradient** is enabled |
| **Icon** | Optional emoji or project sprite, chosen with **Choose…** and removed with **Clear** |

New tags start with a blue color (RGBA `0.35, 0.55, 0.75, 1`), no icon, and **Use Gradient** disabled. The initial **End Color** is white and **Direction** is **Diagonal**.

The gradient directions are:

| Direction | Start to end |
|---|---|
| **Diagonal** | Top-left to bottom-right |
| **Horizontal** | Left to right |
| **Vertical** | Top to bottom |

For example, select `Burn`, choose an orange **Color**, enable **Use Gradient**, choose a red **End Color**, and set **Direction** to **Horizontal**. Check **Preview** beneath the icon controls: it shows **Breadcrumb**, **Flat**, and **Hover card** presentations.

### Choose an emoji or sprite

With one tag selected, click **Choose…** beside **Icon**:

- In **Emoji**, type in **Search emoji…** or choose a category, then click an emoji to apply it and close the picker
- Alternatively, paste an emoji or short text into **Or paste:** and press Enter
- In **Sprite**, assign a project sprite to **Sprite**, or choose one shown under **Used by other tags**; selection applies it and closes the picker
- Use **Clear icon** in the picker or **Clear** in the Inspector to remove an icon; **Cancel** closes the picker without applying a choice

The emoji tab includes **Recent** and **Favourites**. Right-click an emoji to pin or unpin it; emoji that support skin tones also offer a **Skin tone** submenu. Unsupported glyphs are hidden by default; **Show unsupported** reveals them, but their appearance still depends on the editor's font support.

<!-- IMAGE MISSING: Capture Burn's icon picker on the Emoji tab with Search emoji…, category controls, and the Sprite tab visible. -->
![Tag icon picker with Emoji search, categories, and Sprite tab](../../images/creating-tags/icon-picker.png)

Sprite icons store an asset GUID rather than a hard `Sprite` reference. The package resolves it in the editor for drawing, so assigning an icon does not by itself include that texture in a player build. Runtime UI needs its own asset loading and rendering. The picker stores only the asset GUID, not an individual sub-sprite identifier; use a separate sprite asset when a specific sprite-sheet slice must be unambiguous.

Colors, icons, gradients, and descriptions affect presentation and authoring metadata, not tag matching or stable identity.

After creating the hierarchy, follow [Package Configuration and the Registry](package-configuration.md) to make the project tags available to runtime registry lookups.

## API reference

[GameTagSO](xref:ElectricDrill.AstraTags.GameTagSO) exposes the authored identity, parent, description, and visual properties. Use `FullPath`, `Depth`, and `Ancestors` to inspect the hierarchy; `Ancestors` runs from the immediate parent toward the root. The runtime hierarchy walks have a 64-step guard; keep authored hierarchies shallow rather than relying on arbitrarily deep paths.

[TagIcon](xref:ElectricDrill.AstraTags.TagIcon) represents an optional icon, with [TagIconKind](xref:ElectricDrill.AstraTags.TagIconKind) distinguishing `None`, `Emoji`, and `Sprite`. [GradientDirection](xref:ElectricDrill.AstraTags.GradientDirection) defines the fill directions above. These are runtime data types; the picker and pill drawing described here are editor features.
