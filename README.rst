=========
fun-boxes
=========

This repository contains scripts to help you launch your own OpenFUN instance.
Instances are packaged in Virtuabox images managed by Vagrant and configured
with Ansible scripts.


Requirements
============

A couple basic development packages are required::

    sudo apt-get install g++ make

You are going to need vagrant(>= 1.5.3), ansible, and virtualbox to install and
run the OpenFUN virtual image::

    sudo apt-get install vagrant ansible virtualbox 

Note that recent versions of Vagrant can be downloaded from
http://www.vagrantup.com/downloads.

If Virtualbox is not available in your package repositories, it may be
downloaded directly from https://www.virtualbox.org/wiki/Linux_Downloads.

Install vagrant-vbguest plugin::

    vagrant plugin install vagrant-vbguest

Install
=======

Running an existing release
---------------------------

OpenFUN provides ready-made VirtualBox images::

    cd releases/
    vagrant up

You may also specify the release to use::

    export FUN_RELEASE=2.9 vagrant

Downloading the 4.3+Gb Virtualbox image via HTTP may be time consuming.
Instead, we suggest to download the image by bittorrent from
http://files.alt.openfun.fr/vagrant-images/fun/ and then run the Vagrantfile::

    FUN_RELEASE=2.9 VAGRANT_BOXES=/home/mytorrents/ vagrant up

Provisioning a VM from scratch
------------------------------

This is a risky and lengthy process that will require running the OpenEdx provisioning playbook::

    cd devstack
    vagrant up --provision # grab a coffee

For development
---------------

If you wish to contribute to OpenFUN you might want to checkout the OpenFUN and
OpenEdx repositories outside of the VM, in your host machine. The local
repositories will then be mounted in the VM::

    export VAGRANT_MOUNT_BASE="/path/to/my/repos"
    git clone https://github.com/openfun/fun-apps $VAGRANT_MOUNT_BASE/fun-apps/
    git clone https://github.com/openfun/edx-platform $VAGRANT_MOUNT_BASE/edx-platform/
    git clone https://github.com/openfun/edx-theme $VAGRANT_MOUNT_BASE/themes/fun/

You may then start your VM as usual::

    cd releases/
    vagrant up --no-provision

The directories containing your repositories will be mounted in your VM so that
you can use your favorite IDE in your host environment and see the result in
the MV.

Upgrading an existing VM
------------------------

Starting from an existing VM, e.g: release 2.9, you may wish to upgrade it to
2.10, say for packaging. The following will run the `upgrade.yml` playbook::

    cd releases/
    FUN_RELEASE=2.10 vagrant up --provision

You may then package the upgraded VM::

    vagrant package --output openfun-2.10.box

And even create a torrent file to distribute it::

    ./create_torrent.py openfun-2.10.box

Commands
========

You now have a virtual machine containing a working instance of FUN. You can
log into the VM::

    vagrant ssh

Most commands should be run as user `edxapp`::

    sudo su edxapp # note that exapp is not sudo user

Start an LMS webserver::

    fun lms.dev run # open http://localhost:8000 in your browser

Start a Studio instance::

    fun cms.dev run # open http://localhost:8001 in your browser

Run OpenFUN unit tests::

    fun lms.test test ../fun-apps

Optional variables
==================

The following environment variables can be used to customize your guest environment.

- VAGRANT_NETWORK_DHCP: define this variable to use DHCP instead of a fixed IP.
- VAGRANT_NETWORK_IP: define this variable to customise the fixed IP of the
  guest machine. Otherwise it will be 10.1.100.101.
- VAGRANT_USE_VBOXF: set this variable to "true" to use vboxfs instead of nfs.
- VAGRANT_MOUNT_BASE: set this variable to an existing path that contains the
  fun-apps, edx-theme and edx-platform repositories (e.g:
  /home/user/fun/repos/) to mount them to /edx/app/edxapp/<reponame>.
- VAGRANT_NO_PORT_FORWARDING: disable port forwarding.
- VM_CPU_COUNT: the number of allocated CPUs. Defaults to 2.
- VM_MEMORY: the amount in Mb of allocated memory, in Mb. Defaults to 2048.
- FUN_RELEASE: the git version of FUN repositories to checkout. Can be a git
  sha1, tag or remote branch name. Defaults to the latest version, e.g: 2.11.


Troubleshooting
===============

Cannot connect to guest host via ssh
------------------------------------

The first step to diagnose this problem is to check the SSH configuration of
Vagrant for this particular VM:

    vagrant ssh-config

You can then try to login in verbose mode to the virtual machine by specifying
explicitely the user, host, port and private key:

    ssh -i /path/to/identity/file -P port -vvv user@host

Some kind of distribute/setuptools python issue
-----------------------------------------------

This is a frequent issue with OpenFUN. Some dependencies of FUN require a
recent version of setuptools, while Open edX requires an older version of
distribute. See [this pull
request](https://github.com/edx/edx-platform/pull/7465/) for reference. In
practice, this means you might have to manually install the 'right' (i.e: old)
version of distribute and setuptools manually in your guest environment:

    pip install setuptools==0.6c11
    pip install distribute==0.6.49

"It appears your machine doesn't support NFS"
---------------------------------------------

Make sure nfs is supported by your kernel::

    sudo apt-get install nfs-kernel-server

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

DHCP error
----------

On versions of Vagrant older than 1.7.3 you might encounter the following error:

    A host only network interface you're attempting to configure via DHCP
    already has a conflicting host only adapter with DHCP enabled. The
    DHCP on this adapter is incompatible with the DHCP settings. Two
    host only network interfaces are not allowed to overlap, and each
    host only network interface can have only one DHCP server. Please
    reconfigure your host only network or remove the virtual machine
    using the other host only network.

The nitty-gritty details are described here: https://github.com/mitchellh/vagrant/issues/3083

This issue can be solved by running::

    VBoxManage dhcpserver remove --netname HostInterfaceNetworking-vboxnet0

MySQL job "failed to start"
---------------------------

When downgrading from mysql-5.6, mysql-server may fail to start after install:

    ...
    Setting up mysql-server-5.5 (5.5.41-0ubuntu0.12.04.1) ...
    start: Job failed to start
    invoke-rc.d: initscript mysql, action "start" failed.

You may diagnose this problem more precisely by starting the mysql daemon manually::

    $ vagrant ssh
    $ sudo mysqld
    150415  7:34:08 [Warning] Using unique option prefix key_buffer instead of key_buffer_size is deprecated and will be removed in a future release. Please use the full name instead.
    150415  7:34:08 [Warning] Using unique option prefix myisam-recover instead of myisam-recover-options is deprecated and will be removed in a future release. Please use the full name instead.
    150415  7:34:08 [Note] Plugin 'FEDERATED' is disabled.
    150415  7:34:08 InnoDB: The InnoDB memory heap is disabled
    150415  7:34:08 InnoDB: Mutexes and rw_locks use GCC atomic builtins
    150415  7:34:08 InnoDB: Compressed tables use zlib 1.2.3.4
    150415  7:34:08 InnoDB: Initializing buffer pool, size = 128.0M
    150415  7:34:08 InnoDB: Completed initialization of buffer pool
    InnoDB: Error: log file ./ib_logfile0 is of different size 0 50331648 bytes
    InnoDB: than specified in the .cnf file 0 5242880 bytes!
    150415  7:34:08 [ERROR] Plugin 'InnoDB' init function returned error.
    150415  7:34:08 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
    150415  7:34:08 [ERROR] Unknown/unsupported storage engine: InnoDB
    150415  7:34:08 [ERROR] Aborting

This problem is caused by the InnoDb log file which was not updated prior to
upgrade. You may simply uninstall all mysql packages, remove the log files and
restart install::

    $ sudo apt-get remove --purge mysql-*
    $ sudo rm -rf /var/lib/mysql/
    $ sudo apt-get install mysql-server-5.5


Django is very slow
-------------------

If you find that your development server is very slow, it might be because of
DNS resolution. Try to alter the `/etc/hosts` file from the guest machine by
following the instructions from
http://stackoverflow.com/questions/28562968/django-1-4-18-dev-server-slow-to-respond-under-virtualbox/30356662#30356662

Other issues
------------

If other issues arise, feel free to open a ticket on this Github project.
