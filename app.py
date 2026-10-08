import streamlit as st
from datetime import date
from db import get_connection, fetch_data, execute_query


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("📚 Library Management System")



# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

try:
    connection = get_connection()
    connection.close()
    database_connected = True

except Exception as e:
    database_connected = False

    st.error("❌ Database connection failed.")
    st.code(str(e))

    st.stop()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("📚 Library System")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Students",
        "Authors",
        "Books",
        "Issue / Return",
        "Librarians",
        "Search"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header("🏠 Dashboard")

    student_count = fetch_data(
        "SELECT COUNT(*) AS total FROM STUDENT"
    ).iloc[0]["total"]

    author_count = fetch_data(
        "SELECT COUNT(*) AS total FROM AUTHOR"
    ).iloc[0]["total"]

    book_count = fetch_data(
        "SELECT COUNT(*) AS total FROM BOOK"
    ).iloc[0]["total"]

    issued_count = fetch_data(
        """
        SELECT COUNT(*) AS total
        FROM ISSUE
        WHERE Status = 'Issued'
        """
    ).iloc[0]["total"]

    returned_count = fetch_data(
        """
        SELECT COUNT(*) AS total
        FROM ISSUE
        WHERE Status = 'Returned'
        """
    ).iloc[0]["total"]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("👨‍🎓 Students", student_count)
    col2.metric("✍️ Authors", author_count)
    col3.metric("📖 Books", book_count)
    col4.metric("📕 Issued", issued_count)
    col5.metric("📗 Returned", returned_count)

    st.divider()

    st.subheader("📋 Recent Issue Records")

    recent = fetch_data(
        """
        SELECT
            I.Issue_ID,
            S.Name AS Student,
            B.Title AS Book,
            I.Issue_Date,
            I.Return_Date,
            I.Status
        FROM ISSUE I
        JOIN STUDENT S
            ON I.Student_ID = S.Student_ID
        JOIN BOOK B
            ON I.Book_ID = B.Book_ID
        ORDER BY I.Issue_ID DESC
        LIMIT 10
        """
    )

    if recent.empty:
        st.info("No issue records available.")

    else:
        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# STUDENTS
# =========================================================

elif page == "Students":

    st.header("👨‍🎓 Student Management")

    tab_view, tab_add = st.tabs(
        ["View Students", "Add Student"]
    )

    with tab_view:

        students = fetch_data(
            """
            SELECT
                Student_ID,
                Name,
                Email,
                Phone,
                Department
            FROM STUDENT
            ORDER BY Student_ID
            """
        )

        st.dataframe(
            students,
            use_container_width=True,
            hide_index=True
        )

    with tab_add:

        with st.form("add_student"):

            student_id = st.number_input(
                "Student ID",
                min_value=1,
                step=1
            )

            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            department = st.text_input("Department")

            submit = st.form_submit_button("Add Student")

            if submit:

                if name.strip() == "":
                    st.warning("Please enter the student name.")

                else:

                    success, message = execute_query(
                        """
                        INSERT INTO STUDENT
                        (
                            Student_ID,
                            Name,
                            Email,
                            Phone,
                            Department
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            student_id,
                            name,
                            email,
                            phone,
                            department
                        )
                    )

                    if success:
                        st.success("✅ Student added successfully.")
                        st.rerun()

                    else:
                        st.error(message)


# =========================================================
# AUTHORS
# =========================================================

elif page == "Authors":

    st.header("✍️ Author Management")

    tab_view, tab_add = st.tabs(
        ["View Authors", "Add Author"]
    )

    with tab_view:

        authors = fetch_data(
            """
            SELECT
                Author_ID,
                Author_Name
            FROM AUTHOR
            ORDER BY Author_ID
            """
        )

        st.dataframe(
            authors,
            use_container_width=True,
            hide_index=True
        )

    with tab_add:

        with st.form("add_author"):

            author_id = st.number_input(
                "Author ID",
                min_value=1,
                step=1
            )

            author_name = st.text_input("Author Name")

            submit = st.form_submit_button("Add Author")

            if submit:

                if author_name.strip() == "":
                    st.warning("Please enter the author name.")

                else:

                    success, message = execute_query(
                        """
                        INSERT INTO AUTHOR
                        (
                            Author_ID,
                            Author_Name
                        )
                        VALUES (%s, %s)
                        """,
                        (
                            author_id,
                            author_name
                        )
                    )

                    if success:
                        st.success("✅ Author added successfully.")
                        st.rerun()

                    else:
                        st.error(message)


# =========================================================
# BOOKS
# =========================================================

elif page == "Books":

    st.header("📖 Book Management")

    tab_view, tab_add = st.tabs(
        ["View Books", "Add Book"]
    )

    with tab_view:

        books = fetch_data(
            """
            SELECT
                B.Book_ID,
                B.Title,
                B.Price,
                B.Category,
                A.Author_Name
            FROM BOOK B
            LEFT JOIN AUTHOR A
                ON B.Author_ID = A.Author_ID
            ORDER BY B.Book_ID
            """
        )

        st.dataframe(
            books,
            use_container_width=True,
            hide_index=True
        )

    with tab_add:

        authors = fetch_data(
            """
            SELECT
                Author_ID,
                Author_Name
            FROM AUTHOR
            ORDER BY Author_Name
            """
        )

        if authors.empty:

            st.warning(
                "Please add an author before adding a book."
            )

        else:

            author_options = {
                f"{row['Author_ID']} - {row['Author_Name']}":
                row["Author_ID"]
                for _, row in authors.iterrows()
            }

            with st.form("add_book"):

                book_id = st.number_input(
                    "Book ID",
                    min_value=1,
                    step=1
                )

                title = st.text_input("Book Title")

                price = st.number_input(
                    "Price",
                    min_value=0.01,
                    step=0.01
                )

                category = st.text_input("Category")

                selected_author = st.selectbox(
                    "Author",
                    list(author_options.keys())
                )

                submit = st.form_submit_button("Add Book")

                if submit:

                    if title.strip() == "":
                        st.warning("Please enter the book title.")

                    else:

                        author_id = author_options[
                            selected_author
                        ]

                        success, message = execute_query(
                            """
                            INSERT INTO BOOK
                            (
                                Book_ID,
                                Title,
                                Price,
                                Category,
                                Author_ID
                            )
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (
                                book_id,
                                title,
                                price,
                                category,
                                author_id
                            )
                        )

                        if success:
                            st.success(
                                "✅ Book added successfully."
                            )
                            st.rerun()

                        else:
                            st.error(message)


# =========================================================
# ISSUE / RETURN
# =========================================================

elif page == "Issue / Return":

    st.header("🔄 Issue / Return Books")

    tab_issue, tab_return = st.tabs(
        ["Issue Book", "Return Book"]
    )

    # -----------------------------------------------------
    # ISSUE BOOK
    # -----------------------------------------------------

    with tab_issue:

        students = fetch_data(
            """
            SELECT
                Student_ID,
                Name
            FROM STUDENT
            ORDER BY Name
            """
        )

        books = fetch_data(
            """
            SELECT
                Book_ID,
                Title
            FROM BOOK
            ORDER BY Title
            """
        )

        if students.empty:

            st.warning(
                "Please add students first."
            )

        elif books.empty:

            st.warning(
                "Please add books first."
            )

        else:

            student_options = {
                f"{row['Student_ID']} - {row['Name']}":
                row["Student_ID"]
                for _, row in students.iterrows()
            }

            book_options = {
                f"{row['Book_ID']} - {row['Title']}":
                row["Book_ID"]
                for _, row in books.iterrows()
            }

            with st.form("issue_book"):

                issue_id = st.number_input(
                    "Issue ID",
                    min_value=1,
                    step=1
                )

                selected_student = st.selectbox(
                    "Student",
                    list(student_options.keys())
                )

                selected_book = st.selectbox(
                    "Book",
                    list(book_options.keys())
                )

                issue_date = st.date_input(
                    "Issue Date",
                    value=date.today()
                )

                submit = st.form_submit_button(
                    "Issue Book"
                )

                if submit:

                    student_id = student_options[
                        selected_student
                    ]

                    book_id = book_options[
                        selected_book
                    ]

                    success, message = execute_query(
                        """
                        INSERT INTO ISSUE
                        (
                            Issue_ID,
                            Student_ID,
                            Book_ID,
                            Issue_Date,
                            Status
                        )
                        VALUES (%s, %s, %s, %s, 'Issued')
                        """,
                        (
                            issue_id,
                            student_id,
                            book_id,
                            issue_date
                        )
                    )

                    if success:
                        st.success(
                            "✅ Book issued successfully."
                        )
                        st.rerun()

                    else:
                        st.error(message)

    # -----------------------------------------------------
    # RETURN BOOK
    # -----------------------------------------------------

    with tab_return:

        issued_books = fetch_data(
            """
            SELECT
                I.Issue_ID,
                S.Name AS Student,
                B.Title AS Book,
                I.Issue_Date
            FROM ISSUE I
            JOIN STUDENT S
                ON I.Student_ID = S.Student_ID
            JOIN BOOK B
                ON I.Book_ID = B.Book_ID
            WHERE I.Status = 'Issued'
            ORDER BY I.Issue_ID
            """
        )

        if issued_books.empty:

            st.info("No books are currently issued.")

        else:

            st.dataframe(
                issued_books,
                use_container_width=True,
                hide_index=True
            )

            issue_ids = issued_books["Issue_ID"].tolist()

            selected_issue = st.selectbox(
                "Select Issue ID",
                issue_ids
            )

            return_date = st.date_input(
                "Return Date",
                value=date.today()
            )

            if st.button(
                "📗 Return Book",
                type="primary"
            ):

                success, message = execute_query(
                    """
                    UPDATE ISSUE
                    SET
                        Return_Date = %s,
                        Status = 'Returned'
                    WHERE Issue_ID = %s
                    """,
                    (
                        return_date,
                        selected_issue
                    )
                )

                if success:
                    st.success(
                        "✅ Book returned successfully."
                    )
                    st.rerun()

                else:
                    st.error(message)


# =========================================================
# LIBRARIANS
# =========================================================

elif page == "Librarians":

    st.header("👩‍💼 Librarian Management")

    tab_view, tab_add = st.tabs(
        ["View Librarians", "Add Librarian"]
    )

    with tab_view:

        librarians = fetch_data(
            """
            SELECT
                Librarian_ID,
                Name,
                Email
            FROM LIBRARIAN
            ORDER BY Librarian_ID
            """
        )

        st.dataframe(
            librarians,
            use_container_width=True,
            hide_index=True
        )

    with tab_add:

        with st.form("add_librarian"):

            librarian_id = st.number_input(
                "Librarian ID",
                min_value=1,
                step=1
            )

            name = st.text_input("Name")
            email = st.text_input("Email")

            submit = st.form_submit_button(
                "Add Librarian"
            )

            if submit:

                if name.strip() == "":
                    st.warning(
                        "Please enter the librarian name."
                    )

                else:

                    success, message = execute_query(
                        """
                        INSERT INTO LIBRARIAN
                        (
                            Librarian_ID,
                            Name,
                            Email
                        )
                        VALUES (%s, %s, %s)
                        """,
                        (
                            librarian_id,
                            name,
                            email
                        )
                    )

                    if success:
                        st.success(
                            "✅ Librarian added successfully."
                        )
                        st.rerun()

                    else:
                        st.error(message)


# =========================================================
# SEARCH
# =========================================================

elif page == "Search":

    st.header("🔍 Search Library")

    search_type = st.selectbox(
        "Search By",
        [
            "Books",
            "Students",
            "Authors"
        ]
    )

    keyword = st.text_input(
        "Enter search keyword"
    )

    if keyword.strip():

        search = f"%{keyword}%"

        if search_type == "Books":

            results = fetch_data(
                """
                SELECT
                    B.Book_ID,
                    B.Title,
                    B.Price,
                    B.Category,
                    A.Author_Name
                FROM BOOK B
                LEFT JOIN AUTHOR A
                    ON B.Author_ID = A.Author_ID
                WHERE B.Title LIKE %s
                   OR B.Category LIKE %s
                   OR A.Author_Name LIKE %s
                ORDER BY B.Title
                """,
                (
                    search,
                    search,
                    search
                )
            )

        elif search_type == "Students":

            results = fetch_data(
                """
                SELECT
                    Student_ID,
                    Name,
                    Email,
                    Phone,
                    Department
                FROM STUDENT
                WHERE Name LIKE %s
                   OR Email LIKE %s
                   OR Department LIKE %s
                ORDER BY Name
                """,
                (
                    search,
                    search,
                    search
                )
            )

        else:

            results = fetch_data(
                """
                SELECT
                    Author_ID,
                    Author_Name
                FROM AUTHOR
                WHERE Author_Name LIKE %s
                ORDER BY Author_Name
                """,
                (search,)
            )

        if results.empty:

            st.info("No matching records found.")

        else:

            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True
            )