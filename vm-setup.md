## Installing the Virtual Machine
We are using a virtual machine (VM) to run an SQL database server and a Python script that uses it. The VM is a Linux server system that runs on top of your own computer. Don't worry if you are not familiar with virtual machines, this documnet will guide you through the setup part.

### Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

**Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

If Vagrant is successfully installed, you will be able to run `vagrant --version`
in your terminal to see the version number.

## General Usage

### Clone the repository
Clone this repository by running ``git clone [repository-url]`` in your terminal window.

### Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

*Note:* The command ``vagrant up`` threw an error on my machine. I had to enable SVM in my BIOS in order to fix it.

![Screenshot of the vagrant up command](https://github.com/michi1992/item-catalog/blob/master/images_for_readme/varant_up.png)

### Log into the virtual machine

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log into your newly installed Linux VM!

![Screenshot of the vagrant ssh command](https://github.com/michi1992/item-catalog/blob/master/images_for_readme/vagrant_ssh.png)

Congratulations! 🙌 You are now ssh'ed to your virtual machine.

After you are finished working with the virtual machine, you can simply press ``CTRL``+``D`` to log out and execute ``vagrant halt`` to properly shut down the virtual machine. 

![Screenshot of the vagrant halt command](https://github.com/michi1992/item-catalog/blob/master/images_for_readme/vagrant_halt.png)

Have Fun! 
