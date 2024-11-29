import random
import string
import mysql.connector


class PasswordGenerator:
    def __init__(self, include_special_chars=False):
        """Initialize the password generator with optional configurations."""
        self.include_special_chars = include_special_chars
        self.alphabet = string.ascii_lowercase
        self.numbers = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

    def generate_password(self, length):
        """Generate a single password with the specified length."""
        if length < 3:
            raise ValueError("Password length must be at least 3.")
        
        # Base password with random lowercase letters
        password = ''.join(random.choice(self.alphabet) for _ in range(length))
        
        # Replace random letters with numbers
        password = self._replace_with_number(password)
        
        # Replace random letters with uppercase letters
        password = self._replace_with_uppercase(password)
        
        # Optionally replace with special characters
        if self.include_special_chars:
            password = self._replace_with_special_char(password)
        
        return password

    def _replace_with_number(self, pword):
        """Replace 1-2 characters in the password with random numbers."""
        num_replacements = random.randint(1, 2)
        for _ in range(num_replacements):
            replace_index = random.randrange(len(pword))
            pword = pword[:replace_index] + random.choice(self.numbers) + pword[replace_index + 1:]
        return pword

    def _replace_with_uppercase(self, pword):
        """Replace 1-2 characters in the password with uppercase letters."""
        num_replacements = random.randint(1, 2)
        for _ in range(num_replacements):
            replace_index = random.randrange(len(pword))
            pword = pword[:replace_index] + pword[replace_index].upper() + pword[replace_index + 1:]
        return pword

    def _replace_with_special_char(self, pword):
        """Replace 1-2 characters in the password with special characters."""
        num_replacements = random.randint(1, 2)
        for _ in range(num_replacements):
            replace_index = random.randrange(len(pword))
            pword = pword[:replace_index] + random.choice(self.special_chars) + pword[replace_index + 1:]
        return pword


class PasswordManager:
    def __init__(self, generator, manager_password, db_config):
        """Manage password generation, storage, and protection."""
        self.generator = generator
        self.manager_password = manager_password
        self.db_config = db_config
        self.connection = self._connect_to_db()

    def _connect_to_db(self):
        """Connect to the MySQL database."""
        try:
            connection = mysql.connector.connect(**self.db_config)
            print("Connected to the database successfully.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit()

    def generate_and_store_password(self, length):
        """Generate a password and store it in the database."""
        password = self.generator.generate_password(length)
        self._store_password_in_db(password)
        return password

    def _store_password_in_db(self, password):
        """Store a generated password in the database."""
        cursor = self.connection.cursor()
        query = "INSERT INTO password_history (password) VALUES (%s)"
        cursor.execute(query, (password,))
        self.connection.commit()
        cursor.close()

    def add_custom_password(self, custom_password):
        """Add a user-provided password to the database."""
        self._store_password_in_db(custom_password)

    def view_password_history(self, manager_password):
        """Allow viewing of password history if the manager password is correct."""
        if manager_password == self.manager_password:
            cursor = self.connection.cursor()
            query = "SELECT id, password, created_at FROM password_history"
            cursor.execute(query)
            history = cursor.fetchall()
            cursor.close()
            return history
        else:
            raise ValueError("Incorrect manager password!")

    def delete_password_history(self, manager_password):
        """Delete passwords from the history."""
        if manager_password == self.manager_password:
            print("\n1. Delete a specific password by ID")
            print("2. Delete all passwords")
            choice = int(input("Enter your choice: "))

            cursor = self.connection.cursor()

            if choice == 1:
                password_id = int(input("Enter the ID of the password to delete: "))
                query = "DELETE FROM password_history WHERE id = %s"
                cursor.execute(query, (password_id,))
                print(f"Password with ID {password_id} deleted successfully.")
            elif choice == 2:  # Delete all passwords
                 query = "DELETE FROM password_history"
                 cursor.execute(query)
                 cursor.execute("ALTER TABLE password_history AUTO_INCREMENT = 1")
                 print("All passwords deleted successfully and ID counter reset.")

            else:
                print("Invalid choice. No action performed.")

            self.connection.commit()
            cursor.close()
        else:
            raise ValueError("Incorrect manager password!")

    def user_interaction(self):
        """Handle user inputs and manage passwords."""
        try:
            while True:
                print("\nMenu:")
                print("1. Generate and store a password")
                print("2. Add a custom password to history")
                print("3. View password history")
                print("4. Delete password history")
                print("5. Exit")

                choice = int(input("Enter your choice: "))
                if choice == 1:
                    length = int(input("Enter the length of the password to generate: "))
                    if length < 3:
                        print("Password length adjusted to 3 (minimum requirement).")
                        length = 3
                    password = self.generate_and_store_password(length)
                    print(f"Generated Password: {password}")
                elif choice == 2:
                    custom_password = input("Enter your custom password: ")
                    self.add_custom_password(custom_password)
                    print("Custom password added to the database.")
                elif choice == 3:
                    manager_password = input("Enter the manager password: ")
                    try:
                        history = self.view_password_history(manager_password)
                        print("\nPassword History:")
                        for entry in history:
                            print(f"ID: {entry[0]}, Password: {entry[1]}, Created At: {entry[2]}")
                    except ValueError as e:
                        print(e)
                elif choice == 4:
                    manager_password = input("Enter the manager password: ")
                    try:
                        self.delete_password_history(manager_password)
                    except ValueError as e:
                        print(e)
                elif choice == 5:
                    print("Exiting Password Manager. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    print("Welcome to the Enhanced Password Manager with Database Integration!")
    include_special_chars = input("Do you want to include special characters in your passwords? (yes/no): ").strip().lower() == 'yes'
    manager_password = input("Set a manager password to secure your password history: ").strip()

    # Database connection configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',
        'database': 'password_manager'
    }

    generator = PasswordGenerator(include_special_chars=include_special_chars)
    manager = PasswordManager(generator, manager_password, db_config)
    manager.user_interaction()


if __name__ == "__main__":
    main()
