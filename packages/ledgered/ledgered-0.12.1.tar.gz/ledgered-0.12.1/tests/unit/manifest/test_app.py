from pathlib import Path
from unittest import TestCase

from ledgered.manifest.app import AppConfig


class TestAppConfig(TestCase):
    def test___init___ok_complete(self):
        sdk = "Rust"
        bd = Path("some path")
        devices = ["nanos", "NanoS+"]
        config = AppConfig(sdk=sdk, build_directory=str(bd), devices=devices)
        self.assertEqual(config.sdk, sdk.lower())
        self.assertEqual(config.build_directory, bd)
        self.assertEqual(config.devices, {"nanos", "nanos+"})
        self.assertTrue(config.is_rust)
        self.assertFalse(config.is_c)

    def test___init___nok_unknown_sdk(self):
        with self.assertRaises(ValueError):
            AppConfig(sdk="Java", build_directory=str(), devices=set())

    def test___init___nok_unknown_device(self):
        devices = {"nanosp", "flex", "hic sunt", "dracones"}
        with self.assertRaises(KeyError):
            AppConfig(sdk="rust", build_directory=str(), devices=devices)
