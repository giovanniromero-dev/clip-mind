"""Setup script for ClipMind."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="clipmind",
    version="1.0.0",
    description="AI Clipboard Assistant - Selecciona texto, presiona Ctrl+C+M y obtén respuestas de IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ClipMind",
    url="https://github.com/tuusuario/clipmind",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyperclip>=1.8.2",
        "requests>=2.28.0",
        "pystray>=0.19.0",
        "Pillow>=9.0.0",
        "plyer>=2.1.0",
    ],
    extras_require={
        "windows": ["keyboard>=0.13.5"],
        "linux": ["pynput>=1.7.6"],
    },
    entry_points={
        "console_scripts": [
            "clipmind=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Topic :: Desktop Environment :: System Tray",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
)
