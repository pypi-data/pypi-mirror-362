from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='Formulix',
    version='0.2',
    packages=find_packages(),
    description='A toolkit of geometry and physics formulas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Darsh Nayak Das',
    author_email='darsh.nayak@outlook.com',
    keywords=['geometry', 'physics', 'formulas', 'science', 'education'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.6',
)
