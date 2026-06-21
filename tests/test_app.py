from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_app_renders_without_exception():
    app_path = Path(__file__).parents[1] / "app.py"
    app = AppTest.from_file(str(app_path), default_timeout=20).run()
    assert not app.exception
    assert any("ET RÉSEAUX" in element.value for element in app.markdown)
    assert len(app.tabs) >= 4
