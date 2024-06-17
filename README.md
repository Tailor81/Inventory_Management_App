# Inventory_Management_App
 This is a Python-based Inventory Management System using the tkinter library for the GUI and mysql.connector for connecting to a MySQL database. The application supports basic CRUD (Create, Read, Update, Delete) operations, login/logout functionality, and table management.

# Features
User Authentication: Login and logout functionalities for secure access.
Table Management: Load and display data from different tables.
CRUD Operations: Add, edit, and delete inventory items.
Dynamic Form Generation: Forms are generated dynamically based on the table schema, with special handling for date fields.
Data Display: Inventory data is displayed in a table with sortable columns.

# Prerequisites
Python 3.x
MySQL database
Required Python packages: tkinter, mysql-connector-python, tkcalendar

# Installation
Install Python Packages:
pip install tk mysql-connector-python tkcalendar

# MySQL Setup:
Create a MySQL database named inventory_db.
Create an admin table for login purposes:

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO admin (username, password) VALUES ('admin', 'admin');  -- Example admin user
Create other necessary tables for your inventory management, e.g.:

CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10, 2),
    date DATE
);

# Usage
Run the Application:
python inventory_app.py

Login:
Use the credentials defined in the admin table to log in.

# Main Interface:
Logout: Click the "Logout" button to log out.

Select Table: Use the dropdown to select a table to view and manage.

Add Item: Click the "Add" button to add a new item.

Edit Item: Select an item and click the "Edit" button to modify it.

Delete Item: Select an item and click the "Delete" button to remove it.

Refresh: Click the "Refresh" button to reload the table data.


# Code Explanation
Main Classes and Methods 

InventoryApp Class:
Initializes the main application, sets up the login frame, and manages the database configuration.

create_login_frame:
Creates the login frame with username and password fields.

login:
Authenticates the user by checking the credentials against the admin table.

create_main_frame:
Sets up the main interface for managing inventory items and other tables.

load_table_names:
Loads the names of the tables from the database and populates the dropdown.

on_table_selected:
Loads the data from the selected table.

load_table_data:
Fetches and displays the data from the currently selected table.

add_item:
Opens a form to add a new item to the table.

edit_item:
Opens a form to edit the selected item.

delete_item:
Deletes the selected item from the table.

logout:
Logs out the current user and returns to the login screen.

# Customization
Database Configuration: Update the self.db_config dictionary with your MySQL database credentials.
Table Schema: Ensure the table schemas in your database match the fields expected by the application.
User Interface: Customize the tkinter widgets and layout to fit your needs.

# Converting to Executable
To convert the script to an executable, you can use pyinstaller:
pip install pyinstaller
pyinstaller --onefile inventory_app.py
The executable will be created in the dist directory.
