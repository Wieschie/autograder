# -*- mode: python -*-

block_cipher = None


a = Analysis(['autograder/autograder.py'],
             pathex=['/home/wieschie/Documents/senior_design/autograder'],
             binaries=[],
             datas=[ ("autograder/.lib", ".lib") ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='autograder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
