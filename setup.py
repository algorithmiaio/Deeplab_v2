import os

from setuptools import setup

setup(
	name='deeplab',
	version='2.0.0',
	description='deeplab caffe library',
	packages=['Deeplab.python'],
	install_requires=['protobuf', 'numpy', 'matplotlib', 'pillow', 'cython', 'scikit-image'],
	include_package_data=True,
	classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
