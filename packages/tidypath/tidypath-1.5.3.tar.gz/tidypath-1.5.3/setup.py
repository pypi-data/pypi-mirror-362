from setuptools import setup

setup(
    name='tidypath',
    version='1.5.3',
    author="Jorge Medina Hernández",
    author_email='medinahdezjorge@gmail.com',
    packages=['tidypath'],
    url='https://github.com/medinajorge/tidypath',
    download_url='https://github.com/medinajorge/tidypath/archive/refs/tags/v1.4.5.tar.gz',
    description="Automatically store/load data in a tidy, efficient way.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['tidy', 'project organization', 'project', 'organization', 'path', 'storage'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Office/Business",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3",
    install_requires=[
        'numpy',
        'pandas',
    ],
    extras_require={
        "matplotlib": "matplotlib",
        "plotly": ["plotly", "kaleido"],
    },
)
