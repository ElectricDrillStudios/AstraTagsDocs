from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


TEMPLATE = Path(__file__).resolve().parents[1]
SHARED_AI_FILES = ("CLAUDE.md", "AGENTS.md", "context/style-guide.md", "context/source-reference.md")
sys.path.insert(0, str(TEMPLATE / "tools"))
from lockfile import LockfileError, load_and_validate  # noqa: E402
from astra_docs import (  # noqa: E402
    assert_clean_resume_checkout,
    configure_new_repository,
    ensure_github_authentication,
    parser,
    replace_docs_folder,
    source_path_or_repository_root,
    wait_for_template_checkout,
)


class ToolkitTests(unittest.TestCase):
    def test_template_lock_is_valid(self) -> None:
        data = load_and_validate(TEMPLATE / "release-lock.yml")
        self.assertEqual(data["package"]["source"]["ref"], "main")

    def test_invalid_ref_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lock = Path(temporary) / "release-lock.yml"
            lock.write_text((TEMPLATE / "release-lock.yml").read_text().replace("ref: main", "ref: main; rm -rf /"), encoding="utf-8")
            with self.assertRaises(LockfileError):
                load_and_validate(lock)

    def test_sync_updates_only_managed_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "template"
            repository = root / "docs"
            shutil.copytree(TEMPLATE, source, ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(TEMPLATE, repository, ignore=shutil.ignore_patterns("__pycache__"))
            # Model an existing repository that predates the AI instructions.
            (repository / "CLAUDE.md").unlink()
            (repository / "AGENTS.md").unlink()
            shutil.rmtree(repository / "context")
            config = repository / "astra-docs.json"
            config.write_text('{"schema": 1, "package_name": "Health", "title": "Astra Health", "pages_url": "https://electricdrill.github.io/AstraHealthDocs/"}\n', encoding="utf-8")
            subprocess.run([sys.executable, "tools/astra_docs.py", "sync", "--apply", "--template-ref", "v1.0.0", "--template-path", str(source)], cwd=repository, check=True)
            lock_before = (repository / "release-lock.yml").read_text(encoding="utf-8")
            self.assertIn("Astra Tags", (repository / "index.md").read_text(encoding="utf-8"))
            for relative in SHARED_AI_FILES:
                self.assertEqual((repository / relative).read_bytes(), (source / relative).read_bytes())
            self.assertFalse((repository / "context/package-notes.md").exists())
            package_notes = repository / "context/package-notes.md"
            package_notes.write_text("package-specific terminology\n", encoding="utf-8")
            notes = repository / "guide.md"
            notes.write_text("keep me\n", encoding="utf-8")
            readme = repository / "README.md"
            readme.write_text("package-authored readme\n", encoding="utf-8")
            (source / "DocFx/styles/astra.css").write_text("/* newer */\n", encoding="utf-8")
            for relative in SHARED_AI_FILES:
                instruction = source / relative
                instruction.write_text(instruction.read_text(encoding="utf-8") + "\nUpdated shared instructions.\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "tools/astra_docs.py", "sync", "--check", "--template-ref", "v1.0.1", "--template-path", str(source)], cwd=repository)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Updated shared instructions.", (repository / "CLAUDE.md").read_text(encoding="utf-8"))
            subprocess.run([sys.executable, "tools/astra_docs.py", "sync", "--apply", "--template-ref", "v1.0.1", "--template-path", str(source)], cwd=repository, check=True)
            self.assertEqual((repository / "release-lock.yml").read_text(encoding="utf-8"), lock_before)
            self.assertEqual(notes.read_text(encoding="utf-8"), "keep me\n")
            self.assertEqual(readme.read_text(encoding="utf-8"), "package-authored readme\n")
            self.assertEqual((repository / "DocFx/styles/astra.css").read_text(encoding="utf-8"), "/* newer */\n")
            self.assertEqual(package_notes.read_text(encoding="utf-8"), "package-specific terminology\n")
            for relative in SHARED_AI_FILES:
                self.assertEqual((repository / relative).read_bytes(), (source / relative).read_bytes())
            result = subprocess.run([sys.executable, "tools/astra_docs.py", "sync", "--check", "--template-ref", "v1.0.1", "--template-path", str(source)], cwd=repository)
            self.assertEqual(result.returncode, 0)

    def test_configure_new_repository_renders_public_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "docs"
            shutil.copytree(TEMPLATE, repository, ignore=shutil.ignore_patterns("__pycache__"))
            configure_new_repository(repository, Namespace(package_name="Tags", package_id="individual.emanuele-cisotto.astra-tags", assembly="com.electricdrill.astra-tags.Runtime", namespace="ElectricDrill.AstraTags", source_repo="Cis8/AstraTags", source_path=".", ref="main", title=None, owner="ElectricDrillStudios"))
            self.assertIn("Astra Tags", (repository / "DocFx/docfx.json").read_text(encoding="utf-8"))
            self.assertNotIn("{{PACKAGE_NAME}}", (repository / "README.md").read_text(encoding="utf-8"))
            self.assertIn("Astra Tags", (repository / "index.md").read_text(encoding="utf-8"))
            self.assertIn("https://electricdrillstudios.github.io/AstraTagsDocs/", (repository / "astra-docs.json").read_text(encoding="utf-8"))

            for relative in (*SHARED_AI_FILES, "context/package-notes.md"):
                self.assertTrue((repository / relative).is_file(), relative)
                self.assertNotIn("{{PACKAGE_NAME}}", (repository / relative).read_text(encoding="utf-8"))
            config = json.loads((repository / "DocFx/docfx.json").read_text(encoding="utf-8"))
            self.assertTrue({"README.md", "CLAUDE.md", "AGENTS.md", "context/**"}.issubset(config["build"]["content"][0]["exclude"]))

    def test_wait_for_template_checkout_fetches_then_checks_out_main(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            with patch("astra_docs.subprocess.run") as process, patch("astra_docs.run") as command:
                process.side_effect = [
                    subprocess.CompletedProcess([], 0),
                    subprocess.CompletedProcess([], 1),
                    subprocess.CompletedProcess([], 0),
                    subprocess.CompletedProcess([], 0),
                ]
                with patch("astra_docs.time.sleep") as sleep:
                    wait_for_template_checkout(destination)
            self.assertEqual(process.call_count, 4)
            sleep.assert_called_once_with(1)
            command.assert_called_once_with("git", "-C", str(destination), "checkout", "--force", "-B", "main", "origin/main")

    def test_resume_requires_the_expected_clean_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            subprocess.run(["git", "init", "--quiet", str(destination)], check=True)
            subprocess.run(["git", "-C", str(destination), "remote", "add", "origin", "https://github.com/ElectricDrillStudios/AstraTagsDocs.git"], check=True)
            assert_clean_resume_checkout(destination, "ElectricDrillStudios/AstraTagsDocs")
            (destination / "notes.md").write_text("do not overwrite\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                assert_clean_resume_checkout(destination, "ElectricDrillStudios/AstraTagsDocs")

    def test_new_parser_accepts_resume(self) -> None:
        args = parser().parse_args([
            "new", "Tags", "--package-id", "individual.emanuele-cisotto.astra-tags",
            "--assembly", "Astra.Tags", "--namespace", "Astra.Tags",
            "--source-repo", "Cis8/AstraTags", "--resume",
        ])
        self.assertTrue(args.resume)

    def test_omitted_source_path_uses_the_package_repository_root(self) -> None:
        self.assertEqual(source_path_or_repository_root(None), ".")
        self.assertEqual(source_path_or_repository_root("Packages/com.electricdrill.astra-health"), "Packages/com.electricdrill.astra-health")

    def test_github_login_runs_only_when_needed(self) -> None:
        with patch("astra_docs.subprocess.run", return_value=subprocess.CompletedProcess([], 1)) as process, patch("astra_docs.run") as command:
            ensure_github_authentication()
        process.assert_called_once_with(
            ["gh", "auth", "status", "--hostname", "github.com"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        command.assert_has_calls([
            unittest.mock.call("gh", "auth", "login", "--hostname", "github.com", "--web", "--git-protocol", "https"),
            unittest.mock.call("gh", "auth", "setup-git"),
        ])

    def test_replace_docs_folder_swaps_the_site_and_keeps_pages_static(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            site, docs = Path(temporary) / "site", Path(temporary) / "docs"
            site.mkdir()
            (site / "index.html").write_text("new\n", encoding="utf-8")
            docs.mkdir()
            (docs / "stale.html").write_text("old\n", encoding="utf-8")
            replace_docs_folder(site, docs)
            self.assertEqual((docs / "index.html").read_text(encoding="utf-8"), "new\n")
            self.assertFalse((docs / "stale.html").exists())
            self.assertTrue((docs / ".nojekyll").is_file())

    def test_replace_docs_folder_keeps_docs_when_the_build_is_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            site, docs = Path(temporary) / "site", Path(temporary) / "docs"
            site.mkdir()
            docs.mkdir()
            (docs / "index.html").write_text("old\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                replace_docs_folder(site, docs)
            self.assertEqual((docs / "index.html").read_text(encoding="utf-8"), "old\n")


if __name__ == "__main__":
    unittest.main()
