#!/bin/bash

# Replace the stack-installed deployer with our dev version
mkdir -p /opt/stackful
rm -rf /opt/stackful/app-deployer
ln -s /vagrant /opt/stackful/app-deployer
