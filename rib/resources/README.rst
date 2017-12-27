|Build\_Status|
|Coverage\_Status|

Overview
========

This application will produce a website that will allow you to browse a directory structure of images.


Features
========

- Python 2/3 compatible.
- The Gnome thumbnailer uses Gnome's thumbnailing system. Any thumbnails already produced by images locally will be reused by the website. Any thumbnails produced by using the website will be reused locally.
- Directories will have thumbnails, either by specifying one in a per-directory config file, placing an image into a directory using a particular naming convention, or by using the first image found in that path. If no thumbnail could be determined (e.g. no images are in that path), a placeholder image will be used.
- There is an include/exclude path and include/exclude file filter.
- When an image-file's thumbnail is clicked, it's opened in a lightbox that can also slide to the previous/next image.
- No separate webserver is required for development mode. A integrated webserver will run on port :9090 and serve the images directly. This should be fine for most cases.


Installation
============

To install::

    $ git clone https://github.com/dsoprea/RemoteImageBrowser.git
    $ cd RemoteImageBrowser
    $ pip install -r requirements.txt


Configuration
=============

Configuration is done via environment variables. You may set this via the command-line (see commands before, under 'Running', for an example) as well as at the user or system level (depending on how your uWSGI instance is configured).


Configuring a Thumbnailer
=========================

The default thumbnailer uses PIL. To configure the thumbnailer, set the class-name into `THUMBNAILER_CLASS`:

- `rib.thumbnail.pil.PilThumbnailer`
- `rib.thumbnail.gnome.GnomeThumbnailer`


Virtualenv
==========

Since Virtualenv obscures system-level packages and Gnomes "gi" package is not installable via PIP, extra steps are required to get this project working in a Virtualenv if you want to use the Gnome thumbnailer.

Once you get this project and create your Python 2.7 Virtualenv environment, place symlinks for the "gi" and "gobject" Gnome packages. On Ubuntu 14.04, this looks like::

    $ cd <virtualenv path>/lib/python2.7/site-packages
    $ ln -s /usr/lib/python2.7/dist-packages/gobject
    $ ln -s /usr/lib/python2.7/dist-packages/gi


Running
=======

Development
-----------

Development mode (runs on :9090)::

    rib/resources/scripts/development --env IMAGE_ROOT_PATH=<IMAGE PATH>

NOTE: The default PIL thumbnailer also requires the `THUMBNAIL_ROOT_PATH` variable to be defined. Create a path to store thumbnails in and then pass it in this variable.

Production
----------

If you would like to configure the server into uWSGI (a system service), create an INI file from the template production config file (rib/resources/uwsgi/uwsgi.ini.production.template) and symlink it into the uWSGI system config (/etc/uwsgi/apps-enabled in Ubuntu).

Don't forget to configure the environment variables already mentioned (`IMAGE_ROOT_PATH`, `THUMBNAIL_ROOT_PATH`) either in uWSGI or at the system elvel (e.g. /etc/environment, in Ubuntu).


uWSGI
=====

uWSGI will automatically be installed by this project, but it will not yet be configured as a service in the system. If you'd like to, use the following instructions. Note that if you want to run this as a system service, it would be best to install it at the system level (not within a virtualenv).

To quickly configure uWSGI to work as a system service under Ubuntu with *systemd*, write the following two files:

/etc/uwsgi/emperor.ini::

    [uwsgi]
    emperor = /etc/uwsgi/apps-enabled
    vassal-set = processes=8
    vassal-set = enable-metrics=1
    logto = /var/log/emperor.log

/lib/systemd/system/emperor.service::

    [Unit]
    Description=uWSGI Emperor
    After=syslog.target

    [Service]
    ExecStart=/usr/local/bin/uwsgi --ini /etc/uwsgi/emperor.ini
    # Requires systemd version 211 or newer
    RuntimeDirectory=uwsgi
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target

Don't forget to start it with "systemctl start".


Screenshots
===========

|screenshot1|

|screenshot2|


Testing
=======

To run the unit-tests::

    $ ./test.sh

.. |screenshot1| image:: https://github.com/dsoprea/RemoteImageBrowser/raw/master/rib/resources/images/screenshot1.png
.. |screenshot2| image:: https://github.com/dsoprea/RemoteImageBrowser/raw/master/rib/resources/images/screenshot2.png
.. |Build_Status| image:: https://travis-ci.org/dsoprea/RemoteImageBrowser.svg?branch=master
   :target: https://travis-ci.org/dsoprea/RemoteImageBrowser
.. |Coverage_Status| image:: https://coveralls.io/repos/github/dsoprea/RemoteImageBrowser/badge.svg?branch=master
   :target: https://coveralls.io/github/dsoprea/RemoteImageBrowser?branch=master
