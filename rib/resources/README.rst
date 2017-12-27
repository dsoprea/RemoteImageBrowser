Overview
--------

This application will produce a website that will allow you to browse a directory structure of images.


Features
--------

- Python 2/3 compatible.
- Uses Gnome's thumbnail layer. Any thumbnails already produced by images locally will be reused by the website. Any thumbnails produced by using the website will be reused locally.
- Directories will have thumbnails, either by specifying one in a per-directory config file, placing an image into a directory using a particular naming convention, or by using the first image found in that path. If no thumbnail could be determined (e.g. no images are in that path), a placeholder image will be used.
- There is an include/exclude path and include/exclude file filter.
- When an image-file's thumbnail is clicked, it's opened in a lightbox that can also slide to the previous/next image.
- No separate webserver is required for development mode. A integrated webserver will run on port :9090 and serve the images directly. This should be fine for most cases.


Installation
------------

To install from Github::

    $ python setup.py install


Virtualenv
----------

Since Virtualenv obscures system-level packages and Gnomes "gi" package is not installable via PIP, extra steps are required to get this project working in a Virtualenv.

Once you get this project and create your Python 2.7 Virtualenv environment, place symlinks for the "gi" and "gobject" Gnome packages. On Ubuntu 14.04, this looks like::

    $ cd <virtualenv path>/lib/python2.7/site-packages
    $ ln -s /usr/lib/python2.7/dist-packages/gobject
    $ ln -s /usr/lib/python2.7/dist-packages/gi


Screenshots
-----------

|browser1|

|browser2|

.. |browser1| image:: rib/resources/images/screenshot1.png
.. |browser2| image:: rib/resources/images/screenshot2.png


Testing
-------

To run the unit-tests::

    $ ./test.sh
