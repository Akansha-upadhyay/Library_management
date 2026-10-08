CREATE DATABASE library_management;

USE library_management;


CREATE TABLE STUDENT (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Department VARCHAR(50)
);

SHOW TABLES;


CREATE TABLE AUTHOR (
    Author_ID INT PRIMARY KEY,
    Author_Name VARCHAR(100) NOT NULL
);


CREATE TABLE BOOK (
    Book_ID INT PRIMARY KEY,
    Title VARCHAR(150) NOT NULL,
    Price DECIMAL(10,2) CHECK (Price > 0),
    Category VARCHAR(50),
    Author_ID INT,
    FOREIGN KEY (Author_ID) REFERENCES AUTHOR(Author_ID)
);


CREATE TABLE ISSUE (
    Issue_ID INT PRIMARY KEY,
    Student_ID INT NOT NULL,
    Book_ID INT NOT NULL,
    Issue_Date DATE NOT NULL,
    Return_Date DATE DEFAULT NULL,
    Status VARCHAR(20) DEFAULT 'Issued',
    FOREIGN KEY (Student_ID) REFERENCES STUDENT(Student_ID),
    FOREIGN KEY (Book_ID) REFERENCES BOOK(Book_ID)
);


CREATE TABLE LIBRARIAN (
    Librarian_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE
);

USE library_management;

INSERT INTO STUDENT
(Student_ID, Name, Email, Phone, Department)
VALUES
(101, 'Aarav Sharma', 'aarav@gmail.com', '9876543210', 'CSE'),
(102, 'Priya Verma', 'priya@gmail.com', '9876543211', 'IT'),
(103, 'Rahul Singh', 'rahul@gmail.com', '9876543212', 'ECE'),
(104, 'Sneha Patel', 'sneha@gmail.com', '9876543213', 'CSE'),
(105, 'Rohan Gupta', 'rohan@gmail.com', '9876543214', 'IT');

SHOW TABLES;

SELECT * FROM STUDENT;

USE library_management;

INSERT INTO AUTHOR (Author_ID, Author_Name)
VALUES
(201, 'Chetan Bhagat'),
(202, 'R. K. Narayan'),
(203, 'A. P. J. Abdul Kalam'),
(204, 'J. K. Rowling'),
(205, 'George Orwell');

SELECT * FROM AUTHOR;

USE library_management;

INSERT INTO BOOK
(Book_ID, Title, Price, Category, Author_ID)
VALUES
(301, 'Five Point Someone', 350.00, 'Fiction', 201),
(302, 'Malgudi Days', 280.00, 'Fiction', 202),
(303, 'Wings of Fire', 400.00, 'Biography', 203),
(304, 'Harry Potter', 500.00, 'Fantasy', 204),
(305, 'Animal Farm', 250.00, 'Political Fiction', 205);

SELECT * FROM BOOK;

USE library_management;

INSERT INTO LIBRARIAN
(Librarian_ID, Name, Email)
VALUES
(401, 'Anita Sharma', 'anita@library.com'),
(402, 'Vikram Singh', 'vikram@library.com'),
(403, 'Neha Verma', 'neha@library.com');

SELECT * FROM LIBRARIAN;

USE library_management;

INSERT INTO ISSUE
(Issue_ID, Student_ID, Book_ID, Issue_Date, Return_Date, Status)
VALUES
(501, 101, 301, '2026-09-01', NULL, 'Issued'),
(502, 102, 302, '2026-09-03', '2026-09-10', 'Returned'),
(503, 103, 303, '2026-09-05', NULL, 'Issued'),
(504, 104, 304, '2026-09-08', NULL, 'Issued'),
(505, 105, 305, '2026-09-10', '2026-09-17', 'Returned');

SELECT * FROM ISSUE;

SHOW TABLES;

USE library_management;

SELECT
    STUDENT.Name AS Student_Name,
    BOOK.Title AS Book_Title,
    ISSUE.Issue_Date,
    ISSUE.Return_Date,
    ISSUE.Status
FROM ISSUE
JOIN STUDENT
    ON ISSUE.Student_ID = STUDENT.Student_ID
JOIN BOOK
    ON ISSUE.Book_ID = BOOK.Book_ID;

  USE library_management;

SELECT
    ISSUE.Issue_ID,
    STUDENT.Name AS Student_Name,
    BOOK.Title AS Book_Title,
    ISSUE.Issue_Date,
    ISSUE.Status
FROM ISSUE
JOIN STUDENT
    ON ISSUE.Student_ID = STUDENT.Student_ID
JOIN BOOK
    ON ISSUE.Book_ID = BOOK.Book_ID
WHERE ISSUE.Status = 'Issued';

USE library_management;

SELECT
    STUDENT.Student_ID,
    STUDENT.Name AS Student_Name,
    COUNT(ISSUE.Issue_ID) AS Total_Books
FROM STUDENT
LEFT JOIN ISSUE
    ON STUDENT.Student_ID = ISSUE.Student_ID
GROUP BY
    STUDENT.Student_ID,
    STUDENT.Name;

USE library_management;

SELECT
    BOOK.Book_ID,
    BOOK.Title AS Book_Title,
    AUTHOR.Author_Name,
    BOOK.Price,
    BOOK.Category
FROM BOOK
JOIN AUTHOR
    ON BOOK.Author_ID = AUTHOR.Author_ID;

USE library_management;

SELECT
    Category,
    COUNT(Book_ID) AS Total_Books
FROM BOOK
GROUP BY Category;

USE library_management;

UPDATE ISSUE
SET
    Return_Date = '2026-09-30',
    Status = 'Returned'
WHERE Issue_ID = 501;

SELECT * FROM ISSUE
WHERE Issue_ID = 501;

USE library_management;

SELECT
    Book_ID,
    Title,
    Price,
    Category
FROM BOOK
ORDER BY Price DESC;

ORDER BY Price ASC;

INSERT INTO BOOK
(Book_ID, Title, Price, Category, Author_ID)
VALUES
(306, 'Invalid Book', -50.00, 'Fiction', 201);

SELECT * FROM BOOK
WHERE Book_ID = 306;

DESCRIBE STUDENT;

DESCRIBE AUTHOR;

DESCRIBE BOOK;

DESCRIBE ISSUE;

DESCRIBE LIBRARIAN;

