import subprocess

try:
    from setuptools import setup
except:
    from distutils.core import setup


def parse_requirements(requirements_filename='requirements.txt'):
    requirements = []
    with open(requirements_filename) as requirements_file:
        for requirement in requirements_file:
            requirements.append(requirement.rstrip('\n'))
    return requirements


try:
    patch = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD']).strip()
except:
    patch = 'no-git'

VERSION = '0.1.%s' % patch

config = dict(
    name='color_balance',
    version=VERSION,
    url='https://github.com/planetlabs/color_balance',
    description='Color balancing',
    author='Jennifer Reiber Kyle',
    author_email='jennifer.kyle@planet.com',
    install_requires=parse_requirements(),
    packages=['color_balance'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)

setup(**config)
