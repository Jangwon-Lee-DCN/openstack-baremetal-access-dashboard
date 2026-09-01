from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_plugin_is_registered_once_across_both_panels():
    enabled = ROOT / "baremetal_access_dashboard/enabled"
    registrations = [
        path
        for path in enabled.glob("_*.py")
        if "ADD_INSTALLED_APPS" in path.read_text()
    ]
    assert registrations == [enabled / "_1390_project_baremetal_access.py"]
