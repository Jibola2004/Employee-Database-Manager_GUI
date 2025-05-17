# Employee-Database-Manager_GUI
This is a simple PySide6 desktop application that interacts with an SQLite database to manage employee data. It allows adding, viewing, updating, deleting, and loading employee records using a GUI.

---

## 📁 Imports

```python
import sqlite3
from PySide6.QtWidgets import *
from PySide6.QtGui import QFont
```

- `sqlite3`: To handle database operations.
- `PySide6.QtWidgets`: GUI components like buttons, labels, layout managers, etc.
- `QFont`: Used to style fonts in the GUI.

---

## 🧱 Widget Class

```python
class Widget(QWidget):
```

The main GUI logic is contained within this `Widget` class, which inherits from `QWidget`.

---

### 🏗️ Constructor: `__init__`

Sets up the GUI layout and connects components.

#### 📌 Components:

- **Form inputs** for:
  - Firstname
  - Lastname
  - Profession
  - Age
  - Address
  - Salary

- **Buttons**:
  - `Add New Row`
  - `Update Selected Row`
  - `Insert Demo Data`
  - `Load Data`
  - `Extract Data`
  - `Delete Data`

- **Table**:
  - Displays employee data from the database.
  - Non-editable cells.
  - Columns auto-stretch to fill the space.
  - Sorting enabled on each column.

---

## 🔌 Database Connection

```python
@property
def create_connection(self):
```

Creates and returns a connection to the SQLite database file `employees.db`.

---

## 📥 load_data()

```python
def load_data(self):
```

Fetches all records from the `employees_list` table and loads them into the `QTableWidget`.

---

## ➕ add_data()

```python
def add_data(self):
```

Adds a new employee record to the database using input from the form fields.

---

## 🧪 insert_data()

```python
def insert_data(self):
```

Creates the `employees_list` table if it doesn't exist, and inserts several **demo employee records**.

---

## 📤 call_data()

```python
def call_data(self):
```

When a table row is selected, this method populates the form fields with that row's data for editing or viewing.

---

## ✏️ update_data()

```python
def update_data(self):
```

Updates the selected employee record in the database with the values from the form fields.

---

## ❌ delete_data()

```python
def delete_data(self):
```

Deletes the selected employee after showing a confirmation dialog with the employee's name and ID.

---

## 🧹 clear_inputs()

```python
def clear_inputs(self):
```

Clears all input fields after add/update operations.

---

## 🔔 show_notification()

```python
def show_notification(self, title="Success", message="Operation completed successfully!"):
```

Displays a message box with a custom title and message.

---

## 🖼️ GUI Features Summary

- **User-friendly** data entry form with labels and text fields.
- **Interactive Table** with sorting, auto-resizing, and non-editable cells.
- **Persistent Data** using SQLite backend.
- **Confirmation Dialog** before deletion.
- **Notification Popups** for every operation (add, update, delete, etc.).

---
