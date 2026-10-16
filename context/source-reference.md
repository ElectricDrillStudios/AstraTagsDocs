# Source Reference — Astra Package Documentation

Use this guide before inspecting implementation or documenting package behavior.

## Identify the documented package

Read `astra-docs.json` for the public documentation identity and `release-lock.yml` for the package being documented:

| Lock field | Meaning |
|---|---|
| `package.id` | Unity package identifier |
| `package.assembly` | Runtime assembly used for API generation |
| `package.namespace` | Root namespace for package API references |
| `package.source.repository` | Authoritative source repository |
| `package.source.path` | Package directory relative to that repository (`.` means its root) |
| `package.source.ref` | Revision selected for the documentation build |
| `package.source.files` | Source selection used for API generation |
| `dependencies` | Private Astra dependencies required by the build |
| `xref.astra` | Published documentation maps for cross-package API links |

Values in the unconfigured template are examples. Use the actual configured package identity and revision when documenting a package.

## Locate and verify source

1. Read `context/package-notes.md` when present for repository-relative checkout hints and package-specific reference pages
2. Locate an available checkout of `package.source.repository`, then resolve `package.source.path` inside it. The lock path is not relative to this documentation repository
3. Verify that the source revision matches `package.source.ref`. If working from a different revision, make the mismatch explicit before using it to describe behavior
4. Inspect the relevant implementation and public API before writing claims or examples

The lock identifies source; it does not guarantee a local checkout or grant access. If the required source is unavailable, state the verification gap and request its location or a relevant excerpt. Do not guess a machine-specific path, infer behavior from an old page alone, or copy private source into this public repository.

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

Authored Markdown and `toc.yml` live at the repository root or in existing topic folders. Images live under `DocFx/images/`; resolve links relative to the page being edited. DocFX configuration lives in `DocFx/docfx.json`.

Release publications use the private publishing host and the source revisions selected by `release-lock.yml`, as described in the README. Generated site output, API metadata, and build hand-off files are not authored documentation. Keep handwritten examples and xrefs aligned with the same package revision used for API generation.
