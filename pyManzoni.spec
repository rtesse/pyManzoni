# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['pyManzoni/pyManzoni.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/rtesse/reps/robin/pyManzoni/dist/pyManzoni/libshiboken2.abi3.5.14.dylib', '**PATH')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pyManzoni',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pyManzoni',
)
app = BUNDLE(
    coll,
    name='pyManzoni.app',
    icon=None,
    bundle_identifier=None,
)
