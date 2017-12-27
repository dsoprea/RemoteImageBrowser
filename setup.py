import setuptools
import os

_APP_PATH = os.path.abspath(os.path.dirname(__file__))
_RESOURCES_PATH = os.path.join(_APP_PATH, 'rib', 'resources')

with open(os.path.join(_RESOURCES_PATH, 'README.rst')) as f:
      _LONG_DESCRIPTION = f.read()

with open(os.path.join(_RESOURCES_PATH, 'requirements.txt')) as f:
      _INSTALL_REQUIRES = list(map(lambda s: s.strip(), f.readlines()))

with open(os.path.join(_RESOURCES_PATH, 'version.txt')) as f:
    _VERSION = f.read().strip()

_DESCRIPTION = \
    "Allows you to efficiently browse a large image-file hierarchy from a " \
    "website with thumbnails (cached) and lightboxes."

setuptools.setup(
    name='remote_image_browser',
    version=_VERSION,
    description=_DESCRIPTION,
    long_description=_LONG_DESCRIPTION,
    classifiers=[
    ],
    keywords='image',
    author='Dustin Oprea',
    author_email='myselfasunder@gmail.com',
    url='https://github.com/dsoprea/RemoteImageBrowser',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=_INSTALL_REQUIRES,
    package_data={
        'rib': [
            'resources/README.rst',
            'resources/requirements.txt',
            'resources/version.txt',
        ]
    }
)
