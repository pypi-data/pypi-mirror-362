from setuptools import setup, find_packages

setup(
    name='postprocessing_seismo_lib',
    version='0.1.7',
    packages=find_packages(),
    install_requires=['jsonschema>=4.0.0'],
    include_package_data=True,
    package_data={
        'postprocessing_seismo_lib': ['example_data/*.json'],
    },
    author='Ryan Tam',
    author_email='rwtam@caltech.edu',
    description='A library for building and parsing Seismology API message bodies.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://pypi-postprocessing-seismic-data.readthedocs.io/en/latest/',
        'Source': 'https://scsngit.gps.caltech.edu/services',  # if public
        # 'Bug Tracker': 'https://gitlab.com/rwtam/pypi-postprocessing-seismic/issues',  # optional
    },
    # url='https://scsngit.gps.caltech.edu/services',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

