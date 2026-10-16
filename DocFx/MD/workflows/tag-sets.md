# Tag sets and matching

A [TagSet](xref:ElectricDrill.AstraTags.TagSet) stores distinct tag asset references. Use it to check literal assignments, accept tags through their ancestors, or combine stored assignments with set operations. Matching never inserts inferred ancestors into the collection.

## Before starting

Complete [Creating and Organizing Tags](creating-tags.md) to create this hierarchy:

| Reference used below | Full path | Parent |
|---|---|---|
| `damage` | `Damage` | (root) |
| `fire` | `Damage.Fire` | `damage` |
| `burn` | `Damage.Fire.Burn` | `fire` |
| `ice` | `Damage.Ice` | `damage` |

These names refer to the actual `GameTagSO` assets, not strings or generated accessors. Direct references work without a registry. The runnable matching example obtains them through the registry configured in [Package Configuration and the Registry](package-configuration.md).

## Store a set in a serialized field

A set can be a field on a MonoBehaviour, ScriptableObject, or serializable class. For example, save this component as `TagSetFieldExample.cs` and attach it to a GameObject:

```csharp
using ElectricDrill.AstraTags;
using UnityEngine;

public sealed class TagSetFieldExample : MonoBehaviour
{
    [SerializeField] private TagSet _tags = new TagSet();

    public bool HasTag(GameTagSO tag) => _tags.Contains(tag);
}
```

Expand **Tags** in the Inspector, add a list entry with **+**, and assign the `Burn` asset. The expanded list also provides **+ Add Multiple Tags…** for selecting several tags. An Inspector assignment stores a reference to an existing tag asset; it does not create a tag or add the tag's parents as entries.

Follow [Integrating Custom Tagged Assets](taggable-assets.md) to expose the stored set through `ITagged` for editable headers and asset discovery.

`new TagSet()` creates an empty set. `new TagSet(burn)` stores one tag, and `new TagSet(new[] { burn, ice })` stores a sequence. The sequence constructor skips nulls and duplicate references while retaining the first occurrence's position. `new TagSet(existingSet)` copies the entries into a separate collection, retaining references to the same tag assets. Assigning `var copy = existingSet` shares the same mutable set instead.

## Choose exact or hierarchical membership

`ContainsExact(tag)` checks whether the tag asset is explicitly stored. `Contains(tag)` checks whether a stored tag is the requested tag or a descendant of it. `HasAny(GameTagSO)` is an alias for `Contains`, and `HasNone(GameTagSO)` returns its inverse. There is no single-tag `HasAll` overload; use `Contains` for one requirement.

For `owned = new TagSet(burn)`:

| Expression | Result | Reason |
|---|---|---|
| `owned.ContainsExact(burn)` | `true` | Burn is stored |
| `owned.ContainsExact(fire)` | `false` | Fire is only inferred |
| `owned.Contains(fire)` | `true` | Burn is a descendant of Fire |
| `owned.Contains(damage)` | `true` | Burn is a descendant of Damage |
| `owned.Contains(ice)` | `false` | A sibling branch is not satisfied |
| `new TagSet(fire).Contains(burn)` | `false` | Holding a parent does not imply a particular child |
| `owned.Count` | `1` | Inferred ancestors are not stored entries |

Checks use tag references and parent relationships. A separate asset with a similar name or path is not interchangeable with the queried asset.

### Match a group of requirements

For set overloads, call `owned.HasAny(query)`, `owned.HasAll(query)`, or `owned.HasNone(query)`. Each entry in `query` is a requirement evaluated hierarchically against `owned`. The direction matters: reversing the sets asks a different question.

For `owned = new TagSet(burn)`:

| Query entries | `HasAny(query)` | `HasAll(query)` | `HasNone(query)` |
|---|---|---|---|
| Fire | `true` | `true` | `false` |
| Damage, Fire | `true` | `true` | `false` |
| Fire, Ice | `true` | `false` | `false` |
| Ice | `false` | `false` | `true` |
| (empty) | `false` | `true` | `true` |

One stored child can satisfy multiple ancestor requirements. `HasAll` does not require a different stored entry for each requirement. These methods have no exact-matching flag; use `ContainsExact` for each literal requirement when that is the intended rule.

### Run the matching example

Save this component as `TagSetMatchingExample.cs`, attach it to a scene GameObject, and enter Play mode after setting up the four-tag runtime registry. It reads the actual assets from that registry and logs the results above:

```csharp
using ElectricDrill.AstraTags;
using UnityEngine;

public sealed class TagSetMatchingExample : MonoBehaviour
{
    private void Start()
    {
        var registry = TagRegistry.Active;
        if (registry == null)
        {
            Debug.LogError("Set up Resources/AstraTags/TagRegistry first.");
            return;
        }

        var damage = registry.Find("Damage");
        var fire = registry.Find("Damage.Fire");
        var burn = registry.Find("Damage.Fire.Burn");
        var ice = registry.Find("Damage.Ice");
        if (damage == null || fire == null || burn == null || ice == null)
        {
            Debug.LogError("Create the four-tag hierarchy and rebuild the runtime registry from project.");
            return;
        }

        var owned = new TagSet(burn);
        var mixedQuery = new TagSet(new[] { fire, ice });
        var ancestorQuery = new TagSet(new[] { damage, fire });

        Debug.Log($"Exact Burn: {owned.ContainsExact(burn)}; exact Fire: {owned.ContainsExact(fire)}");
        Debug.Log($"Matches Fire: {owned.Contains(fire)}; matches Ice: {owned.Contains(ice)}");
        Debug.Log($"Fire implies Burn: {new TagSet(fire).Contains(burn)}");
        Debug.Log($"Mixed any/all/none: {owned.HasAny(mixedQuery)}/{owned.HasAll(mixedQuery)}/{owned.HasNone(mixedQuery)}");
        Debug.Log($"All ancestors: {owned.HasAll(ancestorQuery)}; stored count: {owned.Count}");

        foreach (var tag in owned)
            Debug.Log($"Stored: {tag.FullPath}");
    }
}
```

The expected values are `True/False` for exact Burn/Fire, `True/False` for matching Fire/Ice, `False` for Fire implying Burn, `True/False/False` for the mixed query, and `True` with count `1` for the ancestor query. Enumeration logs only `Damage.Fire.Burn`.

### Null and empty inputs

These results apply to an initialized receiving set, including an empty one:

| Call | Result |
|---|---|
| `Contains((GameTagSO)null)` / `ContainsExact((GameTagSO)null)` | `false` |
| `HasAny((GameTagSO)null)` | `false` |
| `HasNone((GameTagSO)null)` | `true` |
| `HasAny((TagSet)null)` / `HasAny(new TagSet())` | `false` |
| `HasAll((TagSet)null)` / `HasAll(new TagSet())` | `true` |
| `HasNone((TagSet)null)` / `HasNone(new TagSet())` | `true` |

An empty receiving set cannot satisfy any non-null single tag or any non-empty normalized query: `HasAny` and `HasAll` return `false`, while `HasNone` returns `true`. A query constructed entirely from null references becomes empty, so the empty-query rules apply.

Cast a null literal in `HasAny(null)` and `HasNone(null)` to select the tag or set overload; an untyped literal is ambiguous. The same applies to `new TagSet(null)`, which has both single-tag and sequence constructors. `new TagSet((GameTagSO)null)` and `new TagSet((System.Collections.Generic.IEnumerable<GameTagSO>)null)` both create an empty set. A null receiving variable still cannot be used to call instance methods.

## Modify literal assignments

Mutation operates on stored references. Removing Fire from a set containing only Burn leaves Burn present, so the set continues to match Fire hierarchically.

| Operation | Behavior |
|---|---|
| `Add(tag)` | Appends a new reference and returns `true`; returns `false` for null or an existing reference |
| `Remove(tag)` | Removes that exact reference and returns `true`; returns `false` for null or an absent reference |
| `Clear()` | Removes all stored entries |
| `UnionWith(other)` | Adds missing literal entries from `other`, in their iteration order |
| `ExceptWith(other)` | Removes entries literally present in `other` |
| `IntersectWith(other)` | Keeps entries literally present in `other`, preserving their relative order |

The three set operations modify the receiving set. They return `void` and do not mutate a separate `other` collection. For each independent operation below, start with stored entries `[Burn, Ice]` and use `other = [Fire, Ice]`:

| Operation | Resulting stored entries | Explanation |
|---|---|---|
| `UnionWith(other)` | Burn, Ice, Fire | Fire is added even though Burn already matches it |
| `ExceptWith(other)` | Burn | Ice is removed; Fire does not remove its descendants |
| `IntersectWith(other)` | Ice | Burn is not literally in `other` |

`UnionWith(null)` and `ExceptWith(null)` leave membership unchanged. `IntersectWith(null)` clears the set. An empty `other` has the same respective effects.

> [!CAUTION]
> Avoid `set.ExceptWith(set)` at the current source baseline. It removes an entry while iterating the same internal list and can throw `InvalidOperationException` after partially changing a non-empty set. Use `set.Clear()` to remove everything. When two variables may refer to the same collection, pass a separate copy such as `new TagSet(other)` to `ExceptWith`.

## Ordering and enumeration

`Count`, the zero-based indexer, `Tags`, and enumeration expose stored entries in presentation order. `Tags` is an `IReadOnlyList<GameTagSO>` view of the same collection, so later mutations are visible through an existing view; it is not a snapshot. Use `new TagSet(set)` when an independent collection is needed. The indexer throws `ArgumentOutOfRangeException` for an invalid index.

`MoveBefore(tag, before)` returns `false` if `tag` is absent. Otherwise, it removes that entry and inserts it before `before`. A null or absent target moves it to the end. Passing the same tag as both arguments also moves it to the end, because the target is looked up after removal. A successful call returns `true`, including when the final order is unchanged. Ordering does not affect matching or set equality.

Use `foreach (var tag in set)` as in the matching example. It uses [TagSet.Enumerator](xref:ElectricDrill.AstraTags.TagSet.Enumerator), whose public `MoveNext()` advances and `Current` reads the current stored entry. Read `Current` only after `MoveNext()` returns `true`. Iterating through `IEnumerable<GameTagSO>` or non-generic `IEnumerable` is also supported. Finish iteration before changing the set; enumerators are not snapshots and mutation behavior differs between the direct and interface paths.

## Equality and normalization

`Equals(TagSet)` and `Equals(object)` compare literal membership regardless of order. `[Burn, Ice]` equals `[Ice, Burn]` and produces the same hash code. `[Burn]` does not equal `[Burn, Fire]`, even though both match Fire. `[Burn]` also does not equal `[Fire]`. Comparing a set with null using `Equals` returns `false`.

`TagSet` is a class and does not overload `==` or `!=`; those operators compare set object identity. Use `Equals` to compare membership. Membership changes can change `GetHashCode()`, so avoid mutating a set while using it as a dictionary key or hash-set element.

After Unity deserializes a set, normalization is deferred until an operation needs the stored entries (for example, reading `Count`, accessing `Tags`, or enumerating). It removes null and duplicate tag references, keeping the first occurrence and the order of surviving entries. The deserialization callback marks the collection for this work; it does not prune referenced Unity objects inside the callback. `OnBeforeSerialize` performs no cleanup. Normalization does not collapse child/ancestor pairs: storing both Burn and Fire keeps two distinct entries.

This serialized field stores Unity asset references. Explicit save/network formats are separate APIs: consult [TagSet](xref:ElectricDrill.AstraTags.TagSet) for `ToIdArray`, `ToIndexArray`, `LoadIds`, `LoadIndices`, `FromIds`, and `FromIndices`, and [the registry guide](package-configuration.md#signature-and-indices) for the identity/index distinction.

## Matching with and without a registry

Exact membership, mutation, equality, and enumeration use stored references directly. Hierarchical matching uses a lazily built ancestor mask when an active registry can represent the set and the queried tag. Membership changes and registry signature changes cause the matching mask to rebuild when needed.

| Situation | Matching path |
|---|---|
| No active registry | Walks parent references from each stored entry |
| At least one stored tag is absent from the active registry | Treats the set's mask as incomplete and uses the parent walk for queries |
| The queried tag is absent from the active registry | Uses the parent walk for that query |
| Stored and queried tags are registered, with available ancestor masks | Uses the registry-derived mask |

For example, a directly referenced Burn still matches Fire when Burn or Fire is unregistered, through the corresponding fallback above. A missing registry lookup cannot supply such a reference: `registry.Find(...)` returns null for an absent tag, and null inputs follow their own rules.

Keep the full hierarchy, including intermediate ancestors, in the registry and reconcile it after authoring changes. The fallbacks do not validate every gap in an otherwise usable mask: registry mask construction bounds its ancestor walk by registry size. Very sparse registries can therefore omit a distant registered ancestor. The direct fallback also inspects at most 64 nodes per stored entry, including the entry itself. Do not rely on malformed cycles or arbitrarily deep hierarchies matching identically across paths.

These paths do not imply constant-time set queries or allocation-free first use. Keep the [registry setup](package-configuration.md) current and use the [API reference](xref:ElectricDrill.AstraTags.TagSet) for complete member signatures.
