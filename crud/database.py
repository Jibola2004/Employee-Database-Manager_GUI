import sqlite3
from PySide6.QtWidgets import *
from PySide6.QtGui import QFont


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SQLite Database')
        self.setGeometry(100, 100, 600, 450)

        label_font = QFont('Arial', 11)
        input_font = QFont('Arial', 11)

        # Labels
        labels = ['Firstname', 'Lastname', 'Profession', 'Age', 'Address', 'Salary']
        self.inputs = {}

        form_layout = QVBoxLayout()
        for label in labels:
            hbox = QHBoxLayout()
            qlabel = QLabel(f"{label}:")
            qlabel.setFont(label_font)
            line_edit = QLineEdit()
            line_edit.setFont(input_font)
            line_edit.setMinimumWidth(300)
            self.inputs[label.lower()] = line_edit
            hbox.addWidget(qlabel)
            hbox.addWidget(line_edit)
            form_layout.addLayout(hbox)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton('Add New Row')
        update_button = QPushButton('Update Selected Row')
        add_button.setFont(label_font)
        update_button.setFont(label_font)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)

        add_button.clicked.connect(self.add_data)
        update_button.clicked.connect(self.update_data)

        form_layout.addLayout(button_layout)

        form_group = QGroupBox('Add / Update Employee')
        form_group.setFont(QFont('Arial', 12, QFont.Bold))
        form_group.setLayout(form_layout)


        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)  # set the number column in the table
        self.table.setHorizontalHeaderLabels(["ID", "Firstname", "Lastname", "Profession", "Age", "Address", "Salary"]) # set the header labels
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) # prevent the editting of the content of the table directly.
        self.table.setSortingEnabled(True) # enables the sorting for each column eg Ascending and Descending order
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # it allows all columns to strech to absolve the available space.
        self.table.setFont(QFont('Arial', 10)) # set the font to arial and font size to 10


        # Extra buttons
        insert_button = QPushButton('Insert Demo Data')
        insert_button.clicked.connect(self.insert_data)
        load_button = QPushButton('Load Data')
        load_button.clicked.connect(self.load_data)
        call_button = QPushButton('Extract Data')
        call_button.clicked.connect(self.call_data)
        delete_button = QPushButton('Delete Data')
        delete_button.clicked.connect(self.delete_data)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(form_group)
        main_layout.addWidget(self.table)
        main_layout.addWidget(insert_button)
        main_layout.addWidget(load_button)
        main_layout.addWidget(call_button)
        main_layout.addWidget(delete_button)

        self.setLayout(main_layout)


    @property
    def create_connection(self):
        '''Create a connection with the database'''
        self.connection = sqlite3.connect('employees.db')
        return self.connection

    def load_data(self):
        '''Load employee data from the database.'''
        cursor = self.create_connection.cursor()
        cursor.execute("SELECT * FROM employees_list")
        results = cursor.fetchall()

        self.table.setRowCount(len(results))
        for row_index, row_data in enumerate(results):
            for col_index, data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

        self.show_notification("Success", "Data loaded successfully.")
        self.connection.close()

    def add_data(self):
        cursor = self.create_connection.cursor()
        data = (
            self.inputs['lastname'].text(),
            self.inputs['firstname'].text(),
            self.inputs['profession'].text(),
            int(self.inputs['age'].text()),
            self.inputs['address'].text(),
            float(self.inputs['salary'].text())
        )

        cursor.execute("INSERT INTO employees_list (Lastname, Firstname, Profession, Age, Address, Salary) VALUES (?, ?, ?, ?, ?, ?)", data)
        self.connection.commit()
        self.connection.close()
        self.clear_inputs()
        self.show_notification("Done", "Employee added successfully.")

    def insert_data(self):
        cursor = self.create_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Lastname TEXT,
                Firstname TEXT,
                Profession TEXT,
                Age INTEGER,
                Address TEXT,
                Salary REAL
            )
        """)

        demo_employees = [
            ("Smith", "John", "Engineer", 30, "123 Maple Street", 75000),
            ("Doe", "Jane", "Designer", 28, "456 Oak Avenue", 68000),
            ("Brown", "Charlie", "Manager", 40, "789 Pine Road", 90000),
            ("Johnson", "Emily", "Developer", 25, "321 Birch Blvd", 70000),
            ("Davis", "Michael", "Analyst", 35, "654 Cedar Lane", 72000),
            ("Wilson", "Laura", "HR Specialist", 29, "987 Spruce Drive", 66000),
        ]

        cursor.executemany("INSERT INTO employees_list (Lastname, Firstname, Profession, Age, Address, Salary) VALUES (?, ?, ?, ?, ?, ?)", demo_employees)
        self.connection.commit()
        self.connection.close()
        self.show_notification("Done", "Demo data inserted successfully.")

    def call_data(self):
        row = self.table.currentRow()
        if row < 0:
            return
        for i, key in enumerate(["firstname", "lastname", "profession", "age", "address", "salary"], start=1):
            self.inputs[key].setText(self.table.item(row, i).text())

    def update_data(self):
        row = self.table.currentRow()
        if row < 0:
            self.show_notification("Error", "Please select a row to update.")
            return

        emp_id = int(self.table.item(row, 0).text())
        data = (
            self.inputs['lastname'].text(),
            self.inputs['firstname'].text(),
            self.inputs['profession'].text(),
            int(self.inputs['age'].text()),
            self.inputs['address'].text(),
            float(self.inputs['salary'].text()),
            emp_id
        )

        cursor = self.create_connection.cursor()
        cursor.execute("""
            UPDATE employees_list
            SET Lastname = ?, Firstname = ?, Profession = ?, Age = ?, Address = ?, Salary = ?
            WHERE id = ?
        """, data)
        self.connection.commit()
        self.connection.close()
        self.clear_inputs()
        self.show_notification("Updated", "Employee updated successfully.")

    def delete_data(self):
        row = self.table.currentRow()
        if row < 0:
           self.show_notification("Error", "Please select a row to delete.")
           return

        emp_id = int(self.table.item(row, 0).text())
        emp_name = self.table.item(row, 1).text() + " " + self.table.item(row, 2).text()

        # Ask for confirmation
        reply = QMessageBox.question(
              self,
              "Confirm Deletion",
             f"Are you sure you want to delete employee '{emp_name}' (ID: {emp_id})?",
             QMessageBox.Yes | QMessageBox.No
          )

        if reply == QMessageBox.Yes:
           cursor = self.create_connection.cursor()
           cursor.execute("DELETE FROM employees_list WHERE id = ?", (emp_id,))
           self.connection.commit()
           self.connection.close()
           self.table.removeRow(row)
           self.show_notification("Deleted", f"Employee '{emp_name}' (ID: {emp_id}) deleted.")
        else:
           self.show_notification("Cancelled", "Deletion cancelled.")


    def clear_inputs(self):
        for field in self.inputs.values():
            field.clear()

    def show_notification(self, title="Success", message="Operation completed successfully!"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

