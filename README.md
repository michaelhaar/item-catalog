# SQLAlchemy-intro
This project was part of my Full Stack Web Developer Nanodegree at Udacity. In this miniproject we used SQLAlchemy to perform CRUD (Create-Read-Update-Delete) operations on a database.

### Database Structure
Assume we want to model the menus of some restaurants in a database.
![Image of three restaurant menus](https://github.com/michi1992/item-catalog/blob/master/images_for_readme/overview.png)

Therefore we will use the following database structure:

![Image of the Databasestructure](https://github.com/michi1992/item-catalog/blob/master/images_for_readme/database_structure.png)

The database consists of two tables called ``restaurant`` and ``menu_item`` and its columns like name, id, etc. Additionally the ``menu_item`` holds a foreign key to the related restaurant id.

## Installing the Virtual Machine
We are using a virtual machine (VM) to run an SQL database server and a Python script that uses it. The VM is a Linux server system that runs on top of your own computer. The required steps to setup the virtual machine can be found in the separated [vm-setup.md](https://github.com/michi1992/SQLAlchemy-intro/blob/master/vm-setup.md) file.


## Usage
1. Clone this repository by executing ``git clone https://github.com/michi1992/item-catalog`` into your terminal window.
2. [Install the virtual machine.](https://github.com/michi1992/item-catalog/blob/master/vm-setup.md)
3. Enter ``cd item-catalog/vagrant`` to switch to the vagrant directory.
4. Start the virtual-machine: ``vagrant up``.
5. Log into the VM: ``vagrant ssh``
6. When you are successfully logged in, type ``cd /vagrant`` to switch the working directory.
7. Run ``python database_setup.py`` to create an empty database with Python and SQLAlchemy.
8. Run ``python lotsofmenus.py`` to populate the database with some entries provided by Udacity.
9. Take a closer look at the ``simple_crud.py``-file in order to see how to manipulate the database from Python and SQLALchemy.

## Authors

* **Michael Haar** - *Initial work* - [Michael Haar](https://github.com/michi1992)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/michi1992/database-logs-analysis/blob/master/LICENSE) file for details
