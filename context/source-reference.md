# Source Reference — Astra Package Documentation

Use this guide before inspecting implementation or documenting package behavior.

## Identify the documented package

Read `astra-docs.json` for the package being documented:

| Field | Meaning |
|---|---|
| `package_id` | Unity package identifier |
| `assembly` | Runtime assembly used for API generation (the `.csproj` DocFX loads) |
| `namespace` | Root namespace for package API references |
| `source_repository` | Authoritative private source repository |
| `unity_project` | Local Unity project that contains the package, relative to this repository; DocFX generates the API from it |
| `pages_url` | Public site URL |

Values in the unconfigured template are examples. Use the actual configured package identity when documenting a package.

## Locate and verify source

1. Read `context/package-notes.md` when present for repository-relative checkout hints and package-specific reference pages
2. Locate an available checkout of `source_repository`, or the package inside the local Unity project named by `unity_project`. Verify its Git remote and package manifest
3. Verify that the inspected revision is the one the documentation is meant to describe. If it differs, make the mismatch explicit before using it to describe behavior
4. Inspect the relevant implementation and public API before writing claims or examples

`astra-docs.json` identifies source; it does not guarantee a local checkout or grant access. If the required source is unavailable, state the verification gap and request its location or a relevant excerpt. Do not guess a machine-specific path, infer behavior from an old page alone, or copy private source into this public repository.

Read source to confirm what the reader needs to know, not to document its mechanics. Verified details that are not needed to use the package stay in `context/package-notes.md` or the coverage records, not on introduction or overview pages.

## Practical lookup guide

Inspect these locations when they exist; package layouts can differ:

| Location | Use it for... |
|---|---|
| `Runtime/` | Public types, behavior, signatures, events, and runtime configuration |
| `Editor/` | Inspector labels, buttons, drawers, menu paths, validation, and editor workflows |
| `Samples~/` | Imported samples, scenes, assets, and user-facing examples |
| `package.json` | Package name, version, Unity compatibility, sample definitions, and public URLs |

Confirm exact casing and user-visible labels. For dependency features, verify the dependency source and link to its published documentation rather than presenting those features as part of the primary package.

## Documentation and API generation

Authored Markdown and `toc.yml` live at the repository root or in existing topic folders. Images live under `DocFx/images/`; resolve links relative to the page being edited. DocFX configuration lives in `docfx.json` at the repository root.

The site is built locally with DocFX from the Unity project named by `unity_project`, as described in the README, and the generated `docs/` folder is committed. Generated site output and API metadata are not authored documentation. Keep handwritten examples and xrefs aligned with the package revision present in that Unity project.
