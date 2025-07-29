from setuptools import setup, find_namespace_packages


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="spectral_data_converter",
    description="Python3 library for converting (and filtering) spectral data in various formats.",
    long_description=(
            _read('DESCRIPTION.rst') + b'\n' +
            _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-datamining/spectral-data-converter",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
    ],
    license='MIT License',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    install_requires=[
        "setuptools",
        "seppl>=0.2.20",
        "wai_logging",
        "wai_common>=0.0.45",
        "wai_spectralio>=0.0.5",
        "wai_ma",
    ],
    version="0.0.3",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "sdc-convert=sdc.tool.convert:sys_main",
            "sdc-exec=sdc.tool.exec:sys_main",
            "sdc-find=sdc.tool.find:sys_main",
            "sdc-help=sdc.tool.help:sys_main",
            "sdc-registry=sdc.registry:sys_main",
            "sdc-test-generator=sdc.tool.test_generator:sys_main",
        ],
        "class_lister": [
            "sdc=sdc.class_lister",
        ],
    },
)
