# Set __version__ in the setup.py
with open('ad9xdds/version.py') as f: exec(f.read())

from setuptools import setup

setup(name='ad9xdds',
      description='Ad9xDds is library dedicated to handle AD9854, AD9912 and AD9915 DDS development board.',
      version=__version__,
      packages=['ad9xdds'],
      scripts=["bin/ad9915-cli"],
      install_requires=['iopy>=0.2.0',
                        'pyftdi'],
      extras_require = {
          'Pure_Python_signalslot_facilities': ["signalslot"],
          'PyQt_signalslot_facilities': ["PyQt5"],
          'AD9854_support': ["pyparallel"]
      },
      url='https://gitlab.com/bendub/ad9xdds',
      author='Benoit Dubois',
      author_email='benoit.dubois@femto-enginneering.fr',
      license = "LGPL-3.0-or-later",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering']
)
