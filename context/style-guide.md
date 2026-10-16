# Style Guide — Astra Package Documentation

> All documentation is written in **English**. Conversations with the user happen in **Italian**.
> Follow this guide when writing or editing documentation in this repository.
> When in doubt, use the established reference pages listed in `context/package-notes.md`, when present. The initial template has no substantive reference pages.
> Examples below illustrate formatting; verify all names, paths, and signatures against the package being documented before using them in a page.

---

## Heading Structure

- `#` — page title (one per file)
- `##` — major sections
- `###` — subsections
- `####` — sub-subsections
- Do **not** use `#####` for inline labels; use bold inline labels instead

---

## Language, Tone, and Register

- Professional, instructional, and technically precise
- Default to third-person neutral exposition
- Use direct imperative phrasing for guidance when needed
- Prefer concept -> configuration/details -> example -> caveats/links
- Keep explanations compact when a cross-reference can carry the detail
- Use **"Let's"** phrasing naturally for guided walkthroughs and examples
- Use parenthetical asides `(like this)` for brief clarifications instead of em-dashes
- Avoid summary sections unless the user explicitly asks for them

---

## Inline Formatting

| What | Format | Example |
|---|---|---|
| Class, interface, method, generic type, enum, field in code context | `` `inline code` `` | `EntityCore`, `GameAction<TContext>`, `RunFireAndForget` |
| Inspector field names and user-facing inspector labels | `**Bold**` | **Use constant value at level 1**, **Max Level** |
| Unity asset creation paths and editor menu paths | `` `inline code` `` | `Astra <Package> -> <Asset>`, `Tools > Astra <Package> > <Command>` (replace placeholders with verified labels) |
| File, folder, asset, and package paths | `` `inline code` `` | `Packages/com.electricdrill.astra-package-name/Runtime` |
| Version availability tags | `*🏷️ Version X.Y.Z+*` or inline `(🏷️*vX.Y.Z+*)` | `(🏷️*v1.4.0+*)` |

- Apply inline code to programmatic identifiers in prose, headings, tables, and link labels, including Unity types such as `ScriptableObject` and `MonoBehaviour`
- When an identifier is linked, put the backticks inside the link label: `` [`GameTagSO`](xref:ElectricDrill.AstraTags.GameTagSO) ``; keep the destination outside the code span
- Do not combine bold and inline code for the same token
- Use the exact casing used by Unity, the package, or the source code

---

## Links and Cross-References

| Link type | Format | Example |
|---|---|---|
| Same-file anchor | `[Title](#anchor)` | `[Game Event Generators](#game-event-generators)` |
| Other file in the same documentation folder | `[Text](filename.md)` | `[Samples](samples.md)` |
| Other file + anchor | `[Text](filename.md#anchor)` | `[Understanding Stat Modifier Types](workflows.md#understanding-stat-modifier-types)` |
| API xref | `` [`TypeName`](xref:Namespace.TypeName) `` | `` [`GameTagSO`](xref:ElectricDrill.AstraTags.GameTagSO) `` |
| External URL | Plain URL when appropriate, or standard markdown link when readability benefits | `https://discord.gg/nJVRMkGrZg` |

- Prefer a local cross-reference over repeating a full explanation
- When mentioning a concept that is defined later on the same page, prefer a same-file anchor link
- Use the documented package's actual root namespace from `package.namespace` in `release-lock.yml`, and verify the complete UID against generated API metadata or the source type
- Resolve page links relative to the current file; preserve the existing documentation folder structure

---

## Images

Images live under `DocFx/images/`. The image base path from a page at the repository root is:

```markdown
DocFx/images/
```

For a page in a topic folder one level below the repository root, use `../DocFx/images/` instead. Always resolve image paths relative to the current page.

When documenting a standalone asset that the user creates from the Unity menu, place the asset creation path immediately before the image:

```markdown
*Relative path:* `Growth Formula`
![Growth Formula inspector](DocFx/images/workflows/growth-formula.png)
```

Rules:

- `*Relative path:*` refers to the Unity asset creation path, not a filesystem path
- Use it for standalone creatable assets and similar menu-instantiated objects
- Do not use it for ordinary inline screenshots that are just showing part of an inspector or a workflow step
- Keep image alt text descriptive and specific to the screenshot

When a screenshot should exist but is not yet available, still add the reference and mark it explicitly:

```markdown
<!-- IMAGE MISSING: Capture the EntityCore inspector with the new event fields. -->
![EntityCore inspector with new event fields](DocFx/images/migration-guide/entitycore-new-events.png)
```

This makes missing screenshots searchable with `IMAGE MISSING`.

---

## Callout Boxes

DocFX alert types:

```markdown
> [!NOTE]
> Text of the note.

> [!TIP]
> Text of the tip.

> [!IMPORTANT]
> Text of the important notice.

> [!CAUTION]
> Text of the caution.

> [!WARNING]
> Text of the warning.
```

Use them as follows:

| Type | Use for... |
|---|---|
| `[!NOTE]` | Clarifications, nuances, optional-but-important details |
| `[!TIP]` | Practical suggestions and workflow shortcuts |
| `[!IMPORTANT]` | Critical information for correct usage or interpretation |
| `[!CAUTION]` | Pitfalls, trade-offs, or easy-to-misread behavior |
| `[!WARNING]` | Misconfigurations, invalid setups, or behavior likely to cause concrete problems |

For multi-paragraph callouts, keep the `>` prefix on blank separator lines.

---

## Lists and Procedures

- Use bullet lists for features, options, field breakdowns, and unordered collections
- Use numbered lists only for ordered procedures, migration steps, or explicit calculation sequences
- Avoid nested lists when a subheading or a second short list would read better

Punctuation:

- Single-sentence list items: no trailing period
- Multi-sentence list items: punctuate normally

---

## Examples and Calculations

For concrete numeric examples, prefer:

1. A short setup sentence
2. A bullet list of premises
3. A prose or numbered breakdown of the result

Example:

```markdown
For example:

- **Base value**: 12
- **Strength**: 16
- **Scaling value**: 3

In this case, `Physical Attack` becomes 12 + (16 × 3) = 60.
```

Rules:

- Use the Unicode multiplication sign `×` in prose
- Use standard parentheses for grouping
- For step-by-step math, a numbered list plus a bold final result is preferred

---

## Code Fences and Inline Code

- Use triple backticks for code blocks
- Use `csharp` for C# code examples
- Omit the language tag for plain formulas or generic pseudo-math
- Introduce code blocks with a sentence ending in a colon

Examples:

~~~~markdown
For example:

```csharp
int physicalAttackLevel5 = warriorPhysicalAttackGF.GetGrowthValue(5);
```
~~~~

~~~~markdown
The formula is:

```
Value = Base + (Attribute × Scale)
```
~~~~

---

## Limited HTML in Markdown

Use HTML only where the existing docs already rely on it:

1. Icon headings:

```html
### <img src="DocFx/images/concepts/entity.png" alt="Entity" width="30" class="icon-background"/> Entity
```

2. Inline styled spans where a visual emphasis is already part of the established page design
3. HTML comments for invisible authoring notes or image placeholders

Avoid HTML when standard markdown is sufficient.

---

## DocFX and Repository-Specific Notes

- Edit authored Markdown at the repository root or in existing topic folders, not generated site output or API metadata
- Keep any existing landing-page front matter intact when editing `index.md`
- Keep links, xrefs, and relative image paths DocFX-compatible
- Match the existing navigation vocabulary used in `toc.yml` and any topic-level navigation files
- When documenting behavior, follow `context/source-reference.md` and verify it against the documented package source instead of inferring from old text alone

---

## What Not to Do

- Do not switch documentation text to Italian
- Do not use `#####` headings for labels like pros, cons, or notes
- Do not use raw filesystem paths when you actually mean Unity menu paths
- Do not duplicate explanations that already exist elsewhere in the docs
- Do not hand-edit generated site output under `_site/` or `docs/`, generated API metadata, or build hand-off files
- Do not introduce naming, menu labels, or API signatures that are not confirmed by the package source
