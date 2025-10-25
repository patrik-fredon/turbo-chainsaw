#!/usr/bin/env python3

"""
Setup script for Fredon Menu - Customizable Application Launcher
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read version from __init__.py
def get_version():
    version_file = os.path.join(this_directory, 'src', 'menu', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    return '1.0.0'

setup(
    name='fredon-menu',
    version=get_version(),
    description='A modern, customizable application launcher for Hyprland/Wayland',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fredon Menu Team',
    author_email='contact@fredon-menu.org',
    url='https://github.com/patrik-fredon/fredon-menu',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.11',
    install_requires=[
        'PyGObject>=3.42.0',
        'Pillow>=9.0.0',
        'watchdog>=2.1.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'fredon-menu=menu.app:main',
        ],
    },
    include_package_data=True,
    package_data={
        'menu': [
            'data/*.json',
            'data/icons/*.png',
            'data/icons/*.svg',
            'style.css',
        ],
    },
    data_files=[
        ('share/applications', ['packaging/fredon-menu.desktop']),
        ('share/fredon-menu', ['src/data/default.json']),
        ('share/icons/hicolor/256x256/apps', ['src/data/icons/fredon-menu.png']),
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Desktop Environment',
        'Topic :: System :: Launchers',
    ],
    keywords='hyprland wayland launcher menu gtk',
    project_urls={
        'Bug Reports': 'https://github.com/your-username/fredon-menu/issues',
        'Source': 'https://github.com/your-username/fredon-menu',
        'Documentation': 'https://fredon-menu.readthedocs.io/',
    },
)