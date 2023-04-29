import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--clean',
    '--noconfirm',
    '--hidden-import "babel.numbers"',
    '-nhammer',
])
