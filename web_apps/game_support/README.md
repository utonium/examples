game\_support README
====================

Prerequisites
--------------------
The devops install for this example requires two applications already
available on the machine where this is being run. They are

    http://virtualbox.com
    http://vagrant.com

VirtualBox is a virtual machine emulator. Vagrant is a toolset used
to deploy and manage virtual machine. This has only been tested on
OSX (currently Yosemite).

You'll also need the Chef librarian tool. It is used to automate the
downloading of Chef cookbooks. Run the following in a Terminal shell

    gem install librarian

TODO: Could libararian be installed with vagrant. It was aggressive
about managing cookbooks, but that could be doable now.

Installation
--------------------
Once those applications are installed, open a new Terminal window.

cd into the 'devops' directory, and run

    librarian-chef install

The librarian tool takes over the cookbooks directory. So any local
cookbooks must be place into 'site\_cookbooks'.

That will download the various Chef cookbooks and their dependencies
automatically. Once that is complete, run the following.

    vagrant up 

This will start the virtual machine and do the installation of the
necessary components.

    vagrant ssh

Once you are at the prompt, you can run the tests. First clear the
example data

    /vagrant/scripts/reset_datastore

Then run the tests

    /var/www/code/test/bin/test_all

The example data can be loaded back up with the command

    /var/www/code/bin/setup_example_data
