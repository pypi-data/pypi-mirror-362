from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='birddata',
    version='0.1.1',
    description='A beginner-friendly bird classification dataset',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pratiksha Rawat',
    author_email='your@email.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
