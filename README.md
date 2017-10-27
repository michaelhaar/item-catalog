# Item-Catalog
This project was part of my Full Stack Web Developer Nanodegree at Udacity. In this project we developed an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Installing the Virtual Machine
We are using a virtual machine (VM) to run an SQL database server and some Python scripts that use it. The VM is a Linux server system that runs on top of your own computer. The required steps to setup the virtual machine can be found in the separated [vm-setup.md](https://github.com/michi1992/SQLAlchemy-intro/blob/master/vm-setup.md) file.


## Usage
1. Clone this repository by executing ``git clone https://github.com/michi1992/item-catalog`` in your terminal window.
2. Obtain a Google CLIENT ID by following [this guide](https://developers.google.com/identity/sign-in/web/devconsole-project). Add ``https://localhost:5000`` to the javascript origins and the authorized forwarding urls.
3. Rename the file to ``client_secrets.json`` and copy&paste it into the vagrant folder. 
4. [Install the virtual machine.](https://github.com/michi1992/item-catalog/blob/master/vm-setup.md)
5. Run ``cd item-catalog/vagrant`` to switch to the vagrant directory.
6. Start the virtual-machine: ``vagrant up``.
7. Log into the VM: ``vagrant ssh``.
8. When you are successfully logged in, type ``cd /vagrant`` to switch the working directory of your VM.
9. Run ``python database_setup.py`` to create an empty database.
10. Run ``python populate_database.py`` to create the item categories.
11. Type ``python item_catalog.py`` to start the server..
12. Finally you can visit the webpage: [https://localhost:5000](https://localhost:5000)


## Authors

* **Michael Haar** - *Initial work* - [Michael Haar](https://github.com/michi1992)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/michi1992/database-logs-analysis/blob/master/LICENSE) file for details
