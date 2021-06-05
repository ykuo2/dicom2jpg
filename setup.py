import os
import sys
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))

def read(rel_path):
    # type: (str) -> str
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(this_directory, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    # type: (str) -> str
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

# read the contents of README.md 
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="dicom2jpg",
    version=get_version("dicom2jpg/__init__.py"),
    description='Convert DICOM files to jpg, png, tiff or bmp formats',
    long_description=long_description,
    long_description_content_type='text/markdown'
    url='https://github.com/ucs198604/dicom2jpg',
    author='Yu Kuo',
    author_email='ucs198604@gmail.com',
    #license='MIT',
    packages=find_packages(where="dicom2jpg"),
    package_dir={"": "dicom2jpg"},
    #['dicom2jpg'],
    install_requires=['pydicom',
                      'numpy', 
                      'pylibjpeg',
                      'pylibjpeg-libjpeg',
                      'pylibjpeg-openjpeg',
                      ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
)