=========
fun-boxes
=========

This repository contains scripts to help you launch your own OpenFUN instance.
Instances are packaged in Virtuabox images managed by Vagrant and configured
with Ansible scripts.


Requirements
============

You are going to need vagrant(>= 1.5.3), ansible, and virtualbox to install and run the OpenFUN virtual image:

    sudo apt-get install vagrant ansible virtualbox 

Install vagrant-vbguest plugin::

    vagrant plugin install vagrant-vbguest

Install
=======
Get the Vagrant File and ansible playbook:
------------------------------------------

    curl -L https://rawgit.com/openfun/fun-boxes/master/Vagrantfile > Vagrantfile
    curl -L https://rawgit.com/openfun/fun-boxes/master/fun-devstack.yml > fun-devstack.yml

For testing
------------

Start the Vagrant instance::

    vagrant up --provision # go grab a coffee

For development
---------------

If you wish to contribute to OpenFUN you might want to checkout the OpenFUN and
OpenEdx repositories outside of the VM, in your host machine. The local
repositories will then be mounted in the VM::

    export VAGRANT_MOUNT_BASE="/path/to/my/repos"
    git clone https://github.com/openfun/fun-apps $VAGRANT_MOUNT_BASE/fun-apps/
    git clone https://github.com/openfun/edx-platform $VAGRANT_MOUNT_BASE/edx-platform/
    git clone https://github.com/openfun/edx-theme $VAGRANT_MOUNT_BASE/themes/fun/
    vagrant up --provision

Commands
========

You now have a virtual machine containing a working instance of FUN. You can
log into the VM::

    vagrant ssh

Start an LMS webserver::

    fun lms.dev run # open http://localhost:8000 in your browser

Start a Studio instance::

    fun cms.dev run # open http://localhost:8001 in your browser

Run OpenFUN unit tests::

    fun lms.test test ../fun-apps

Troubleshooting
===============

apt-get upgrade takes too long
------------------------------

It's quite possible that the package upgrade step stalls on a package install
that requires user input. If the upgrade step takes too long, you may want to
to manually log in to the virtual machine and upgrade packages::

    vagrant ssh
    sudo apt-get update && sudo apt-get upgrade

Cloning FUN repositories takes forever
--------------------------------------

If your repositories use the ssh git remotes, then git might get stuck on
verifying the fingerprint of the repository. You can solve this issue by
manually adding your private key to /edx/app/edxapp/.ssh/.

Other issues
------------

If other issues arise, feel free to open a ticket on this Github project.
