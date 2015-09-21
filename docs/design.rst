Design of the system
======================

Autocloud helps to automated testing of the Fedora Cloud images, and vagrant images produced
in the koji. It uses fedmsg to keep listening to new builds (createImage) task, and when a 
new image is available it enqueues it to it's own job queue, and then finally execute the
latest tests on the image. It can find out if the image is qcow2 based cloud image, or a
vagrant image, and calls tunir to do the real testing. The following image gives a basic 
idea about the flow of the steps in autocloud.


.. image:: design.png

Second system to test virtualbox based vagrant images
------------------------------------------------------

We need a second system which only tests the vagrant-virtualbox images. This has to be done
in a separate system as Virtualbox can not co-exists with kvm. So, the primary system does all
the work related to any libvirt based image (may be a qcow2, or a box file). The secondary
system only listens for vagrant-virtualbox based images, and tests those vagrant images.
