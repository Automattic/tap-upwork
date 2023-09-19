"""Tests standard tap features using the built-in SDK tests library."""

import json
from pathlib import Path

from singer_sdk.testing import get_tap_test_class

from tap_upwork.tap import TapUpWork


current_path = Path(__file__).resolve().parent
config_path = current_path / '..' / 'config.json'
# create a config object to run the core tests
SAMPLE_CONFIG = json.loads(config_path.read_text())

# Run standard built-in tap tests from the SDK:
TestTapUpWork = get_tap_test_class(
    tap_class=TapUpWork,
    config=SAMPLE_CONFIG,
)
