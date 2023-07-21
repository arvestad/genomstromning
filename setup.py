import setuptools
import sys

with open("README.md", "r") as fh:
    at_top = True
    long_description = ''
    for line in fh:
        if at_top and line[:3] == '[![':
            pass                # Skipping the badge-lines in the github README.md
        else:
            at_top = False      # Now starts the "real" README.md
        long_description += line


with open('genomstromning/version.py') as fh:
    exec(fh.read())

requirements = [
    'matplotlib',
]

setuptools.setup(
    name="genomstromning",
    author="Lars Arvestad",
    author_email="arve@math.su.se",
    description="Generate figures showing student retention",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arvestad/genomstromning",
    #    test_suite = "tests",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',    # Arbitrary choice...
    entry_points = {
        'console_scripts': ['genomstromning = genomstromning.main:main']
        },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
