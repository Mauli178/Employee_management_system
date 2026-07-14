#import tkinter library for creating GUI applications
import tkinter as tk
#import  message box for showing alerts
from tkinter import messagebox
#import  mysql connector for database connection
import mysql.connector

#function to connect to the database 
def get_connection():
    #connect to mysql
    connection = mysql.connector.connect(
        host="localhost",# database host 
        user="root",# database user
        password="1234",# database password
        database="employee_db"# database name
    )
    return connection
#function to setup the database and create the employee table if not exists
def setup_database():
    #connect to mysql
    try:
        connection = mysql.connector.connect(
        host="localhost",# database host 
        user="root",# database user
        password="1234",# database password
        )
        cursor=connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
        cursor.execute("USE employee_db")
    # create a table for storing employee information
    #tabel has id, name, position, salary and hire date columns

        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id Int AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL, 
            position VARCHAR(100) NOT NULL,
            salary DECIMAL(10, 2) NOT NULL,
            hire_date DATE NOT NULL
        )"""
        #execute the query to create table
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()
        print("database and table created successfully")
    except Exception as e:
        print("Error while setting up the database:", e)

#function to add a new employee to the database
def add_employee():
    #create a new window for adding employee
    add_window = tk.Toplevel(root)
    #set the window title
    add_window.title("Add Employee")
    #set window size
    add_window.geometry("400x300")

    #label and entry for employee name
    tk.Label(add_window,text="Name: ").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)

    #label and entry for employee position
    tk.Label(add_window,text="Position:").pack(pady=5)
    position_entry = tk.Entry(add_window)
    position_entry.pack(pady=5)

    #label and entry for employee salary
    tk.Label(add_window,text="Salary:").pack(pady=5)
    salary_entry = tk.Entry(add_window)
    salary_entry.pack(pady=5)

    #label and entry for employee hire date
    tk.Label(add_window,text="Hire Date (YYYY-MM-DD):").pack(pady=5)
    hire_date_entry = tk.Entry(add_window)
    hire_date_entry.pack(pady=5)
#function to save employee info in database
    def save_employee():
        #get values from entry fields
        name = name_entry.get()
        position = position_entry.get()
        salary = salary_entry.get()
        hire_date = hire_date_entry.get()

        #check if all fields are filled 
        if name  and position and salary and hire_date:
            try:
                #connect to database
                connection = get_connection()
                #create cursor 
                cursor = connection.cursor()
                #insert employee info into database
                query = "INSERT INTO employees (name, position, salary, hire_date) VALUES (%s, %s, %s, %s)"
                #values to insert
                values =(name, position, salary, hire_date)
                #execute the query 
                cursor.execute(query, values)
                #commit changes
                connection.commit()
                #close cursor
                cursor.close()
                #close connection
                connection.close()
                messagebox.showinfo("Success", "Employee added successfully")
                add_window.destroy()#close the add employee window
            except Exception as e:
                messagebox.showerror("Error", f"Error while adding employee: {e}")
        else:
            #show warrning if any field is empty
            messagebox.showwarning("Input Error", "Please fill all fields")
    save_button = tk.Button(add_window, text="Save", command=save_employee)
    save_button.pack(pady=10)
#function to remove an employee from the database

def remove_employee():
    #create a new window for removing employee
    remove_window = tk.Toplevel(root)
    #set the window title
    remove_window.title("Remove Employee")
    #set window size
    remove_window.geometry("400x200")
    #label and entry for employee id 
    tk.Label(remove_window, text="Enter Employee ID to remove:").pack(pady=5)
    id_entry = tk.Entry(remove_window)
    id_entry.pack(pady=5)
#function to delete employee from database
    def delete_employee():
        #get employee id from entry field
        employee_id = id_entry.get()
        #check if id is provided 
        if employee_id:
            try:
                #get database connection
                connection = get_connection()
                #create cursor
                cursor = connection.cursor()
                #sql quesry to delete employee by id
                query = "DELETE FROM employees WHERE id = %s"
                #execute delete query 
                cursor.execute(query, (employee_id,))
                #commit changes
                connection.commit()
                #Check if any row was deleted 
                if cursor.rowcount > 0:
                    #show success message if employee was removed
                    messagebox.showinfo("Success", "Employee removed successfully")
                else:
                    messagebox.showwarning("Not Found", "No employee found with the given ID")
                cursor.close()
                connection.close()
                remove_window.destroy()#close the remove employee window
            except Exception as e:
                messagebox.showerror("Error", f"Error while removing employee: {e}")
        else:
            #show warning if id is not provided
            messagebox.showwarning("Warning", "Please enter an Employee ID")
    #create delete button to trigger the delete_employee function
    delete_button = tk.Button(remove_window, text="Remove", command=delete_employee)
    delete_button.pack(pady=10)
def promote_employee():
    #create a new window for promoting employee
    promote_window = tk.Toplevel(root)
    #set window title 
    promote_window.title("Promote Employee")
    #set window size
    promote_window.geometry("400x250")

    #label and entry for employee id
    tk.Label(promote_window, text="Enter Employee ID to promote:").pack(pady=5)
    id_entry = tk.Entry(promote_window)
    id_entry.pack(pady=5)

    #label and entry for increasing salary
    tk.Label(promote_window, text="Enter Salary Increase Amount:").pack(pady=5)
    increase_entry = tk.Entry(promote_window)
    increase_entry.pack(pady=5)

    #function to update employee salary in database
    def update_salary():
        #get employee id and salary increase amount from entry fields
        employee_id = id_entry.get()
        increase_amount = increase_entry.get()
        #check if both fields are filled
        if employee_id and increase_amount:
            try:
                #get database connection
                connection = get_connection()
                #create cursor
                cursor = connection.cursor()
                #sql query to update employee salary by adding the increase amount
                query = "UPDATE employees SET salary = salary + %s WHERE id = %s"
                #execute the update query
                cursor.execute(query, (increase_amount, employee_id))
                #commit changes
                connection.commit()
                #check if any row was updated 
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Employee promoted successfully")
                else:
                    messagebox.showwarning("Not Found", "No employee found with the given ID")
                cursor.close()
                connection.close()
                promote_window.destroy()#close the promote employee window
            except Exception as e:
                #show error msg if something goes wrong while promoting employee
                messagebox.showerror("Error", f"Error while promoting employee: {e}")
        else:
            #show warning if any field is empty
            messagebox.showwarning("Warning", "Please fill all fields")
    #create promote button 
    promote_button = tk.Button(promote_window, text="Promote", command=update_salary)
    promote_button.pack(pady=10)

def display_employees():
    #create a new window for displaying employees
    display_window = tk.Toplevel(root)
    #set window title
    display_window.title("Employee List")
    #set window size
    display_window.geometry("800x400")

    #create a text widget to display employee information
    text_widget = tk.Text(display_window)
    text_widget.pack(expand=True, fill=tk.BOTH)

    try:
        #get database connection
        connection = get_connection()
        #create cursor
        cursor = connection.cursor()
        #sql query to select all employees from the database
        query = "SELECT * FROM employees"
        #execute the select query
        cursor.execute(query)
        #fetch all employee records
        employees = cursor.fetchall()
        cursor.close()
        connection.close()

        #check if there are any employees in the database
        
        if employees:
            text_widget.insert(display_window, height=20, width=80)
            text_widget.pack(pady=10)
            #loop through each employee
            #display each employee's information in the text widget
            for employee in employees:
                #unpack employee tuple into individual variables
                emp_id, name, position, salary, hire_date = employee
                #insert employee information into the text widget
                text_widget.insert(tk.END, f"{emp_id}\t{name}\t\t{position}\t\t{salary}\t\t{hire_date}\n")
            text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
        else:
            #show info message if no employees found
            messagebox.showinfo("Info", "No employees found in the database.")  
    except Exception as e:
        messagebox.showerror("Error", f"Error while fetching employees: {e}")
        display_window.destroy()  # Close the display window if there's an error

#main function to create the main application window and buttons for different operations
def main():
    global root #make root variable global so it can be accessed in other functions
    #setup the database and create the employee table if not exists
    setup_database()
    #create main window
    root = tk.Tk()
    #set window title
    root.title("Employee Management System")
    #set window size
    root.geometry("500x400")

    title_Label = tk.Label(root, text="Employee Management System", font=("Arial", 16))
    title_Label.pack(pady=20)

    #create buttons for different operations
    #create add employee button
    add_button = tk.Button(root, text="Add Employee", command=add_employee, font=("Arial", 12),width=20,height=2)
    add_button.pack(pady=10)

    #create remove employee button
    remove_button = tk.Button(root, text="Remove Employee", command=remove_employee, font=("Arial", 12),width=20,height=2)
    remove_button.pack(pady=10)

    #create promote employee button
    promote_button = tk.Button(root, text="Promote Employee", command=promote_employee, font=("Arial", 12),width=20,height=2)
    promote_button.pack(pady=10)

    #create display employees button
    display_button = tk.Button(root, text="Display Employees", command=display_employees, font=("Arial", 12),width=20,height=2)
    display_button.pack(pady=10)
    
    #exit button
    exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial ", 12),width=20,height=2)
    exit_button.pack(pady=10)

    root.mainloop()#start the main event loop for the application

#check i script is run directly and not imported as a module
if __name__ == "__main__":
    main()#call the main function to start the application
    