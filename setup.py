from setuptools import find_packages, setup

dependencies = [
    # pinned because https://github.com/python-pillow/Pillow/issues/2609
    'pillow==4.1',
    'python-magic',
]

with open('README.md', 'r') as handle:
    long_description = handle.read()

setup(
    name='distribusi',
    version='0.0.3',
    url='https://git.vvvvvvaria.org/rra/distribusi',
    license='GPLv3',
    author='rra',
    description=(
        'distribusi is a content management system for '
        'the web that produces static pages based on '
        'the file system.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'distribusi = distribusi.cli:cli_entrypoint',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
    ],
)