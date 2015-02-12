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
    :name => "named-release/aspen", :box => "aspen-devstack-1", :file => "20141028-aspen-devstack-1.box"
  },
  "2.7" => {
    :name => "named-release/birch.rc1", :box => "birch-devstack-rc1", :file => "20150203-birch-devstack-rc1.box"
  }
}
fun_release = (ENV["FUN_RELEASE"] or "2.7")
openedx_release = fun_releases[fun_release]
openedx_fun_release = "fun/release-" + fun_release

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Creates an edX devstack VM from an official release
  # Note that these images are probably not compatible with vmware
  config.vm.box     = openedx_release[:box]
  config.vm.box_url = "http://files.edx.org/vagrant-images/#{openedx_release[:file]}"

  config.vm.network :private_network, ip: "192.168.33.10"# TODO what for?
  # TODO disable port forwarding if environment variable is set
  config.vm.network :forwarded_port, guest: 8000, host: 8000
  config.vm.network :forwarded_port, guest: 8001, host: 8001
  config.vm.network :forwarded_port, guest: 18080, host: 18080
  config.vm.network :forwarded_port, guest: 8765, host: 8765
  config.vm.network :forwarded_port, guest: 9200, host: 9200
  config.ssh.insert_key = true

  config.vm.synced_folder  ".", "/vagrant", disabled: true

  def sync_folder(src, dst, config, use_nfs)
    if use_nfs
      config.vm.synced_folder src, dst, create: true, owner: "edxapp", group: "www-data"
    else
      config.vm.synced_folder src, dst, create: true, nfs: true
    end
  end
  use_nfs = (ENV['VAGRANT_USE_VBOXFS'] == 'true') ? false : true
  sync_folder "repos/cs_comments_service", "/edx/app/forum/cs_comments_service", config, use_nfs
  sync_folder "repos/edx-platform", "/edx/app/edxapp/edx-platform", config, use_nfs
  sync_folder "repos/fun-apps", "/edx/app/edxapp/fun-apps", config, use_nfs
  sync_folder "repos/fun-config", "/edx/app/edxapp/fun-config", config, use_nfs
  sync_folder "repos/ora", "/edx/app/ora/ora", config, use_nfs
  sync_folder "repos/themes", "/edx/app/edxapp/themes", config, use_nfs

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", MEMORY.to_s]
    vb.customize ["modifyvm", :id, "--cpus", CPU_COUNT.to_s]

    # Allow DNS to work for Ubuntu 12.10 host
    # http://askubuntu.com/questions/238040/how-do-i-fix-name-service-for-vagrant-client
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  # Use vagrant-vbguest plugin to make sure Guest Additions are in sync
  config.vbguest.auto_reboot = true
  config.vbguest.auto_update = true

  # Assume that the base box has the edx_ansible role installed
  # We can then tell the Vagrant instance to update itself.
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "fun-devstack.yml"
    ansible.extra_vars = {
      openedx_release: openedx_release[:name],
      openedx_fun_release: openedx_fun_release
    }
  end
end
