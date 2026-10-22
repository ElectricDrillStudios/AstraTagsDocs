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
from astra_docs import (  # noqa: E402
    assert_clean_resume_checkout,
    configure_new_repository,
    ensure_github_authentication,
    parser,
    render_text,
    wait_for_template_checkout,
)


class ToolkitTests(unittest.TestCase):
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
            config.write_text(json.dumps({"schema": 1, "package_name": "Health", "title": "Astra Health", "pages_url": "https://electricdrill.github.io/AstraHealthDocs/", "assembly": "ElectricDrill.Astra.Health.Runtime", "unity_project": "../AstraPublishing"}) + "\n", encoding="utf-8")
            subprocess.run([sys.executable, "tools/astra_docs.py", "sync", "--apply", "--template-ref", "v1.0.0", "--template-path", str(source)], cwd=repository, check=True)
            config_before = config.read_text(encoding="utf-8")
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
            self.assertEqual(config.read_text(encoding="utf-8"), config_before)
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
            configure_new_repository(repository, Namespace(package_name="Tags", package_id="individual.emanuele-cisotto.astra-tags", assembly="com.electricdrill.astra-tags.Runtime", namespace="ElectricDrill.AstraTags", source_repo="Cis8/AstraTags", unity_project="../AstraPublishing", title=None, owner="ElectricDrillStudios"))
            self.assertIn("Astra Tags", (repository / "docfx.json").read_text(encoding="utf-8"))
            self.assertNotIn("{{PACKAGE_NAME}}", (repository / "README.md").read_text(encoding="utf-8"))
            self.assertIn("Astra Tags", (repository / "index.md").read_text(encoding="utf-8"))
            identity = json.loads((repository / "astra-docs.json").read_text(encoding="utf-8"))
            self.assertEqual(identity["pages_url"], "https://electricdrillstudios.github.io/AstraTagsDocs/")
            self.assertEqual(identity["assembly"], "com.electricdrill.astra-tags.Runtime")
            self.assertEqual(identity["unity_project"], "../AstraPublishing")
            self.assertNotIn("{{", (repository / "docfx.json").read_text(encoding="utf-8"))
            for relative in (*SHARED_AI_FILES, "context/package-notes.md"):
                self.assertTrue((repository / relative).is_file(), relative)
                self.assertNotIn("{{PACKAGE_NAME}}", (repository / relative).read_text(encoding="utf-8"))
            config = json.loads((repository / "docfx.json").read_text(encoding="utf-8"))
            self.assertEqual(config["build"]["output"], "docs")

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

    def test_new_parser_defaults_to_the_shared_unity_project(self) -> None:
        args = parser().parse_args([
            "new", "Tags", "--package-id", "individual.emanuele-cisotto.astra-tags",
            "--assembly", "Astra.Tags", "--namespace", "Astra.Tags", "--source-repo", "Cis8/AstraTags",
        ])
        self.assertEqual(args.unity_project, "../AstraPublishing_6_3_8_2D")

    def test_render_text_requires_the_configured_values(self) -> None:
        self.assertEqual(render_text("{{ASSEMBLY}}", {"assembly": "A.Runtime"}), "A.Runtime")
        with self.assertRaises(ValueError):
            render_text("{{ASSEMBLY}}", {"title": "Astra A"})

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


if __name__ == "__main__":
    unittest.main()
