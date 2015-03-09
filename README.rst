Install dependencies::

    sudo apt-get install ansible virtualbox
    vagrant plugin install vagrant-vbguest

Start the Vagrant instance::

    vagrant up --provision

In order to run the ansible tasks individually::

    ansible-playbook -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory \
        --private-key=~/.vagrant.d/boxes/birch-devstack-rc1/0/virtualbox/vagrant_private_key \
        -u vagrant fun-devstack.yml \
        -e openedx_release=named-release/birch.rc1 -e openedx_fun_release=fun/release-2.7


In case of authentication error, make sure you are using the right ssh private key::

    vagrant ssh-config

You now have a virtual machine containing a working instance of FUN. You can log into the VM and start a webserver:

    vagrant ssh
    paver lms --settings=fun.lms_dev
