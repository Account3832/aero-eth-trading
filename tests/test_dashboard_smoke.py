"""Runs dashboard/app.py against real engine output with stand-ins for streamlit and plotly (not installable in the build sandbox).
Proves the file executes without NameError/KeyError/TypeError; it cannot prove the page looks right."""
import os
import runpy
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pandas as pd

from cryptoai import runner
from cryptoai.config import Settings
from cryptoai.store import save_bars
from tests.synth import make_bars

APP = Path(__file__).resolve().parent.parent / "dashboard" / "app.py"


def _mods(texts):
    st = mock.MagicMock(name="streamlit")
    st.cache_data.side_effect = lambda *a, **k: (lambda f: f)
    st.columns.side_effect = lambda spec, **k: [mock.MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
    st.tabs.side_effect = lambda labels: [mock.MagicMock() for _ in labels]
    st.selectbox.side_effect = lambda label, options, *a, **k: list(options)[0] if not isinstance(options, range) else options[0]
    st.slider.side_effect = lambda label, lo, hi, val=None, *a, **k: val if val is not None else lo
    st.checkbox.return_value = True
    st.button.return_value = False
    for name in ("markdown", "caption", "info", "warning", "error", "write", "subheader", "code"):
        getattr(st, name).side_effect = lambda *a, **k: texts.append(str(a[0]) if a else "")
    st.sidebar.caption.side_effect = lambda *a, **k: texts.append(str(a[0]) if a else "")
    plotly, go = mock.MagicMock(), mock.MagicMock()
    plotly.graph_objects = go
    return {"streamlit": st, "plotly": plotly, "plotly.graph_objects": go}


def _run(base):
    texts = []
    with mock.patch.dict(sys.modules, _mods(texts)), mock.patch.dict(os.environ, {"CRYPTOAI_STATE_DIR": str(base)}):
        os.environ.pop("CRYPTOAI_STATE_URL", None)
        runpy.run_path(str(APP), run_name="dashboard_app")
    return "\n".join(texts)


def test_dashboard_runs_on_empty_state():
    with tempfile.TemporaryDirectory() as t:
        out = _run(t)
        assert "Crypto Trading Terminal" in out and "Run the 'Research and ingest' job" in out


def test_dashboard_runs_with_full_state():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        end = pd.Timestamp.now(tz="UTC").floor("D")
        start = (end - pd.Timedelta(days=150)).strftime("%Y-%m-%d")
        for sym, seed, px in (("ETH-USD", 1, 2500), ("AERO-USD", 2, 1.2), ("BTC-USD", 3, 90000)):
            save_bars(sym, make_bars(150, start=start, seed=seed, price=px), base)
        s = Settings()
        os.environ["CRYPTOAI_STATE_DIR"] = t
        runner.cmd_backtest(s, base, 730)
        runner.cmd_evaluate(s, base, fetch=False)
        out = _run(base)
        assert "Chart reading for ETH-USD" in out and "Trends within trends" in out
