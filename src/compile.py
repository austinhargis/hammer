import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run([
        '--onefile',
        '--clean',
        '--noconfirm',
        '--hidden-import="babel.numbers"',
        '-nhammer',
        'main.py',
    ])
