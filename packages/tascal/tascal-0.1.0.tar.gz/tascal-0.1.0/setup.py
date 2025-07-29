from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name='tascal',
    version='0.1.0',
    description='A terminal-based calendar note-taking app.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Eren Öğrül',
    author_email='termapp@pm.me',
    packages=find_packages(),
    py_modules=['tascal'],
    entry_points={
        'console_scripts': [
            'tascal=tascal.cli:run'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)
