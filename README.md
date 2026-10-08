# 📚 Library Management System

## 1. Project Overview

The **Library Management System** is a DBMS project developed to manage the basic activities of a library in a simple and organized way.

The system stores information about **students, books, authors, librarians, and book issue/return transactions** in a MySQL database. A **Streamlit frontend** is used so that users can interact with the database through a simple interface instead of writing SQL queries manually.

The project demonstrates how a real-world system can be designed using **database tables, primary keys, foreign keys, relationships, constraints, SQL queries, and CRUD operations**.

---

## 2. Objectives

The main objectives of the project are:

* To maintain student records.
* To store and manage book details.
* To maintain author information.
* To store librarian details.
* To keep track of issued and returned books.
* To establish relationships between different tables.
* To reduce manual record keeping.
* To perform database operations through a simple frontend.
* To demonstrate practical implementation of DBMS concepts.
* To connect a MySQL database with a Python application.

---

## 3. Technologies Used

| Technology          | Purpose                                   |
| ------------------- | ----------------------------------------- |
| **MySQL**           | Stores and manages the library database   |
| **Python**          | Used for application development          |
| **Streamlit**       | Used to create the frontend               |
| **MySQL Connector** | Connects Python with MySQL                |
| **Pandas**          | Displays database records in table format |
| **VS Code**         | Used for project development              |

---

## 4. Database Tables

The system contains **five main tables**.

### 4.1 STUDENT

The `STUDENT` table stores information about students who use the library.

| Attribute  | Data Type    | Description                       |
| ---------- | ------------ | --------------------------------- |
| Student_ID | INT          | Primary key and unique student ID |
| Name       | VARCHAR(100) | Student's name                    |
| Email      | VARCHAR(100) | Student's email                   |
| Phone      | VARCHAR(15)  | Student's phone number            |
| Department | VARCHAR(50)  | Student's department              |

**Primary Key:** `Student_ID`

---

### 4.2 AUTHOR

The `AUTHOR` table stores information about book authors.

| Attribute   | Data Type    | Description        |
| ----------- | ------------ | ------------------ |
| Author_ID   | INT          | Primary key        |
| Author_Name | VARCHAR(100) | Name of the author |

**Primary Key:** `Author_ID`

---

### 4.3 BOOK

The `BOOK` table stores information about books available in the library.

| Attribute | Data Type     | Description                    |
| --------- | ------------- | ------------------------------ |
| Book_ID   | INT           | Primary key                    |
| Title     | VARCHAR(150)  | Name of the book               |
| Price     | DECIMAL(10,2) | Price of the book              |
| Category  | VARCHAR(50)   | Category of the book           |
| Author_ID | INT           | Foreign key referencing AUTHOR |

**Primary Key:** `Book_ID`
**Foreign Key:** `Author_ID`

The price also has a constraint:

```sql
CHECK (Price > 0)
```

This ensures that the price of a book cannot be zero or negative.

---

### 4.4 ISSUE

The `ISSUE` table records book issue and return transactions.

| Attribute   | Data Type   | Description                     |
| ----------- | ----------- | ------------------------------- |
| Issue_ID    | INT         | Primary key                     |
| Student_ID  | INT         | Foreign key referencing STUDENT |
| Book_ID     | INT         | Foreign key referencing BOOK    |
| Issue_Date  | DATE        | Date when the book was issued   |
| Return_Date | DATE        | Date when the book was returned |
| Status      | VARCHAR(20) | Current status of the book      |

**Primary Key:** `Issue_ID`

**Foreign Keys:**

```text
Student_ID → STUDENT.Student_ID
Book_ID → BOOK.Book_ID
```

The `ISSUE` table is the **transaction table** of the system.

It connects students with books and records the complete issue/return activity.

---

### 4.5 LIBRARIAN

The `LIBRARIAN` table stores information about librarians.

| Attribute    | Data Type    | Description       |
| ------------ | ------------ | ----------------- |
| Librarian_ID | INT          | Primary key       |
| Name         | VARCHAR(100) | Librarian's name  |
| Email        | VARCHAR(100) | Librarian's email |

**Primary Key:** `Librarian_ID`

---

## 5. Database Relationships

The main relationships in the system are:

### AUTHOR → BOOK

One author can write many books.

```text
AUTHOR  1 ───────── N  BOOK
```

`BOOK.Author_ID` is a foreign key referencing `AUTHOR.Author_ID`.

---

### STUDENT → ISSUE

One student can have multiple issue records.

```text
STUDENT  1 ───────── N  ISSUE
```

`ISSUE.Student_ID` references `STUDENT.Student_ID`.

---

### BOOK → ISSUE

One book can appear in multiple issue transactions over time.

```text
BOOK  1 ───────── N  ISSUE
```

`ISSUE.Book_ID` references `BOOK.Book_ID`.

---

### LIBRARIAN → ISSUE

In the ER model, one librarian can manage multiple issue transactions.

```text
LIBRARIAN  1 ───────── N  ISSUE
```

This represents the librarian responsible for managing book transactions.

---

### Overall Relationship

```text
                 AUTHOR
                    |
                   1:N
                    |
                   BOOK
                    |
                   1:N
                    |
                  ISSUE
                 /     \
               N:1     N:1
               /         \
          STUDENT      LIBRARIAN
```

The **ISSUE table is the central transaction table** connecting the library's book transactions with students.

---

## 6. Features

### 📊 Dashboard

The dashboard provides a quick overview of the library, including:

* Total students
* Total authors
* Total books
* Issued books
* Returned books
* Recent issue records

---

### 👨‍🎓 Student Management

Users can:

* View students
* Add new students
* Store student contact details
* Store department information

---

### ✍️ Author Management

Users can:

* View authors
* Add new authors
* Maintain author records

---

### 📚 Book Management

Users can:

* View books
* Add new books
* Store book price
* Add book categories
* Associate books with authors

---

### 🔄 Issue / Return Management

Users can:

* Issue a book to a student
* Record issue date
* View issue records
* Return books
* Record return date
* Update book status

Example status:

```text
Issued
Returned
```

---

### 👩‍💼 Librarian Management

Users can:

* View librarian records
* Add new librarians
* Store librarian contact information

---

### 🔍 Search

The system provides search functionality for finding:

* Books
* Students
* Authors

This makes it easier to find records without manually checking the entire database.

---

## 7. Streamlit Application Modules

The Streamlit application is divided into different modules:

```text
📊 Dashboard
👨‍🎓 Students
✍️ Authors
📚 Books
🔄 Issue / Return
👩‍💼 Librarians
🔍 Search
```

The sidebar allows the user to move between different sections of the application.

The frontend communicates with the MySQL database through Python and MySQL Connector.

---

## 8. SQL Concepts Covered

This project demonstrates several important DBMS concepts.

### DDL – Data Definition Language

Used to create and define database structures.

Examples:

```sql
CREATE DATABASE
CREATE TABLE
```

---

### DML – Data Manipulation Language

Used to modify data.

Examples:

```sql
INSERT
UPDATE
DELETE
```

---

### DQL – Data Query Language

Used to retrieve data.

```sql
SELECT
```

---

### Primary Key

A primary key uniquely identifies every record in a table.

Examples:

```text
STUDENT → Student_ID
AUTHOR → Author_ID
BOOK → Book_ID
ISSUE → Issue_ID
LIBRARIAN → Librarian_ID
```

---

### Foreign Key

Foreign keys create relationships between tables.

```text
BOOK.Author_ID → AUTHOR.Author_ID

ISSUE.Student_ID → STUDENT.Student_ID

ISSUE.Book_ID → BOOK.Book_ID
```

---

### Constraints

The database uses different constraints to maintain data accuracy:

* `PRIMARY KEY`
* `FOREIGN KEY`
* `NOT NULL`
* `UNIQUE`
* `CHECK`
* `DEFAULT`

---

### JOIN

JOIN operations can be used to retrieve related information from multiple tables.

Example:

```sql
SELECT BOOK.Title, AUTHOR.Author_Name
FROM BOOK
JOIN AUTHOR
ON BOOK.Author_ID = AUTHOR.Author_ID;
```

---

## 9. Database Normalization

The database is divided into multiple related tables instead of storing all information in one table.

For example, author information is stored separately in the `AUTHOR` table. Books only store the corresponding `Author_ID`.

Similarly, student information is stored in `STUDENT`, while issue transactions are stored in `ISSUE`.

This helps:

* Reduce data duplication
* Improve data consistency
* Make updates easier
* Maintain clear relationships
* Organize the database properly

The design follows the basic principles of **First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF)**.

---

## 10. Example SQL Queries

### Display all students

```sql
SELECT * FROM STUDENT;
```

### Display all books

```sql
SELECT * FROM BOOK;
```

### Display all authors

```sql
SELECT * FROM AUTHOR;
```

### Display currently issued books

```sql
SELECT *
FROM ISSUE
WHERE Status = 'Issued';
```

### Display returned books

```sql
SELECT *
FROM ISSUE
WHERE Status = 'Returned';
```

### Find books with their authors

```sql
SELECT 
    BOOK.Title,
    AUTHOR.Author_Name
FROM BOOK
JOIN AUTHOR
ON BOOK.Author_ID = AUTHOR.Author_ID;
```

### Search for a book

```sql
SELECT *
FROM BOOK
WHERE Title LIKE '%Harry%';
```

### Find issue records of a student

```sql
SELECT *
FROM ISSUE
WHERE Student_ID = 101;
```

### Update a book after returning it

```sql
UPDATE ISSUE
SET Return_Date = CURRENT_DATE,
    Status = 'Returned'
WHERE Issue_ID = 1;
```

---

## 11. Project Files

```text
library_management/
│
├── app.py
├── db.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

### `app.py`

Contains the Streamlit frontend and application functionality.

### `db.py`

Handles the connection between Python and MySQL and contains database operation functions.

### `requirements.txt`

Contains the Python libraries required to run the project.

### `README.md`

Contains information about the project, database design, features, and setup instructions.

### `secrets.toml`

Stores local MySQL connection details.

> Database passwords should not be uploaded to a public GitHub repository.

---

## 12. How to Run the Project

### Step 1: Start MySQL

```bash
brew services start mysql
```

### Step 2: Open the project folder

```bash
cd ~/Desktop/library_management
```

### Step 3: Activate the virtual environment

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the application

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

## 13. Application Workflow

The basic working flow of the system is:

```text
START
  ↓
Open Streamlit Application
  ↓
Connect to MySQL Database
  ↓
Dashboard
  ↓
Manage Students / Authors / Books
  ↓
Issue Book
  ↓
Create Issue Record
  ↓
Return Book
  ↓
Update Issue Record
  ↓
Display Updated Information
  ↓
END
```

---

## 14. Testing

The system can be tested using different operations.

### Student Test

Add a new student and verify that the record is stored in the `STUDENT` table.

### Author Test

Add a new author and verify the record.

### Book Test

Add a book using a valid `Author_ID`.

### Foreign Key Test

Try adding a book with an invalid author ID.

```sql
INSERT INTO BOOK
(Book_ID, Title, Price, Category, Author_ID)
VALUES
(999, 'Test Book', 100, 'Test', 999);
```

The database should reject this record because `Author_ID = 999` does not exist in the `AUTHOR` table.

### Issue Test

Create an issue record for a student and book.

The status should initially be:

```text
Issued
```

### Return Test

Return the book and update the record.

The status should change to:

```text
Returned
```

---

## 15. Future Enhancements

The system can be extended by adding:

* User login and authentication
* Admin and librarian roles
* Automatic fine calculation
* Book availability tracking
* Book reservation
* Borrowing history
* Email notifications
* PDF and Excel reports
* Advanced dashboard analytics
* Online/cloud database
* Mobile-friendly interface

---

## 16. Conclusion

The **Library Management System** provides a simple and organized way to manage library records using a relational database.

The project demonstrates practical use of **MySQL, Python, Streamlit, SQL queries, primary keys, foreign keys, constraints, relationships, normalization, and CRUD operations**.

The most important part of the database is the **ISSUE table**, which manages the transactions between students and books.

Overall, the project shows how DBMS concepts can be applied to build a practical real-world application.

# Library_management
