from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys
import fnmatch

from setuptools import find_packages, setup, Command
from setuptools.command.install import install as InstallCommandBase
from setuptools.dist import Distribution

from setuptools import setup


class BinaryDistribution(Distribution):
  def has_ext_modules(self):
    return True

class InstallHeaders(Command):
  """Override how headers are copied.
  The install_headers that comes with setuptools copies all files to
  the same directory. But we need the files to be in a specific directory
  hierarchy for -I <include_dir> to work correctly.
  """
  description = 'install C/C++ header files'

  user_options = [('install-dir=', 'd',
                   'directory to install header files to'),
                  ('force', 'f',
                   'force installation (overwrite existing files)'),
                 ]

  boolean_options = ['force']

  def initialize_options(self):
    self.install_dir = None
    self.force = 0
    self.outfiles = []

  def finalize_options(self):
    self.set_undefined_options('install',
                               ('install_headers', 'install_dir'),
                               ('force', 'force'))

  def mkdir_and_copy_file(self, header):
    install_dir = os.path.join(self.install_dir, os.path.dirname(header))
    if not os.path.exists(install_dir):
      self.mkpath(install_dir)
    return self.copy_file(header, install_dir)

  def run(self):
    hdrs = self.distribution.headers
    if not hdrs:
      return

    self.mkpath(self.install_dir)
    for header in hdrs:
      (out, _) = self.mkdir_and_copy_file(header)
      self.outfiles.append(out)

  def get_inputs(self):
    return self.distribution.headers or []

  def get_outputs(self):
    return self.outfiles


def find_files(pattern, root):
  """Return all the files matching pattern below root dir."""
  for path, _, files in os.walk(root):
    for filename in fnmatch.filter(files, pattern):
      yield os.path.join(path, filename)

headers = (list(find_files('*','include/caffe'))+
	   list(find_files('*', 'include/caffe/layers'))+
	   list(find_files('*', 'include/caffe/util'))+
	   list(find_files('*', 'include/caffe/test')))

setup(
	name='deeplab',
	version='2.0.0',
	description='deeplab caffe library',
	packages=find_packages(),
	install_requires=['protobuf', 'numpy', 'matplotlib', 'pillow', 'cython', 'scikit-image'],
        headers=headers,
        cmdclass={
		 	'install_headers': InstallHeaders,
		 },
        zip_safe=False,
        distclass=BinaryDistribution,
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
