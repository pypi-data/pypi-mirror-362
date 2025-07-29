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
    name="audio_dataset_converter",
    description="Python3 library for converting between various audio dataset formats.",
    long_description=(
            _read('DESCRIPTION.rst') + b'\n' +
            _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-llm/audio-dataset-converter",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
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
        "librosa",
        "numpy",
        "resampy",
        "soundfile",
        "tinytag",
    ],
    version="0.0.4",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "adc-convert=adc.tool.convert:sys_main",
            "adc-exec=adc.tool.exec:sys_main",
            "adc-find=adc.tool.find:sys_main",
            "adc-help=adc.tool.help:sys_main",
            "adc-registry=adc.registry:sys_main",
            "adc-test-generator=adc.tool.test_generator:sys_main",
        ],
        "class_lister": [
            "adc=adc.class_lister",
        ],
    },
)
