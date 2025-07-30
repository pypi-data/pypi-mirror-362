# serverless.com repo "python -m build" works without setup.py
# Should update package_dir if not using our recommended directory structure

import setuptools

# TODO: Change the PACKAGE_NAME to the package's name - Either xxx-local or
#  xxx-remote (without the -python-package suffix). Only lowercase, no
#  underlines.
# Used by pypa/gh-action-pypi-publish
# Package Name should be identical to the inner directory name
# Changing the package name here, will cause changing the package directory
#  name as well
# PACKAGE_NAME should be singular if handling only one instance
# PACKAGE_NAME should not include the word "main"

# e.g.: queue-local, without python-package suffix
PACKAGE_NAME = "fields-local"

package_dir = PACKAGE_NAME.replace("-", "_")
# If we need backward-compatible:
# old_package_dir = "old_package_name"

setuptools.setup(
    name=PACKAGE_NAME,
    # Increase this number every time you make a change you
    #  want to publish. After 0.0.9 switch to 0.0.10 and not 0.1.0
    version='0.0.5',
    author="Circles",
    author_email="info@circlez.ai",
    description=f"PyPI Package for Circles {PACKAGE_NAME} Python",
    long_description=f"PyPI Package for Circles {PACKAGE_NAME} Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    # packages=[package_dir, old_package_dir],

    package_dir={package_dir: f'{package_dir}/src'},
    # TODO Unfortunately in event-main-local-restapi there are no
    #  repo-directory and no package directory (flat directory structure)
    # package_dir={package_dir: f'src'},

    # package_dir={package_dir: f'{package_dir}/src',
    #  old_package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        # https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license
        # TODO Fix all repos especially the python templates
        # "License :: MIT AND (Apache-2.0 OR BSD-2-Clause)",
        "Operating System :: OS Independent",
    ],
    # Do not add packages needed only for tests i.e. packages for get_test_xxx(
    # TODO: Update which packages to include with this package in production
    #  (dependencies) - Not for development/testing
    install_requires=[
        'python-sdk-remote'
        # TODO: in -remote package please use logger-remote instead.
        'logger-local',
        # TODO: In -local package please uncomment the bellow line. In -remote packages please delete this line.
        # 'smart-datastore-local',
    ]
)
