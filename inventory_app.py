import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.db_config = {
            'host': 'localhost',
            'database': 'inventory_db',
            'user': 'root',  # replace with your MySQL username
            'password': ''  # replace with your MySQL password
        }
        self.logged_in = False
        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(pady=10)

        ttk.Label(self.login_frame, text="Username").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            if result:
                self.logged_in = True
                self.login_frame.pack_forget()
                self.create_main_frame()
                self.table_var.set('inventory')  # Set default table to 'inventory'
                self.load_table_data()  # Load data from 'inventory' table
            else:
                messagebox.showerror("Login Error", "Invalid username or password")
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=10)

        self.logout_button = ttk.Button(self.main_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=0, column=0, padx=5, pady=5)

        self.table_var = tk.StringVar()
        self.table_combobox = ttk.Combobox(self.main_frame, textvariable=self.table_var)
        self.table_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_table_names()
        self.table_combobox.bind("<<ComboboxSelected>>", self.on_table_selected)

        self.tree = ttk.Treeview(self.main_frame, show='headings')
        self.tree.grid(row=1, column=0, columnspan=4, pady=5)

        self.add_button = ttk.Button(self.main_frame, text="Add", command=self.add_item)
        self.add_button.grid(row=2, column=0, pady=5)

        self.edit_button = ttk.Button(self.main_frame, text="Edit", command=self.edit_item)
        self.edit_button.grid(row=2, column=1, pady=5)

        self.delete_button = ttk.Button(self.main_frame, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=2, column=2, pady=5)

        self.refresh_button = ttk.Button(self.main_frame, text="Refresh", command=self.load_table_data)
        self.refresh_button.grid(row=2, column=3, pady=5)

    def load_table_names(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables if table[0] != 'products']  # Exclude 'products' table if it exists
            self.table_combobox['values'] = table_names
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_table_selected(self, event):
        self.load_table_data()

    def load_table_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        table_name = self.table_var.get()
        if table_name:
            try:
                connection = mysql.connector.connect(**self.db_config)
                cursor = connection.cursor()
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [row[0] for row in cursor.fetchall()]
                mandatory_fields = ['table_name', 'ref_number', 'item_name', 'unit_price', 'max_stock', 'min_stock', 'ordering_level']
                # Sort columns to ensure mandatory fields are at the top
                sorted_columns = mandatory_fields + [col for col in columns if col not in mandatory_fields]
                self.tree['columns'] = sorted_columns
                for col in sorted_columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=100)
                cursor.execute(f"SELECT * FROM {table_name}")
                for row in cursor.fetchall():
                    self.tree.insert('', 'end', values=row)
            except Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def add_item(self):
        self.item_window = tk.Toplevel(self.root)
        self.item_window.title("Add Item")
        self.item_entries = {}
        table_name = self.table_var.get()
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [row[0] for row in cursor.fetchall()]
            mandatory_fields = ['table_name', 'ref_number', 'item_name', 'unit_price', 'max_stock', 'min_stock', 'ordering_level']
            sorted_columns = mandatory_fields + [col for col in columns if col not in mandatory_fields]
            for i, col in enumerate(sorted_columns):
                if col == 'date':  # Replace entry with DateEntry for 'date' column
                    ttk.Label(self.item_window, text=col).grid(row=i, column=0, padx=5, pady=5)
                    cal = DateEntry(self.item_window, width=12, background='darkblue', foreground='white', borderwidth=2)
                    cal.grid(row=i, column=1, padx=5, pady=5)
                    self.item_entries[col] = cal
                elif col != 'id':  # Don't allow changing the ID field
                    ttk.Label(self.item_window, text=col).grid(row=i, column=0, padx=5, pady=5)
                    entry = ttk.Entry(self.item_window)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    self.item_entries[col] = entry
            ttk.Button(self.item_window, text="Save", command=self.save_item).grid(row=len(columns), columnspan=2, pady=5)
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def save_item(self):
        table_name = self.table_var.get()
        fields = ', '.join(self.item_entries.keys())
        values = ', '.join(['%s'] * len(self.item_entries))
        data = tuple(entry.get() if not isinstance(entry, DateEntry) else entry.get_date() for entry in self.item_entries.values())
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {table_name} ({fields}) VALUES ({values})", data)
            connection.commit()
            messagebox.showinfo("Success", "Item added successfully")
            self.item_window.destroy()
            self.load_table_data()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def edit_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Item", "No item selected")
            return

        item = self.tree.item(selected_item, "values")
        self.item_window = tk.Toplevel(self.root)
        self.item_window.title("Edit Item")
        self.item_entries = {}
        table_name = self.table_var.get()
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [row[0] for row in cursor.fetchall()]
            mandatory_fields = ['table_name', 'ref_number', 'item_name', 'unit_price', 'max_stock', 'min_stock', 'ordering_level']
            sorted_columns = mandatory_fields + [col for col in columns if col not in mandatory_fields]
            for i, (col, val) in enumerate(zip(sorted_columns, item)):
                if col == 'date':  # Replace entry with DateEntry for 'date' column
                    ttk.Label(self.item_window, text=col).grid(row=i, column=0, padx=5, pady=5)
                    cal = DateEntry(self.item_window, width=12, background='darkblue', foreground='white', borderwidth=2)
                    cal.set_date(val)  # Set current date value
                    cal.grid(row=i, column=1, padx=5, pady=5)
                    self.item_entries[col] = cal
                elif col != 'id':  # Don't allow changing the ID field
                    ttk.Label(self.item_window, text=col).grid(row=i, column=0, padx=5, pady=5)
                    entry = ttk.Entry(self.item_window)
                    entry.insert(0, val)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    self.item_entries[col] = entry
            ttk.Button(self.item_window, text="Update", command=lambda: self.update_item(item[0])).grid(row=len(columns), columnspan=2, pady=5)
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_item(self, item_id):
        table_name = self.table_var.get()
        set_clause = ', '.join([f"{col}=%s" for col in self.item_entries.keys()])
        data = tuple(entry.get() if not isinstance(entry, DateEntry) else entry.get_date() for entry in self.item_entries.values())
        data += (item_id,)
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id=%s", data)
            connection.commit()
            messagebox.showinfo("Success", "Item updated successfully")
            self.item_window.destroy()
            self.load_table_data()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Item", "No item selected")
            return

        item = self.tree.item(selected_item, "values")
        table_name = self.table_var.get()
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id=%s", (item[0],))
            connection.commit()
            messagebox.showinfo("Success", "Item deleted successfully")
            self.load_table_data()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def logout(self):
        self.logged_in = False
        self.main_frame.pack_forget()
        self.create_login_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

