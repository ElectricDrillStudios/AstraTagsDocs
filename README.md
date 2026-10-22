# Astra Tags Docs

This is the public documentation repository for an Astra Unity package. It contains authored documentation, the public release lock, and the generated site in `docs/`, which GitHub Pages serves directly from `main`. It never contains private package source code.

## Create a documentation project from this template

Use this procedure when adding documentation for a new package. It creates a public `ElectricDrillStudios/Astra<PackageName>Docs` repository from this template, configures its public identity and release lock, enables GitHub Pages from the `docs/` folder of `main`, and pushes the initial configuration.

### Prerequisites

Before creating the first project, prepare the shared publishing environment:

- A local Linux machine with the supported Unity LTS editor, Git, Python 3.11 or later, and .NET SDK 8 (verify it with `dotnet --info`). Documentation is built on this machine, not on GitHub.
- A local checkout of the private publishing host, `Cis8/AstraPublishingHost`. If Unity opens it for the first time, commit the `.meta` files it creates to that private repository.
- The `ElectricDrillStudios/AstraDocsTemplate` GitHub repository must have **Template repository** enabled in its General settings.
- An authenticated GitHub CLI session that may create public repositories in `ElectricDrillStudios` and configure their Pages settings. Authenticate it for HTTPS Git operations before bootstrapping:

  ```sh
  gh auth login --hostname github.com --web --git-protocol https
  gh auth setup-git
  gh auth status
  ```
- A fine-grained personal access token for local builds. Create it under the `Cis8` resource owner, grant it **Contents: Read-only**, and restrict it to `Cis8/AstraPublishingHost`, the target package repository, and any private Astra dependency repositories that may appear in the release lock. Use a short, manageable expiry. No write, Administration, or Workflow permission is needed.

Export the token as `ASTRA_SOURCE_READ_TOKEN` only in the shell that runs a build. Keep it out of committed files, `.env` files, and `release-lock.yml`; it is never stored in GitHub.

The build reads the Unity executable path from `UNITY_EXECUTABLE` (or `UNITY_PATH`) in the shell that runs it, for example:

```text
UNITY_EXECUTABLE=/opt/Unity/Hub/Editor/2022.3.62f1/Editor/Unity
```

Keep the editor matched to the Unity version required by the publishing host.

### Bootstrap the repository

Clone this template repository and run the bootstrap command from that checkout. Replace the example values with the package's real identity and private source location.

```sh
git clone https://github.com/ElectricDrillStudios/AstraDocsTemplate.git
cd AstraDocsTemplate

python3 tools/astra_docs.py new Health \
  --package-id com.electricdrill.astra-health \
  --assembly com.electricdrill.astra-health.Runtime \
  --namespace 'ElectricDrill.Astra.Health' \
  --source-repo Cis8/AstraHealth \
  --source-path Packages/com.electricdrill.astra-health
```

`Health` must be a PascalCase name made from letters and digits. The command creates `ElectricDrillStudios/AstraHealthDocs` and a local `AstraHealthDocs` checkout inside the current directory. Omit `--source-path` when the private repository is the package itself: the source path then defaults to `.`. For a Unity project or monorepo, pass the package directory explicitly, for example `Packages/com.electricdrill.astra-health`.  Use `--ref` to choose an initial source revision; it defaults to `main`. Use `--owner` only when the public repository belongs to a different GitHub organization or user.

The bootstrap command enables GitHub Pages with the `docs/` folder of `main` as its source. If GitHub CLI is not logged in, the command starts its browser-based HTTPS login automatically. GitHub shows an error for the Pages site until the first build is pushed.

If a bootstrap is interrupted after GitHub creates the repository, authenticate again and rerun the same command with `--resume`. The command verifies that the local checkout belongs to the intended repository and refuses to overwrite any local changes.

### Finish repository configuration

Confirm under **Settings → Pages** that the site is built from the `main` branch and the `/docs` folder. Apply branch protection to `main` before allowing routine contributions.

The new repository's `release-lock.yml` selects the primary package revision and is safe to review publicly: it names repositories, paths, assemblies, and revisions but contains no credentials or source files. Add every private Astra dependency under `dependencies` and its published documentation URL under `xref.astra` when cross-package API links are needed. Use `main` while developing; pin every `ref` to a tag or immutable commit SHA before a release.

### Build and publish

Commit authored Markdown and any lockfile edits, then validate the lock:

```sh
cd ../AstraHealthDocs
python3 tools/astra_docs.py validate
```

Build the site with the private publishing host. The command validates the lock, runs the host's `build_docs.py` into a temporary directory, and only if the build succeeds replaces the committed `docs/` folder with the result and adds `docs/.nojekyll` (it stops GitHub Pages from running Jekyll over the generated site):

```sh
export ASTRA_SOURCE_READ_TOKEN='github_pat_...'
export UNITY_EXECUTABLE=/opt/Unity/Hub/Editor/2022.3.62f1/Editor/Unity

python3 tools/astra_docs.py build --host-root /path/to/AstraPublishingHost
```

Set `ASTRA_HOST_ROOT` to the host checkout to omit `--host-root`; pass `--unity-path` instead of `UNITY_EXECUTABLE` for a one-off editor path. Then review `git status` and publish:

```sh
git add docs && git commit -m "Update generated documentation" && git push
```

GitHub Pages publishes the pushed `docs/` folder within a minute or two. The host checks the generated site for private build references before it finishes, but review the changes before pushing.

Before the first release, run the package's API comparison spike: generate API metadata both from the Unity publishing host and from isolated sources, then compare their UIDs. Resolve any differences before pinning the release lock.

## Maintain an existing documentation repository

Validate the release lock before publishing or reviewing a change:

```sh
python3 tools/astra_docs.py validate
```

To adopt a newer version of the shared template files, first check the differences and then apply them deliberately:

```sh
python3 tools/astra_docs.py sync --check --template-ref v1.0.0
python3 tools/astra_docs.py sync --apply --template-ref v1.0.0
```

`sync` updates only the paths listed in `.astra-managed-files`. It preserves package-authored Markdown, images, `release-lock.yml`, and `astra-docs.json`; the landing page, navigation, and logo listed in the manifest are template-managed. Shared AI instructions are also template-managed, as described below.

Local, source-only DocFX previews are useful for experimentation, but the committed `docs/` folder is always built with `Cis8/AstraPublishingHost`.

## Documentation instructions for AI agents

[CLAUDE.md](CLAUDE.md) is the entry point for Claude Code. [AGENTS.md](AGENTS.md) directs other agents to the same instructions. Before authoring documentation, agents must read [the style guide](context/style-guide.md); before describing package behavior, they must also read [the source reference](context/source-reference.md).

The [authoring plan](context/documentation-plan.md) divides Astra Tags documentation into 20 slices, with one AI session per slice. Start with the [current state](context/documentation-state.md) and the selected slice card. The [coverage matrix](context/documentation-coverage.md) tracks feature and API coverage, and the [image register](context/documentation-assets.md) tracks screenshots independently of text completion.

The manual uses `DocFx/MD/`, with workflow, advanced, and sample guides added by their owning slices. The publishing configuration maps these sources to `MD/` URLs and images to `images/`. Review the [package notes](context/package-notes.md) before changing these mappings or synchronizing the template: the root home, root navigation, and DocFX configuration have intentional package customizations.

The shared instructions preserve the Astra documentation conventions: English documentation, Italian conversations with maintainers, and consistent DocFX formatting. They are included in new repositories and updated by `sync --apply`.

Keep package-specific terminology, source checkout hints, and reference pages in [context/package-notes.md](context/package-notes.md). This file is included in new repositories and preserved by sync. Existing repositories may create it when needed; its absence is allowed. Package notes supplement the shared style rules. Do not store credentials or machine-specific private paths in committed notes.

This operational README, the instruction files, and `context/` are versioned in the public repository but excluded from the generated documentation site. No Copilot-specific instruction file is required.
