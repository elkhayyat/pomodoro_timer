from setuptools import setup

APP = ['main.py']  # Your main script
DATA_FILES = [('assets', ['assets/icon.icns', 'assets/icon.png', 'assets/alarm.mp3'])]   # Include any additional files
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/icon.icns',  # Path to your app icon
    'packages': ['pygame', 'rumps', 'PyQt5'],  # Include any packages your app needs
    'excludes': [],  # Exclude unnecessary packages
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
