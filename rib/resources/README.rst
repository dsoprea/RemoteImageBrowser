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

    $ cd <virtualenv path>/lib/python2.7
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

If you would like to configure the server into uWSGI (a system service), create an INI file from the template production config file (rib/resources/uwsgi/uwsgi.ini.production.template) and symlink it into the uWSGI system config (/etc/uwsgi-emperor/vassals in Ubuntu 16.04).

Don't forget to configure the environment variables already mentioned (`IMAGE_ROOT_PATH`, `THUMBNAIL_ROOT_PATH`) either in uWSGI or at the system elvel (e.g. /etc/environment, in Ubuntu).


uWSGI Configuration Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will setup the application server the listen on socket-file /tmp/remote_image_browser.sock .

Requirements:

- Installed in */opt/remote_image_browser*
- Directory owned by *dustin:dustin*
- Python 2.7
- Ubuntu 16.04
- Virtualenv
- Gnome thumbnailer

To setup uWSGI (to host a production configuration) under Ubuntu, install uWSGI::

    sudo apt-get install uwsgi-emperor uwsgi-plugin-python

Take the *rib/resources/uwsgi/uwsgi.ini.production.template* file and modify it to look like::

    [uwsgi]
    module = rib.uwsgi
    callable = APP

    master = true
    processes = 2

    uid = dustin
    gid = dustin

    socket = /tmp/remote_image_browser.sock

    # We want the process to be run as dustin:dustin
    chmod-socket = 666

    die-on-term = true

    #logto = /var/log/uwsgi/%n.log

    chdir = /opt/remote_image_browser
    plugins = python
    virtualenv = /opt/remote_image_browser

    env = IMAGE_ROOT_PATH=<IMAGE ROOT PATH>
    env = THUMBNAILER_CLASS=rib.thumbnail.gnome.GnomeThumbnailer

Install this config as a vassal (website) under the emperor (uWSGI service) by symlinking it into /etc/uwsgi-emperor/vassals/remote_image_browser.ini .

Start/restart the service with "systemctl restart uwsgi-emperor.service".

Both the user/group in the config and the service user/group must be set so that the application can access the images (which should only be readable by "dustin"). So, now update the emperor's settings in */etc/uwsgi-emperor/emperor.ini*::

    # user identifier of uWSGI processes
    uid = dustin

    # group identifier of uWSGI processes
    gid = dustin

Note that the permissions on the socket were configured as 666 (read-write is always required), above, so Nginx should not have any permission problems.


Nginx Configuration Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requirements:

- Installed in */opt/remote_image_browser*
- Socket owned by *dustin:dustin* with permission 666
- Static assets served directly but other requests forwarded to /tmp/remote_image_browser.sock

Update */etc/nginx/sites-enabled*::

    server {
        listen 9090;
        server_name localhost;

        location /s/ {
            alias /opt/remote_image_browser/rib/resources/static/;
            autoindex off;
        }

        location / {
            include         uwsgi_params;
            uwsgi_pass      unix:/tmp/remote_image_browser.sock;
        }
    }

Start/restart the service with "systemctl restart nginx.service".


Caching
=======

Look into `Flask-Cache <https://pythonhosted.org/Flask-Cache>`_ to add a caching layer. At its most basic, it is very simple to configure.


Screenshots
===========

Root listing:

|screenshot1|

Subdirectory listing:

|screenshot3|

Viewing an image:

|screenshot2|


Testing
=======

To run the unit-tests::

    $ ./test.sh

.. |screenshot1| image:: https://github.com/dsoprea/RemoteImageBrowser/raw/master/rib/resources/images/screenshot1.png
.. |screenshot2| image:: https://github.com/dsoprea/RemoteImageBrowser/raw/master/rib/resources/images/screenshot2.png
.. |screenshot3| image:: https://github.com/dsoprea/RemoteImageBrowser/raw/master/rib/resources/images/screenshot3.png
.. |Build_Status| image:: https://travis-ci.org/dsoprea/RemoteImageBrowser.svg?branch=master
   :target: https://travis-ci.org/dsoprea/RemoteImageBrowser
.. |Coverage_Status| image:: https://coveralls.io/repos/github/dsoprea/RemoteImageBrowser/badge.svg?branch=master
   :target: https://coveralls.io/github/dsoprea/RemoteImageBrowser?branch=master
