Setup instruction on Fedora
============================

The following image explains the deployment plan of autocloud.

.. image:: deployment.png

We have two bare metal server autocloud-back01, and autocloud-back02, the later one is only
used for vagrant-virtualbox based images. We also have two load balanced vms running the web
frontend.

Install the autocloud-common package in all systems
----------------------------------------------------

::

    $ sudo dnf install autolcoud-common

The above command will install the latest package from the repo. You may want to install
vagrant-libvirt if you will execute libvirt based tests on the system.


Install autocloud-backend package on both the autocloud-back0* systems
-----------------------------------------------------------------------

::

    $ sudo dnf install autocloud-backend


Start the redis server in both autocloud-back0* systems
-------------------------------------------------------

::

    $ sudo systemctl start redis


Enable ports for tunir in both autocloud-back0* systems
--------------------------------------------------------

Autocloud uses tunir to execute the tests on a given image. We will have to do the follow setup for tunir
to execute in a proper way.

::

    $ python /usr/share/tunir/createports.py

Enable kill_vagrant command in cron job
----------------------------------------

Enable a cron job which will run */usr/sbin/kill_vagrant* in every 10 minutes (or an hour). This is required
as many vagrant images do not work, and boot_timeout never works with vagrant-libvirt.

.. note:: This is a workaround which is required for now (2015-09-29). But may get removed in future.


Configure the database URI in all systems
------------------------------------------

In */etc/autocloud/autocloud.cfg* file please configure the sqlalchemy uri value. For our work, we are using 
postgres as database.

Create the tables in the database
----------------------------------


.. note:: This has to be done only once from autocloud-back01 system


::

    $ python /usr/share/autocloud/createdb.py


Install vagrant-libvirt on autocloud-back01
--------------------------------------------

This is the system to handle all libvirt tasks, so we will have to install vagrant-libvirt on this system.

::

    $ sudo dnf install vagrant-libvirt


Configure for the vagrant-virtualbox jobs in autocloud-back02
---------------------------------------------------------------

In */etc/autocloud/autocloud.cfg* file set *virtualbox* value to True. If you want to know how to setup virtualbox on the system, please refer to `this guide <http://tunir.readthedocs.org/en/latest/vagrant.html#how-to-install-virtualbox-and-vagrant>`_.


Configure the correct tunir job deatils
----------------------------------------

We need the exact commands/job details for tunir. This is a configuration file so that we can update it
whenever required.

::

    $ sudo wget https://raw.githubusercontent.com/kushaldas/tunirtests/master/fedora.txt -O /etc/autocloud/fedora.txt

Start fedmsg-hub service in autocloud-back0* systems
-----------------------------------------------------

This service listens for new koji builds, and creates the database entry and corresponding task in the queue.

::

    $ sudo systemctl start fedmsg-hub

Start autocloud service in autocloud-back0* systems
----------------------------------------------------

This service will listen for new task in the queue, and execute the tasks.

::

    $ sudo systemctl start autocloud

Starting the web dashboard in autocloud-web0* systems
-------------------------------------------------------

This is the web dashboard for the Autocloud, we use httpd for the this.

::

    $ sudo systemctl start httpd
