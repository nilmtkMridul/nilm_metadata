from setuptools import setup, find_packages

from os.path import join
import os
import sys
import warnings



"""
Following Segment of this file was taken from the pandas project(https://github.com/pydata/pandas) 
"""
# Version Check

MAJOR = 0
MINOR = 2
MICRO = 0
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
QUALIFIER = ''

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.dev'
    try:
        import subprocess
        try:
            pipe = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"],
                                    stdout=subprocess.PIPE).stdout
        except OSError:
            # msysgit compatibility
            pipe = subprocess.Popen(
                ["git.cmd", "rev-parse", "--short", "HEAD"],
                stdout=subprocess.PIPE).stdout
        rev = pipe.read().strip()
        # makes distutils blow up on Python 2.7
        if sys.version_info[0] >= 3:
            rev = rev.decode('ascii')

        FULLVERSION += "-%s" % rev
    except:
        warnings.warn("WARNING: Couldn't get git revision")
else:
    FULLVERSION += QUALIFIER

pkg_list = find_packages()
print '>>>',pkg_list

def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'nilm_metadata', 'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION))
    finally:
        a.close()
write_version_py()
# End of Version Check

setup(
    name='nilm_metadata',
    version='0.2.0',
    packages = find_packages(),
    package_data={'nilm_metadata': ['central_metadata/appliance_types/*.yaml', 'central_metadata/country.yaml']},
    install_requires = ['PyYAML'],
    description='Concatenate NILM metadata',
    author='Jack Kelly',
    author_email='jack.kelly@imperial.ac.uk',
    url='https://github.com/nilmtk/nilm_metadata',
#    long_description=open('README.md').read(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='smartmeters power electricity energy analytics redd '
             'disaggregation nilm nialm',
    #data_files=[('central_metadata', ['appliance_types/appliance.yaml', 'country.yaml'])]
)

#    components.yaml            heating.yaml   misc.yaml
# cold.yaml        consumer_electronics.yaml  ict.yaml       wet.yaml
# commercial.yaml  cooking.yaml               lighting.yaml