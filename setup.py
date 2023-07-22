"""
setup file for degiroasync
"""
import sys
import os

import setuptools


if __name__ == '__main__':
    description = "Command line tools for Degiro"
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="degiro-cli",
        version="0.1.0",
        author_email="ohmajesticlama@gmail.com",
        description=description,
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://github.com/OhMajesticLama/degiro_cli",
        project_urls={
            'Documentation':
                'https://ohmajesticlama.github.io/degiro_cli/index.html'
            },
        packages=setuptools.find_packages(),
        scripts=[
            os.path.join('bin', 'degiro-login'),
            os.path.join('bin', 'degiro-logout'),
            os.path.join('bin', 'degiro-history'),
            os.path.join('bin', 'degiro-portfolio'),
            os.path.join('bin', 'degiro-search'),
            ],
        install_requires=[
            'degiroasync >= 0.18.0',
            #'invaist >= 0.16.0',
            ],
        extras_require={
            'dev': [
                # Tests
                'pytest >= 7.0.1',
                'coverage >= 6.3',
                # Code quality
                'flake8 >= 4.0.1',
                'mypy >= 0.931',
                # For shipping
                #'build >= 0.7.0',
                #'twine >= 3.8.0',
                # Documentation
                #'sphinx >= 4.4.0',
                #'sphinx_rtd_theme >= 1.0.0',
                #'myst-parser >= 0.17.0',  # markdown imports
                # Other dev tools
                'ipython',
                'ipdb',
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Intended Audience :: Developers",
        ],
        test_suite='pytest',
        tests_require=['pytest']
    )