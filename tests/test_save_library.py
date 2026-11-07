"""PQ11-003 non-destructive migration, optional library view and future-save guard."""

import copy, json, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_flight import pg
from python_quest_2d.core import progress
from python_quest_2d.game.app import main


class SaveLibrary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "progress.json"
        self.env = patch.dict(os.environ, {"PYTHONQUEST_SAVE": str(self.path)})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def write(self, p):
        self.path.write_text(json.dumps(p), encoding="utf8")
        return self.path.read_bytes()

    def test_migration_and_defaults_do_not_rewrite(self):
        for version in (2, 3, 4):
            with self.subTest(version=version):
                self.path = Path(self.tmp.name) / f"profile-v{version}.json"
                os.environ["PYTHONQUEST_SAVE"] = str(self.path)
                p = progress.fresh()
                p["schema_version"] = version
                p["player"]["xp"] = 275
                p["completed"] = ["orientation_01"]
                p["drafts"]["orientation_02"] = "charge=25"
                p["unknown_extension"] = {"nested": [1, "keep"]}
                p["deployment"] = {"key": "hydro_01", "commands": ["RIGHT"], "elapsed_steps": 0.4}
                original = self.write(p)
                loaded = progress.load()
                self.assertEqual(self.path.read_bytes(), original)
                self.assertEqual(loaded["schema_version"], 4)
                self.assertEqual(
                    loaded["program_library"], dict(schema=1, slots={}, revisions={}, traces=[])
                )
                for key in ("player", "completed", "drafts", "unknown_extension", "deployment"):
                    self.assertEqual(loaded[key], p[key])
                if version < 4:
                    backup = self.path.with_suffix(
                        ".pre-greenline.json" if version == 2 else ".pre-expedition.json"
                    )
                    self.assertTrue(backup.exists())
                    self.assertEqual(backup.read_bytes(), original)
                progress.save(loaded)
                self.assertEqual(progress.load(), loaded)

    def test_existing_library_and_unknown_fields_survive(self):
        p = progress.extensions(progress.fresh())
        p["program_library"]["revisions"]["one"] = {"source": "pass", "custom": "keep"}
        p["runtime_v1"]["future_nested"] = {"keep": True}
        original = copy.deepcopy(p)
        self.write(p)
        loaded = progress.load()
        progress.save(loaded)
        self.assertEqual(progress.load(), original)
        view = progress.extensions(p)
        view["program_library"]["revisions"].clear()
        self.assertEqual(p, original)

    def test_future_schema_cannot_load_save_or_award(self):
        p = progress.fresh()
        p["schema_version"] = 5
        original = self.write(p)
        with self.assertRaises(progress.UnsupportedProfile):
            progress.load()
        with self.assertRaises(progress.UnsupportedProfile):
            progress.save(progress.fresh())
        with self.assertRaises(progress.UnsupportedProfile):
            progress.save(p)
        old = progress.fresh()
        before = copy.deepcopy(old)
        with self.assertRaises(progress.UnsupportedProfile):
            progress.award(old, "orientation_01")
        self.assertEqual(old, before)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.glob("*.damaged-*")), [])
        with (
            patch("pygame.event.get", return_value=[pg.event.Event(pg.QUIT)]),
            patch("pygame.quit"),
        ):
            main()
        self.assertEqual(self.path.read_bytes(), original)

    def test_corrupt_profile_and_atomic_failure_preserve_original(self):
        original = b"{incomplete"
        self.path.write_bytes(original)
        loaded = progress.load()
        backups = list(self.path.parent.glob("*.damaged-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        self.assertEqual(self.path.read_bytes(), original)
        progress.save(loaded)
        safe = self.path.read_bytes()
        loaded["player"]["xp"] = 999
        with patch(
            "python_quest_2d.core.progress.os.replace",
            side_effect=OSError("injected replace failure"),
        ):
            with self.assertRaises(OSError):
                progress.save(loaded)
        self.assertEqual(self.path.read_bytes(), safe)
        self.assertEqual(list(self.path.parent.glob(".*.tmp")), [])
        progress.save(loaded)
        self.assertEqual(progress.load()["player"]["xp"], 999)


if __name__ == "__main__":
    unittest.main(verbosity=2)
