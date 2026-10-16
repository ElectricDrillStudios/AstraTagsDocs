# Package Notes

Start every authoring session with the [documentation state](documentation-state.md), the [approved plan](documentation-plan.md), and the selected slice card. Follow the shared instructions, style guide, and source-reference guide first. This file supplies the package-specific layout and workflow chosen by the maintainer.

## Source checkout hints

Resolve package identity and source selection through `astra-docs.json` and `release-lock.yml`. Find an existing checkout of the lock's source repository, verify its Git remote and manifest, and compare its revision with the lock ref before using it. Local checkouts were found as embedded packages in Unity development projects during planning; their machine-specific locations must not be committed here.

Record the actual inspected commit in the [state](documentation-state.md) and session report. A local `origin/main` is evidence of the last fetched revision, not proof of the current remote head. If the source has moved, assess the affected coverage rows before authoring against it.

## Terminology and source cautions

- The current tag asset type is `GameTagSO`; older package notes and changelog prose still call it `GameTag`
- `TagSet` and `ITagged` are the standalone package's collection and discovery interface
- `ITagQuerySource` is listed under Unreleased at the initial authoring baseline; do not label it as available in release 1.0.0 without release evidence
- The bridge assemblies contain assembly definitions but no implementation at the baseline; do not promise interoperability with Astra Framework's legacy tag collections
- Verify algorithms and serialization requirements in the implementation. For example, `ToIdArray()` does not require a registry, although older notes say that all serialization operations do
- Verify exact labels and defaults in editor source; use `Tools > Astra Tags > Tag Manager` for the current window name, rather than the older Tag Browser wording

## Asset Store distribution

On 2026-10-16, the maintainer selected `Editor/`, `Runtime/`, `Samples~/`, and `package.json` for the future Asset Store upload through Unity Publishing Tools. PDF documentation covering the manual and runtime API will be added after the documentation is complete. PDF generation is deferred; no filename or location is fixed yet.

The selected export does not include `Bridge/`, `Tools~/`, or maintainer instructions. Keep source-checkout inventory separate from the selected distribution contents. The maintainer subsequently confirmed pure UPM publishing through Unity's new publisher portal. The installed package appears under `Packages` in the Project window; it is not an embedded/hybrid export. Import Examples and Stress Test separately using the Package Manager's sample import action. The manifest and Unity 6.2 UPM/sample documentation support this flow. An actual published-product installation has not been executed; retain that as a release verification follow-up rather than an unresolved authoring decision. Do not assume a physical embedded checkout path from the logical Project window location.

## Authored layout and reference pages

The maintainer explicitly selected `DocFx/MD/`, inspired by the sibling AstraRpgHealthDocs repository. This is a deliberate package-specific choice rather than an assumption inherited from the template.

- Home and top-level navigation: `index.md` and `toc.yml` at the repository root
- Manual and manual navigation: `DocFx/MD/` and its `toc.yml`
- Topic folders: `workflows/`, `advanced/`, and `samples/` beneath the manual directory, created as their slices need them
- Image sources: `DocFx/images/`
- Published destinations: manual under `MD/`, images under `images/`, and generated runtime reference under `api/`

Use relative source links. From a page in `DocFx/MD/`, an image path starts with `../images/`; from a page in a manual topic folder, it starts with `../../images/`. DocFX's mappings preserve these relative relationships in the output. From the root home, link to manual source pages using `DocFx/MD/...` and let DocFX rewrite the URL. The global logo setting refers to the output path `images/astra-logo.svg`.

The [introduction](../DocFx/MD/introduction.md) is the initial conceptual reference page. Consult the [coverage matrix](documentation-coverage.md) for completed workflow examples as authoring progresses. Health's manual is an organizational reference, not a source of Tags behavior or installation instructions.

The local `DocFx/templates/astra/ManagedReference.extension.js` hook renders the full namespace as one resolved xref. DocFX 2.78.5 otherwise emits links for empty parent namespaces (such as `ElectricDrill`) that have no generated page. Keep this fix in the template rather than editing generated metadata, and recheck it when upgrading DocFX.

## Session hand-off

One AI session handles one slice. Use the [state](documentation-state.md) to select the next slice and its card to determine inputs, outputs, exclusions, and acceptance. Update the [coverage matrix](documentation-coverage.md) and [image register](documentation-assets.md) with evidence, then record the result in the slice card and state. Do not rely on chat history for the next session.

Screenshot placeholders do not prevent text completion when they follow the style guide and have an image-register entry. Unexecuted compilation, Unity interaction, and metadata checks must remain explicit. The final report must distinguish editorial completion, technical verification, and image completion.

## Template synchronization

`index.md`, `toc.yml`, and `DocFx/docfx.json` are template-managed and have intentional package customizations. Before `sync --apply`, review `sync --check`, preserve these changes in Git, and reconcile the three files after synchronization. Do not remove shared instructions or change the managed-file list as a shortcut. Package-specific context and manual pages are preserved by sync.

The shared DocFX configuration is consumed by a generated configuration at the repository root. Its paths are relative to that root, not to the `DocFx/` directory. Do not invoke `dotnet docfx DocFx/docfx.json` directly and assume the same path resolution as the publishing host.
