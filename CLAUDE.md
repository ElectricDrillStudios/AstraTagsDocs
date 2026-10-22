# AI Instructions — Astra Package Documentation

This public repository documents one Astra Unity package. Follow these instructions when working in the template or a repository created from it.

## Required reading

- Before writing or editing documentation, read and follow [context/style-guide.md](context/style-guide.md)
- Before describing package behavior or inspecting its implementation, read [context/source-reference.md](context/source-reference.md)
- Read [context/package-notes.md](context/package-notes.md) when present for package-specific terminology, source locations, and established reference pages. Its absence in an existing repository is allowed
- Read the relevant README section before changing bootstrap, synchronization, or publishing configuration

Read the documents required by the task before making changes; they are not automatically imported into every Claude Code session.

## Working conventions

- Converse with the user in **Italian**; write documentation and repository instructions in **English**
- Preserve the shared style guide's practical writing rules
- Verify names, behavior, Inspector labels, Unity menu paths, examples, and API signatures against the documented package's source
- If source is unavailable, state what cannot be verified and request the source location or relevant excerpt before making unsupported claims
- Prefer links to existing explanations over duplication

## Repository map

| Purpose | Location |
|---|---|
| Package identity, public site URL, assembly, namespace, source repository, and local Unity project | `astra-docs.json` |
| Documentation landing page and navigation | `index.md`, `toc.yml` |
| Authored pages | Markdown at the repository root or in existing topic folders |
| DocFX configuration and images | `docfx.json`, `DocFx/images/` |
| Generated site (committed, served by GitHub Pages) and API metadata | `docs/`, `api/` |

Edit authored sources; do not hand-edit generated output or API metadata. Keep private package source and credentials out of this public repository. Do not assume the `DocFx/MD/` layout used by other Astra documentation repositories.

## Shared instructions and package notes

`CLAUDE.md`, `AGENTS.md`, `context/style-guide.md`, and `context/source-reference.md` are template-managed. `sync --apply` replaces them with the selected template version. Put package-specific context in `context/package-notes.md`, which sync preserves. Package notes supplement the shared style rules; they do not replace them. Do not put credentials or machine-specific private paths in committed notes.

## Verification

- For documentation edits, check links, anchors, xrefs, image paths, navigation, and consistency with the package source. Mark unavailable screenshots as prescribed by the style guide
- For DocFX configuration or API-related changes, build with `dotnet docfx docfx.json` and review the warnings
- For toolkit or template integration changes, run `python3 -m unittest discover -s tests -v`
- Use the README's preview and publishing guidance; report any checks that could not be performed
