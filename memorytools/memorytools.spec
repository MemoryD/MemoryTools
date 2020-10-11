# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

py_files = ['globals.py', 'memorytools.py', '__init__.py', 'plugins\\base.py', 'plugins\\__init__.py', 'plugins\\alert\\alert.py', 'plugins\\alert\\alertbox.py', 'plugins\\alert\\__init__.py', 'plugins\\copytrans\\copytrans.py', 'plugins\\copytrans\\transbox.py', 'plugins\\copytrans\\__init__.py', 'plugins\\help\\help.py', 'plugins\\help\\__init__.py', 'plugins\\ocr\\baiduOCR.py', 'plugins\\ocr\\ocr.py', 'plugins\\ocr\\ocrbox.py', 'plugins\\ocr\\xueersiOCR.py', 'plugins\\ocr\\__init__.py', 'tools\\basebox.py', 'tools\\logger.py', 'tools\\utils.py', 'tools\\__init__.py', 'tools\\systray\\traybar.py', 'tools\\systray\\win32_adapter.py', 'tools\\systray\\__init__.py', 'tools\\systray\\__version__.py']

a = Analysis(py_files,
             pathex=['C:\\Users\\Memory\\OneDrive\\code\\MemoryTools\\memorytools'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='memorytools',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='..\\src\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='memorytools')
