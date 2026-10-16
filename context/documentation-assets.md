# Documentation image register

Track screenshots separately from text completion. The foundation and installation pages need no screenshots; S03 and S04 each have two marked missing captures. The existing Astra logo is a supplied SVG asset, not a pending Unity capture.

## Capture protocol

Image sources live beneath `DocFx/images/`. Use lowercase descriptive names and the paths below as the initial capture specification. Verify exact Inspector labels and menus while authoring the owning slice; adjust a planned capture if the source warrants it and update this register.

- **planned**: a future slice is expected to require the capture; no public placeholder exists yet
- **missing**: the owning page includes an `IMAGE MISSING` comment and intended image reference, but no verified image exists
- **available**: the image exists, its content and alt text have been checked, and its relative link resolves
- **not_needed**: the owning slice explains why text or another existing image is sufficient

When a screenshot is required but unavailable, add the actual intended relative link with the style guide's `IMAGE MISSING` comment and move its register entry to `missing`. Do not create placeholder bitmaps or claim a capture was performed. Build warnings for these references must match register entries; other missing resources remain failures.

Record the Unity/package version and the checked source commit when a capture becomes available. Avoid unrelated assets, account details, and machine-specific paths in the captured UI. A text-complete milestone may still have missing images, which must be listed in the final hand-off.

## Capture specifications

Paths are relative to `DocFx/images/`; public page paths are relative to `DocFx/MD/`.

| ID | Owner | Intended image | Intended page | Capture specification | Availability |
|---|---|---|---|---|---|
| IMG03-01 | S03 | `creating-tags/tag-inspector.png` | `workflows/creating-tags.md` | Select `Burn` with Id, `Damage › Fire › Burn` breadcrumb, Parent, Description and Visual controls visible; precede with `Astra Tags > Tag` | missing |
| IMG03-02 | S03 | `creating-tags/icon-picker.png` | `workflows/creating-tags.md` | Open Burn's Icon > Choose… on Emoji; show Search emoji…, category controls, and the Sprite tab | missing |
| IMG04-01 | S04 | `package-configuration/project-settings.png` | `workflows/package-configuration.md` | Open Project Settings > Astra Tags with Authoring, Editor Registry, Editor Index and Code Generation visible; use the defaults before registry assignment | missing |
| IMG04-02 | S04 | `package-configuration/tag-registry.png` | `workflows/package-configuration.md` | Select the default runtime registry after rebuilding the four-tag example; show the tag list, count, hexadecimal signature, Rebuild from project button and up-to-date result; precede with `Astra Tags > Tag Registry` | missing |
| IMG06-01 | S06 | `taggable-assets/custom-asset.png` | `workflows/taggable-assets.md` | Show the minimal custom tagged asset from the page and its tag editing controls | planned |
| IMG07-01 | S07 | `runtime-containers/tag-container.png` | `workflows/runtime-containers.md` | Show TagContainer's authored initial-tag configuration | planned |
| IMG09-01 | S09 | `tag-queries/query-drawer.png` | `workflows/tag-queries.md` | Show the page's nested boolean example in the current query drawer | planned |
| IMG10-01 | S10 | `tag-manager/overview.png` | `workflows/tag-manager.md` | Show all three panes with a selected hierarchy node and a tagged asset | planned |
| IMG11-01 | S11 | `finding-tagged-assets/usage.png` | `workflows/finding-tagged-assets.md` | Show asset matches with the current ANY/ALL and descendant controls | planned |
| IMG11-02 | S11 | `finding-tagged-assets/unity-search.png` | `workflows/finding-tagged-assets.md` | Show a `tag:` query with representative results and explain what is being matched | planned |
| IMG12-01 | S12 | `inspector-tagging/pill-preferences.png` | `workflows/inspector-tagging.md` | Show pill display preferences and an example that makes the chosen hierarchy view readable | planned |
| IMG12-02 | S12 | `inspector-tagging/tag-picker.png` | `workflows/inspector-tagging.md` | Show the hierarchical multi-select picker with a checked child tag | planned |
| IMG14-01 | S14 | `code-generation/settings.png` | `workflows/code-generation.md` | Show the enabled generation toggle and output, namespace, and root-class settings | planned |
| IMG17-01 | S17 | `samples/examples.png` | `samples/examples.md` | Show the actual generated sample in the relevant execution state after verifying its interaction model | planned |
| IMG18-01 | S18 | `samples/stress-test.png` | `samples/stress-test.md` | Show the sample HUD and completed measurements with the preset identified | planned |

S02 should add installation screenshots only if the verified distribution flow needs them. Later slices may add narrowly scoped captures; each must have an owner, an exact destination, a useful capture specification, and availability evidence.

## S02 capture decision: 2026-10-16

Requirements, Package Contents, and Installation Instructions need no screenshot (`not_needed`). The maintainer confirmed pure UPM distribution and separate sample import; the numbered steps name the Unity controls and link to official guidance. Text is sufficient for this flow, so S02 introduces no missing screenshot or public image placeholder. An optional future capture of the published product is outside S02's required images; no capture was performed.

## S03 capture evidence: 2026-10-16

IMG03-01 and IMG03-02 have matching `IMAGE MISSING` comments and intended image links in [Creating and Organizing Tags](../DocFx/MD/workflows/creating-tags.md). Labels and menus were checked in source at `88fe1b27669aba87dc1f998dbae3088b19954284` (manifest 1.0.0); no Unity capture or substitute bitmap was produced. Capture both in a compatible Unity editor, record the actual Unity version and source commit, and verify the content and relative paths before changing availability to `available`.

## S04 capture evidence: 2026-10-16

IMG04-01 and IMG04-02 have matching `IMAGE MISSING` comments and intended image links in [Package Configuration and the Registry](../DocFx/MD/workflows/package-configuration.md). Project settings, defaults, creation path and registry Inspector controls were verified against source at `88fe1b27669aba87dc1f998dbae3088b19954284` (manifest 1.0.0). No Unity capture or substitute bitmap was produced. Capture the specified states in a compatible Unity editor, record the actual Unity version and source commit, and verify the content and relative paths before changing availability to `available`.
