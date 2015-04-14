Vagrant.require_version ">= 1.5.3"
unless Vagrant.has_plugin?("vagrant-vbguest")
  raise "Please install the vagrant-vbguest plugin by running `vagrant plugin install vagrant-vbguest`"
end

VAGRANTFILE_API_VERSION = "2"

MEMORY = 2048
CPU_COUNT = 2

# This is the version from the Openfun repository that you wish to use
# We map the name of the git branch that we use for a release
# to a box name and a file path, which are used for retrieving
# a Vagrant box from the internet.
fun_releases = {
  "2.6" => {
    :ref =>"fun/release-2.6",
    :name => "named-release/aspen", :box => "aspen-devstack-1", :file => "20141028-aspen-devstack-1.box"
  },
  "2.7" => {
    :ref =>"fun/release-2.7",
    :name => "named-release/birch.rc1", :box => "birch-devstack-rc1", :file => "20150203-birch-devstack-rc1.box"
  },
  "2.9" => {
    :ref =>"fun/release-2.9",
    :name => "named-release/birch", :box => "birch-devstack", :file => "20150224-birch-devstack.box"
  },
  "master" => {
    :ref =>"fun/release-2.9",
    :name => "named-release/birch", :box => "birch-devstack", :file => "20150224-birch-devstack.box"
  }
}
fun_release = (ENV["FUN_RELEASE"] or "master")
openedx_release = fun_releases[fun_release]


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Creates an edX devstack VM from an official release
  # Note that these images are probably not compatible with vmware
  config.vm.box     = openedx_release[:box]
  config.vm.box_url = "http://files.alt.openfun.fr/vagrant-images/edx/#{openedx_release[:file]}"

  unless ENV['VAGRANT_NO_PORT_FORWARDING']
      config.vm.network :forwarded_port, guest: 8000, host: 8000
      config.vm.network :forwarded_port, guest: 8001, host: 8001
      config.vm.network :forwarded_port, guest: 18080, host: 18080
      config.vm.network :forwarded_port, guest: 8765, host: 8765
      config.vm.network :forwarded_port, guest: 9200, host: 9200
  end
  config.ssh.insert_key = true

  config.vm.synced_folder  ".", "/vagrant", disabled: true

  # Assign a fixed IP
  config.vm.network :private_network, type: "dhcp"

  # If this environment variable is defined, we mount the OpenEdx and OpenFUN
  # repositories from this folder to their corresponding locations in the VM
  if ENV['VAGRANT_MOUNT_BASE']
    # Sync folders with NFS or VBOXFS
    def sync_folder(src, dst, config)
      use_nfs = (ENV['VAGRANT_USE_VBOXFS'] == 'true') ? false : true
      full_src = ENV['VAGRANT_MOUNT_BASE'] + "/" + src
      if use_nfs
        config.vm.synced_folder full_src, dst, create: true, nfs: true
      else
        config.vm.synced_folder full_src, dst, create: true, owner: "edxapp", group: "www-data"
      end
    end
    sync_folder "edx-platform", "/edx/app/edxapp/edx-platform", config
    sync_folder "fun-apps", "/edx/app/edxapp/fun-apps", config
    sync_folder "themes", "/edx/app/edxapp/themes", config
  end

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", MEMORY.to_s]
    vb.customize ["modifyvm", :id, "--cpus", CPU_COUNT.to_s]

    # Allow DNS to work for Ubuntu 12.10 host
    # http://askubuntu.com/questions/238040/how-do-i-fix-name-service-for-vagrant-client
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    # Solve this issue: https://www.virtualbox.org/ticket/13002
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "off"]
  end

  # Use vagrant-vbguest plugin to make sure Guest Additions are in sync
  config.vbguest.auto_reboot = true
  config.vbguest.auto_update = true

  # Assume that the base box has the edx_ansible role installed
  # We can then tell the Vagrant instance to update itself.
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "fun-devstack.yml"
    ansible.extra_vars = {
      fun_release: fun_release,
      openedx_release: openedx_release[:name],
      openedx_fun_release: openedx_release[:ref]
    }
  end
end
