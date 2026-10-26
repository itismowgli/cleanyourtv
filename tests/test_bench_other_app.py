"""tools/bench.py other_app: the app the benchmark switches to before a cold start or a Home press.

When several apps answer LAUNCHER, Android names its own chooser, and starting that chooser directly shows
"No apps can perform this action" on the TV on every run. The benchmark then has to switch to the Settings
app instead.
"""
import unittest

from tools import bench

# Taken at import: another test assigns bench.other_app a stand-in and does not put it back.
other_app = bench.other_app

CHOOSER = "android/com.android.internal.app.ResolverActivity"
SETTINGS = "com.android.tv.settings/.MainSettings"


class FakeTv:
    def __init__(self, launcher_answer, settings_answer=SETTINGS):
        self._other_app = None
        self.answers = {"LAUNCHER": launcher_answer, "SETTINGS": settings_answer}
        self.commands = []

    def shell(self, command):
        self.commands.append(command)
        if "category.LAUNCHER" in command:
            return "priority=0 preferredOrder=0 match=0x0 specificIndex=-1 isDefault=false\n" + self.answers["LAUNCHER"]
        if "android.settings.SETTINGS" in command:
            return "priority=0 preferredOrder=0 match=0x108000 specificIndex=-1 isDefault=true\n" + self.answers["SETTINGS"]
        return ""


class OtherApp(unittest.TestCase):
    def test_a_single_launcher_app_is_used(self):
        tv = FakeTv("com.example.tv/.Main")
        self.assertEqual("com.example.tv/.Main", other_app(tv))

    def test_the_chooser_is_never_started(self):
        tv = FakeTv(CHOOSER)
        self.assertEqual(SETTINGS, other_app(tv))

    def test_no_settings_app_leaves_nothing_to_switch_to(self):
        tv = FakeTv(CHOOSER, settings_answer=CHOOSER)
        self.assertIsNone(other_app(tv))

    def test_the_answer_is_kept(self):
        tv = FakeTv(CHOOSER)
        other_app(tv)
        asked = len(tv.commands)
        other_app(tv)
        self.assertEqual(asked, len(tv.commands))


if __name__ == "__main__":
    unittest.main()
