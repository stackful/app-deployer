#!/bin/sh

export DEBIAN_FRONTEND=noninteractive

# Get rid of the ancient Vagrant Chef
# Not needed on boxes that already pack Chef 11
# sudo /opt/vagrant_ruby/bin/gem uninstall chef ohai


# Install latest Chef release, if needed
chef_location=$(which chef-solo)
if [ -x "$chef_location" ] ; then
    echo "Chef Solo already installed: $chef_location"
else
    apt-get install --yes curl
    curl -L https://www.opscode.com/chef/install.sh | bash
fi

# Install stackful-node stack, if not there
if [ -f "/etc/stackful/node.json" ] ; then
    echo "Stack already installed."
else
    mkdir -p /etc/stackful
    cp /vagrant/node.json.sample /etc/stackful/node.json

    # set up in your project folder by the vagrant-up wrapper script
    /vagrant/stackful-node/run
fi

# Replace the stack-installed deployer with our dev version
rm -rf /opt/stackful/app-deployer
ln -s /vagrant /opt/stackful/app-deployer
