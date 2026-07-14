# Import tkinter library for creating GUI
import tkinter as tk
# Import messagebox for showing alerts
from tkinter import messagebox
# Import mysql connector for database operations
import mysql.connector
 
# Function to establish database connection
def get_connection():
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host='localhost',        # Database host (usually localhost)
        user='root',             # Database username (change as needed)
        password='1234',             # Database password (change as needed)
        database='employee_db'   # Database name
    )
    # Return the connection object
    return connection
 
# Function to create database and table if they don't exist
def setup_database():
    try:
        # Connect to MySQL server without specifying database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234'
        )
        # Create cursor to execute SQL commands
        cursor = connection.cursor()
       
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
       
        # Use the employee_db database
        cursor.execute("USE employee_db")
       
        # Create employees table if it doesn't exist
        # Table has: id, name, position, salary, hire_date
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            position VARCHAR(100) NOT NULL,
            salary DECIMAL(10, 2) NOT NULL,
            hire_date DATE NOT NULL
        )
        """
        # Execute the table creation query
        cursor.execute(create_table_query)
       
        # Commit the changes to database
        connection.commit()
       
        # Close the cursor
        cursor.close()
       
        # Close the connection
        connection.close()
       
        # Print success message
        print("Database and table created successfully!")
       
    except Exception as e:
        # Print error if something goes wrong
        print(f"Error setting up database: {e}")
 
# Function to add a new employee
def add_employee():
    # Create a new window for adding employee
    add_window = tk.Toplevel(root)
    # Set window title
    add_window.title("Add Employee")
    # Set window size
    add_window.geometry("400x300")
   
    # Label and entry for employee name
    tk.Label(add_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)
   
    # Label and entry for employee position
    tk.Label(add_window, text="Position:").pack(pady=5)
    position_entry = tk.Entry(add_window)
    position_entry.pack(pady=5)
   
    # Label and entry for employee salary
    tk.Label(add_window, text="Salary:").pack(pady=5)
    salary_entry = tk.Entry(add_window)
    salary_entry.pack(pady=5)
   
    # Label and entry for hire date
    tk.Label(add_window, text="Hire Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(add_window)
    date_entry.pack(pady=5)
   
    # Function to save employee to database
    def save_employee():
        # Get values from entry fields
        name = name_entry.get()
        position = position_entry.get()
        salary = salary_entry.get()
        hire_date = date_entry.get()
       
        # Check if all fields are filled
        if name and position and salary and hire_date:
            try:
                # Get database connection
                connection = get_connection()
                # Create cursor
                cursor = connection.cursor()
               
                # SQL query to insert employee data
                query = "INSERT INTO employees (name, position, salary, hire_date) VALUES (%s, %s, %s, %s)"
                # Values to insert
                values = (name, position, salary, hire_date)
               
                # Execute the insert query
                cursor.execute(query, values)
               
                # Commit the changes
                connection.commit()
               
                # Close cursor
                cursor.close()
               
                # Close connection
                connection.close()
               
                # Show success message
                messagebox.showinfo("Success", "Employee added successfully!")
               
                # Close the add window
                add_window.destroy()
               
            except Exception as e:
                # Show error message if something goes wrong
                messagebox.showerror("Error", f"Error adding employee: {e}")
        else:
            # Show warning if fields are empty
            messagebox.showwarning("Warning", "Please fill all fields!")
   
    # Create save button
    save_button = tk.Button(add_window, text="Save Employee", command=save_employee)
    save_button.pack(pady=10)
 
# Function to remove an employee
def remove_employee():
    # Create a new window for removing employee
    remove_window = tk.Toplevel(root)
    # Set window title
    remove_window.title("Remove Employee")
    # Set window size
    remove_window.geometry("400x200")
   
    # Label and entry for employee ID
    tk.Label(remove_window, text="Enter Employee ID to remove:").pack(pady=10)
    id_entry = tk.Entry(remove_window)
    id_entry.pack(pady=5)
   
    # Function to delete employee from database
    def delete_employee():
        # Get employee ID from entry
        employee_id = id_entry.get()
       
        # Check if ID is provided
        if employee_id:
            try:
                # Get database connection
                connection = get_connection()
                # Create cursor
                cursor = connection.cursor()
               
                # SQL query to delete employee by ID
                query = "DELETE FROM employees WHERE id = %s"
               
                # Execute the delete query
                cursor.execute(query, (employee_id,))
               
                # Commit the changes
                connection.commit()
               
                # Check if any row was deleted
                if cursor.rowcount > 0:
                    # Show success message
                    messagebox.showinfo("Success", "Employee removed successfully!")
                else:
                    # Show message if employee not found
                    messagebox.showwarning("Warning", "Employee ID not found!")
               
                # Close cursor
                cursor.close()
               
                # Close connection
                connection.close()
               
                # Close the remove window
                remove_window.destroy()
               
            except Exception as e:
                # Show error message if something goes wrong
                messagebox.showerror("Error", f"Error removing employee: {e}")
        else:
            # Show warning if ID is empty
            messagebox.showwarning("Warning", "Please enter Employee ID!")
   
    # Create delete button
    delete_button = tk.Button(remove_window, text="Remove Employee", command=delete_employee)
    delete_button.pack(pady=10)
 
# Function to promote an employee (increase salary)
def promote_employee():
    # Create a new window for promoting employee
    promote_window = tk.Toplevel(root)
    # Set window title
    promote_window.title("Promote Employee")
    # Set window size
    promote_window.geometry("400x250")
   
    # Label and entry for employee ID
    tk.Label(promote_window, text="Enter Employee ID:").pack(pady=5)
    id_entry = tk.Entry(promote_window)
    id_entry.pack(pady=5)
   
    # Label and entry for salary increase amount
    tk.Label(promote_window, text="Enter Salary Increase Amount:").pack(pady=5)
    increase_entry = tk.Entry(promote_window)
    increase_entry.pack(pady=5)
   
    # Function to update employee salary
    def update_salary():
        # Get employee ID and increase amount
        employee_id = id_entry.get()
        increase = increase_entry.get()
       
        # Check if both fields are filled
        if employee_id and increase:
            try:
                # Get database connection
                connection = get_connection()
                # Create cursor
                cursor = connection.cursor()
               
                # SQL query to update salary
                query = "UPDATE employees SET salary = salary + %s WHERE id = %s"
               
                # Execute the update query
                cursor.execute(query, (increase, employee_id))
               
                # Commit the changes
                connection.commit()
               
                # Check if any row was updated
                if cursor.rowcount > 0:
                    # Show success message
                    messagebox.showinfo("Success", "Employee promoted successfully!")
                else:
                    # Show message if employee not found
                    messagebox.showwarning("Warning", "Employee ID not found!")
               
                # Close cursor
                cursor.close()
               
                # Close connection
                connection.close()
               
                # Close the promote window
                promote_window.destroy()
               
            except Exception as e:
                # Show error message if something goes wrong
                messagebox.showerror("Error", f"Error promoting employee: {e}")
        else:
            # Show warning if fields are empty
            messagebox.showwarning("Warning", "Please fill all fields!")
   
    # Create promote button
    promote_button = tk.Button(promote_window, text="Promote Employee", command=update_salary)
    promote_button.pack(pady=10)
 
# Function to display all employees
def display_employees():
    # Create a new window for displaying employees
    display_window = tk.Toplevel(root)
    # Set window title
    display_window.title("All Employees")
    # Set window size
    display_window.geometry("800x400")
   
    try:
        # Get database connection
        connection = get_connection()
        # Create cursor
        cursor = connection.cursor()
       
        # SQL query to select all employees
        query = "SELECT * FROM employees"
       
        # Execute the select query
        cursor.execute(query)
       
        # Fetch all employee records
        employees = cursor.fetchall()
       
        # Close cursor
        cursor.close()
       
        # Close connection
        connection.close()
       
        # Check if there are any employees
        if employees:
            # Create a text widget to display data
            text_widget = tk.Text(display_window, height=20, width=100)
            text_widget.pack(pady=10, padx=10)
           
            # Insert header
            text_widget.insert(tk.END, "ID\tName\t\tPosition\t\tSalary\t\tHire Date\n")
            text_widget.insert(tk.END, "-" * 80 + "\n")
           
            # Loop through each employee
            for employee in employees:
                # Unpack employee data
                emp_id, name, position, salary, hire_date = employee
                # Insert employee data into text widget
                text_widget.insert(tk.END, f"{emp_id}\t{name}\t\t{position}\t\t{salary}\t\t{hire_date}\n")
           
            # Make text widget read-only
            text_widget.config(state=tk.DISABLED)
        else:
            # Show message if no employees found
            messagebox.showinfo("Info", "No employees found in database!")
            display_window.destroy()
           
    except Exception as e:
        # Show error message if something goes wrong
        messagebox.showerror("Error", f"Error displaying employees: {e}")
        display_window.destroy()
 
# Main function to create the GUI
def main():
    global root  # Make root variable global
   
    # Setup database and table
    setup_database()
   
    # Create main window
    root = tk.Tk()
    # Set window title
    root.title("Employee Management System")
    # Set window size
    root.geometry("500x400")
   
    # Create title label
    title_label = tk.Label(root, text="Employee Management System", font=("Arial", 16, "bold"))
    title_label.pack(pady=20)
   
    # Create Add Employee button
    add_button = tk.Button(root, text="Add Employee", command=add_employee,
                          font=("Arial", 12), width=20, height=2)
    add_button.pack(pady=10)
   
    # Create Remove Employee button
    remove_button = tk.Button(root, text="Remove Employee", command=remove_employee,
                             font=("Arial", 12), width=20, height=2)
    remove_button.pack(pady=10)
   
    # Create Promote Employee button
    promote_button = tk.Button(root, text="Promote Employee", command=promote_employee,
                              font=("Arial", 12), width=20, height=2)
    promote_button.pack(pady=10)
   
    # Create Display Employees button
    display_button = tk.Button(root, text="Display Employees", command=display_employees,
                              font=("Arial", 12), width=20, height=2)
    display_button.pack(pady=10)
   
    # Create Exit button
    exit_button = tk.Button(root, text="Exit", command=root.quit,
                           font=("Arial", 12), width=20, height=2)
    exit_button.pack(pady=10)
   
    # Start the main event loop
    root.mainloop()
 
# Check if this script is run directly
if __name__ == "__main__":
    # Call the main function
    main()              