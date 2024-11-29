# Password Generator and Manager with MySQL Integration

## Project Overview
This project is a **Password Generator and Manager** designed to provide users with a secure and efficient way to manage their passwords. It combines the ability to generate strong passwords, store them in a MySQL database, and manage password history, all while offering features for security and usability. 

### Key Features:
- **Password Generation**:
  - Create passwords with customizable length.
  - Optionally include special characters for added complexity.

- **Password Storage**:
  - Store passwords in a secure MySQL database.
  - Add custom passwords for manual entry.

- **Password Management**:
  - View password history with timestamps.
  - Protect access to password history using a manager password.
  - Delete specific passwords or clear the entire history.

---

## Running Instructions

### 1. **Set Up the Environment**
1. Install **Python 3.8 or higher** from [python.org](https://www.python.org/).
2. Install **MySQL Server** and ensure it is running.

### 2. **Set Up the MySQL Database**
1. Create a database and table using the following SQL commands:
   ```sql
   CREATE DATABASE password_manager;

   USE password_manager;

   CREATE TABLE password_history (
       id INT AUTO_INCREMENT PRIMARY KEY,
       password VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

### 3. **Install Required Python Libraries**
Run the following command to install the MySQL connector:
```bash
pip install mysql-connector-python
```

### 4. **Configure the Code**
Update the `db_config` section in the script with your MySQL credentials:
```python
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'password_manager'
}
```

### 5. **Run the Application**
1. Save the script as `password_manager.py`.
2. Run the script in your terminal:
   ```bash
   python password_manager.py
   ```

### 6. **Follow the On-Screen Menu**
The application provides a menu with the following options:
- **Option 1**: Generate and store a password of your desired length.
- **Option 2**: Add a custom password to the database.
- **Option 3**: View all passwords (requires the manager password).
- **Option 4**: Delete specific or all passwords.
- **Option 5**: Exit the application.

### Example:
1. Choose **Option 1** to generate a password, specify its length, and store it.
2. Choose **Option 3**, enter the manager password, and view the stored password history.
3. Choose **Option 4** to delete a password by ID or clear the entire history.
