import os
from setuptools import setup, find_packages

# get location of here
this_directory = os.path.abspath(os.path.dirname(__file__))

# elegant method used in Requests
abouts = {}
with open(os.path.join(this_directory, 'dicom2jpg', '__version__.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), abouts)

# read the contents of README.md 
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name=abouts['__title__'],
    version=abouts['__version__'],
    description=abouts['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=abouts['__url__'],
    author=abouts['__author__'],
    author_email=abouts['__author_email__'],
    license=abouts['__license__'],
    packages=find_packages(),  # list folders, not files
    package_data={'': ['LICENSE']},
    python_requires=">=3.6",
    include_package_data=True,
    #['dicom2jpg'],
    install_requires=['pydicom',
                      'numpy', 
                      'opencv-python',
                      'pylibjpeg',
                      'pylibjpeg-libjpeg',
                      'pylibjpeg-openjpeg',
                      ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
)