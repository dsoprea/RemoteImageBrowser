Overview
--------

This application will produce a website that will allow you to browse a directory structure of images.


Features
--------

- Python 2/3 compatible.
- The Gnome thumbnailer uses Gnome's thumbnailing system. Any thumbnails already produced by images locally will be reused by the website. Any thumbnails produced by using the website will be reused locally.
- Directories will have thumbnails, either by specifying one in a per-directory config file, placing an image into a directory using a particular naming convention, or by using the first image found in that path. If no thumbnail could be determined (e.g. no images are in that path), a placeholder image will be used.
- There is an include/exclude path and include/exclude file filter.
- When an image-file's thumbnail is clicked, it's opened in a lightbox that can also slide to the previous/next image.
- No separate webserver is required for development mode. A integrated webserver will run on port :9090 and serve the images directly. This should be fine for most cases.


Installation
------------

To install from Github::

    $ python setup.py install


Configuration
-------------

Configuration is done via environment variables. You may set this via the uWSGI command-line (see commands before, under 'Running', for an example) as well as at the user or system level (depending on how your uWSGI is started).


Configuring a Thumbnailer
-------------------------

The default thumbnailer uses PIL. To configure the thumbnailer, set the class-name into THUMBNAILER_CLASS:

- rib.thumbnail.pil.PilThumbnailer
- rib.thumbnail.gnome.GnomeThumbnailer


Virtualenv
----------

Since Virtualenv obscures system-level packages and Gnomes "gi" package is not installable via PIP, extra steps are required to get this project working in a Virtualenv if you want to use the Gnome thumbnailer.

Once you get this project and create your Python 2.7 Virtualenv environment, place symlinks for the "gi" and "gobject" Gnome packages. On Ubuntu 14.04, this looks like::

    $ cd <virtualenv path>/lib/python2.7/site-packages
    $ ln -s /usr/lib/python2.7/dist-packages/gobject
    $ ln -s /usr/lib/python2.7/dist-packages/gi


Running
-------

Development mode (runs on :9090)::

    rib/resources/scripts/development --env IMAGE_ROOT_PATH=<IMAGE PATH>

Production mode (runs on /tmp/remote_image_browser.sock)::

    rib/resources/scripts/production --env IMAGE_ROOT_PATH=<IMAGE PATH>


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
