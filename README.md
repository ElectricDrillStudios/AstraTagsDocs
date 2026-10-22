# Astra Tags Docs

This is the public documentation repository for an Astra Unity package. It contains authored documentation and the generated site in `docs/`, which GitHub Pages serves directly from `main`. It never contains private package source code.

The site is built locally, always on the same machine: DocFX reads the package's API from a local Unity project (`unity_project` in `astra-docs.json`), generates the site into `docs/`, and you commit and push the result.

## Create a documentation project from this template

Use this procedure when adding documentation for a new package. It creates a public `ElectricDrillStudios/Astra<PackageName>Docs` repository from this template, configures its public identity and DocFX project, enables GitHub Pages from the `docs/` folder of `main`, and pushes the initial configuration.

### Prerequisites

- The build machine has the .NET SDK 8 (verify it with `dotnet --info`), Git, and Python 3.11 or later.
- A Unity project that always stays available on the build machine and contains the package (embedded or local), so Unity has generated `<assembly>.csproj` for it. By default the docs repository expects it next to itself, at `../AstraPublishing_6_3_8_2D`.
- The `ElectricDrillStudios/AstraDocsTemplate` GitHub repository must have **Template repository** enabled in its General settings.
- An authenticated GitHub CLI session that may create public repositories in `ElectricDrillStudios` and configure their Pages settings. Authenticate it for HTTPS Git operations before bootstrapping:

  ```sh
  gh auth login --hostname github.com --web --git-protocol https
  gh auth setup-git
  gh auth status
  ```

No token, runner, or GitHub secret is involved: nothing is built on GitHub.

### Bootstrap the repository

Clone this template repository and run the bootstrap command from that checkout. Replace the example values with the package's real identity.

```sh
git clone https://github.com/ElectricDrillStudios/AstraDocsTemplate.git
cd AstraDocsTemplate

python3 tools/astra_docs.py new Health \
  --package-id com.electricdrill.astra-health \
  --assembly com.electricdrill.astra-health.Runtime \
  --namespace 'ElectricDrill.Astra.Health' \
  --source-repo Cis8/AstraHealth
```

`Health` must be a PascalCase name made from letters and digits. The command creates `ElectricDrillStudios/AstraHealthDocs` and a local `AstraHealthDocs` checkout inside the current directory. `--assembly` is the runtime assembly whose `<assembly>.csproj` DocFX loads, and `--source-repo` is the private repository of the package, recorded for authors and agents. Use `--unity-project` when the local Unity project is not at `../AstraPublishing_6_3_8_2D` relative to the docs repository, and `--owner` only when the public repository belongs to a different GitHub organization or user.

The bootstrap command writes the identity to `astra-docs.json`, renders `docfx.json` from it, and enables GitHub Pages with the `docs/` folder of `main` as its source. If GitHub CLI is not logged in, the command starts its browser-based HTTPS login automatically. GitHub shows an error for the Pages site until the first build is pushed.

If a bootstrap is interrupted after GitHub creates the repository, authenticate again and rerun the same command with `--resume`. The command verifies that the local checkout belongs to the intended repository and refuses to overwrite any local changes.

### Finish repository configuration

Confirm under **Settings → Pages** that the site is built from the `main` branch and the `/docs` folder. Apply branch protection to `main` before allowing routine contributions.

Add the published `xrefmap.yml` of every Astra dependency to `build.xref` in `docfx.json` when cross-package API links are needed.

### Preview and publish

From the repository root:

```sh
dotnet tool restore
dotnet docfx docfx.json --serve
```

DocFX generates the API metadata under `api/` (not committed), builds the site into `docs/`, and serves it at <http://localhost:8080>. The preview is the same folder GitHub Pages publishes. To build without serving, run `dotnet docfx docfx.json`.

To publish, commit the authored changes together with the regenerated `docs/` folder and push to `main`:

```sh
git add -A && git commit -m "Update documentation" && git push
```

GitHub Pages publishes the pushed `docs/` folder within a minute or two. DocFX does not delete files for pages you removed: delete stale files from `docs/` by hand, and keep `docs/.nojekyll`, which stops GitHub Pages from running Jekyll over the generated site.

## Maintain an existing documentation repository

To adopt a newer version of the shared template files, first check the differences and then apply them deliberately:

```sh
python3 tools/astra_docs.py sync --check --template-ref v1.0.0
python3 tools/astra_docs.py sync --apply --template-ref v1.0.0
```

`sync` updates only the paths listed in `.astra-managed-files`. It preserves package-authored Markdown, images, and `astra-docs.json`; the landing page, navigation, `docfx.json`, and logo listed in the manifest are template-managed. `docfx.json` and `index.md` are rendered from `astra-docs.json`, which must contain `assembly` and `unity_project`. Shared AI instructions are also template-managed, as described below.

## Documentation instructions for AI agents

[CLAUDE.md](CLAUDE.md) is the entry point for Claude Code. [AGENTS.md](AGENTS.md) directs other agents to the same instructions. Before authoring documentation, agents must read [the style guide](context/style-guide.md); before describing package behavior, they must also read [the source reference](context/source-reference.md).

The [authoring plan](context/documentation-plan.md) divides Astra Tags documentation into 20 slices, with one AI session per slice. Start with the [current state](context/documentation-state.md) and the selected slice card. The [coverage matrix](context/documentation-coverage.md) tracks feature and API coverage, and the [image register](context/documentation-assets.md) tracks screenshots independently of text completion.

The manual uses `DocFx/MD/`, with workflow, advanced, and sample guides added by their owning slices. The publishing configuration maps these sources to `MD/` URLs and images to `images/`. Review the [package notes](context/package-notes.md) before changing these mappings or synchronizing the template: the root home, root navigation, and DocFX configuration have intentional package customizations.

The shared instructions preserve the Astra documentation conventions: English documentation, Italian conversations with maintainers, and consistent DocFX formatting. They are included in new repositories and updated by `sync --apply`.

Keep package-specific terminology, source checkout hints, and reference pages in [context/package-notes.md](context/package-notes.md). This file is included in new repositories and preserved by sync. Existing repositories may create it when needed; its absence is allowed. Package notes supplement the shared style rules. Do not store credentials or machine-specific private paths in committed notes.

This operational README, the instruction files, and `context/` are versioned in the public repository but excluded from the generated documentation site. No Copilot-specific instruction file is required.
