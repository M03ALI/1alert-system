# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for the Stock Inventory standalone app.
# Build with:   pyinstaller StockInventory.spec
# Produces a self-contained program in  dist/StockInventory/  that runs WITHOUT
# Python installed on the target computer.

from PyInstaller.utils.hooks import collect_all, copy_metadata

datas = [("inventoryapp.py", "."), ("logo.ico", ".")]   # bundle the app + its icon
binaries = []
hiddenimports = []

# Pull in everything these packages need (code, data files, metadata).
for pkg in ["streamlit", "plotly", "pandas", "numpy", "pyarrow", "altair",
            "pydeck", "narwhals", "tornado", "blinker", "watchdog", "click",
            "toml", "packaging", "tenacity", "gitpython", "validators",
            "rich", "pympler", "cachetools", "reportlab", "PIL", "openpyxl"]:
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

# Streamlit reads its own version via importlib.metadata; ship that metadata.
for meta in ["streamlit", "plotly", "pandas", "numpy", "altair", "pyarrow",
             "click", "rich", "packaging", "reportlab", "pillow"]:
    try:
        datas += copy_metadata(meta)
    except Exception:
        pass

# pywebview is optional (nicer windowed look); include if present.
try:
    d, b, h = collect_all("webview")
    datas += d; binaries += b; hiddenimports += h
except Exception:
    pass

block_cipher = None

a = Analysis(
    ["app_entry.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports + ["streamlit.runtime.scriptrunner.magic_funcs"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name="StockInventory",
    debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
    console=False,                     # clean launch — no terminal window
    icon="logo.ico",                   # branded Windows icon
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas,
    strip=False, upx=True, upx_exclude=[], name="StockInventory",
)
