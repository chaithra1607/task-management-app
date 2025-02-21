import sqlite3

# Create a connection to the SQLite database (or create it if it doesn't exist)
def connect_db():
    return sqlite3.connect("tasks.db")

# Initialize the database (create the tasks table if it doesn't exist)
def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            deadline TEXT,
            status TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Add a task
def add_task():
    conn = connect_db()
    cursor = conn.cursor()
    description = input("Enter task description: ")
    deadline = input("Enter task deadline (optional, press Enter to skip): ")
    status = 'pending'  # Default status is 'pending'
    
    cursor.execute('''
        INSERT INTO tasks (description, deadline, status) 
        VALUES (?, ?, ?)
    ''', (description, deadline, status))
    
    conn.commit()
    conn.close()
    print("Task added successfully!\n")

# View all tasks
def view_all_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    
    if tasks:
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}")
    else:
        print("No tasks available.\n")
    
    conn.close()

# View pending tasks
def view_pending_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE status = "pending"')
    tasks = cursor.fetchall()
    
    if tasks:
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}")
    else:
        print("No pending tasks.\n")
    
    conn.close()

# View completed tasks
def view_completed_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE status = "completed"')
    tasks = cursor.fetchall()
    
    if tasks:
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}")
    else:
        print("No completed tasks.\n")
    
    conn.close()

# Update a task
def update_task():
    task_id = int(input("Enter task ID to update: "))
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    
    if task:
        new_description = input(f"Enter new description (current: {task[1]}): ")
        if new_description:
            cursor.execute('UPDATE tasks SET description = ? WHERE id = ?', (new_description, task_id))
        
        new_status = input(f"Enter new status (current: {task[3]}): ")
        if new_status in ['pending', 'completed']:
            cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
        
        conn.commit()
        print("Task updated successfully!\n")
    else:
        print("Task not found.\n")
    
    conn.close()

# Delete a task
def delete_task():
    task_id = int(input("Enter task ID to delete: "))
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    
    if task:
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        print("Task deleted successfully!\n")
    else:
        print("Task not found.\n")
    
    conn.close()

# Display menu
def display_menu():
    print("Task Management Application")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. View pending tasks")
    print("4. View completed tasks")
    print("5. Update a task")
    print("6. Delete a task")
    print("7. Exit")

# Main function to run the program
def main():
    initialize_db()  # Initialize the database and create the tasks table
    
    while True:
        display_menu()
        choice = input("Choose an option (1-7): ")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_all_tasks()
        elif choice == "3":
            view_pending_tasks()
        elif choice == "4":
            view_completed_tasks()
        elif choice == "5":
            update_task()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
