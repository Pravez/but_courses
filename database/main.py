#!/usr/bin/env python3
"""
Database Generator for School Management System
Generates a database with classes, courses, and students with fake data.
Supports both SQLite and PostgreSQL (with asyncpg).
"""

import random
import argparse
import sys
import asyncio
from datetime import datetime, timedelta
from typing import List
from faker import Faker
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.exc import IntegrityError

# Initialize Faker
fake = Faker()

# Computer Science courses with descriptions
CS_COURSES = [
    (
        "Introduction to Python Programming",
        "Learn Python fundamentals, data structures, and object-oriented programming",
        3,
    ),
    (
        "Advanced JavaScript and Node.js",
        "Master modern JavaScript, async programming, and backend development with Node.js",
        4,
    ),
    (
        "Data Structures and Algorithms",
        "Deep dive into algorithms, complexity analysis, and efficient data structures",
        4,
    ),
    (
        "Web Development with React",
        "Build modern web applications using React, hooks, and state management",
        3,
    ),
    (
        "Machine Learning Fundamentals",
        "Introduction to ML algorithms, neural networks, and practical implementations",
        4,
    ),
    (
        "Database Design and SQL",
        "Learn relational database design, SQL queries, and optimization techniques",
        3,
    ),
    (
        "Cloud Computing with AWS",
        "Explore AWS services, serverless architecture, and cloud deployment strategies",
        3,
    ),
    (
        "Cybersecurity Essentials",
        "Understanding security principles, encryption, and ethical hacking basics",
        3,
    ),
    (
        "Mobile App Development",
        "Create native and cross-platform mobile applications using React Native",
        4,
    ),
    (
        "DevOps and CI/CD Pipelines",
        "Master Docker, Kubernetes, Jenkins, and automated deployment workflows",
        3,
    ),
    (
        "Artificial Intelligence with TensorFlow",
        "Build AI models using TensorFlow, deep learning, and computer vision",
        4,
    ),
    (
        "Blockchain and Smart Contracts",
        "Learn blockchain technology, Ethereum, and Solidity programming",
        3,
    ),
    (
        "Full Stack Development",
        "End-to-end web development covering frontend, backend, and databases",
        4,
    ),
    (
        "System Design and Architecture",
        "Learn scalable system design, microservices, and distributed systems",
        4,
    ),
    (
        "Natural Language Processing",
        "Process and analyze text data using NLP techniques and transformer models",
        3,
    ),
]

# Class information
CLASSES = [
    ("CS-2024-A", "Computer Science - Morning Batch", "2024-09-01"),
    ("CS-2024-B", "Computer Science - Afternoon Batch", "2024-09-01"),
    ("CS-2024-C", "Computer Science - Evening Batch", "2024-09-01"),
    ("CS-2024-D", "Computer Science - Weekend Batch", "2024-09-15"),
]


def normalize_connection_string(db_string: str) -> str:
    """Normalize database connection string for SQLAlchemy async."""
    # Handle postgresql+asyncpg:// format (already correct)
    if db_string.startswith("postgresql+asyncpg://"):
        return db_string

    # Handle postgresql:// format (convert to asyncpg)
    if db_string.startswith("postgresql://"):
        return db_string.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Handle sqlite file paths
    if not db_string.startswith(("sqlite", "postgresql")):
        # Assume it's a file path for SQLite
        return f"sqlite+aiosqlite:///{db_string}"

    # Handle sqlite:// format
    if db_string.startswith("sqlite://"):
        return db_string.replace("sqlite://", "sqlite+aiosqlite://", 1)

    return db_string


def is_postgres(connection_string: str) -> bool:
    """Check if the connection string is for PostgreSQL."""
    return "postgresql" in connection_string


async def create_database(engine: AsyncEngine, is_pg: bool):
    """Create the database and all necessary tables."""

    # Determine the appropriate serial/autoincrement syntax
    serial_type = "SERIAL" if is_pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
    current_timestamp = "CURRENT_TIMESTAMP" if is_pg else "CURRENT_TIMESTAMP"

    async with engine.begin() as conn:
        # Drop existing tables if they exist
        await conn.execute(
            text(
                "DROP TABLE IF EXISTS enrollments CASCADE"
                if is_pg
                else "DROP TABLE IF EXISTS enrollments"
            )
        )
        await conn.execute(
            text(
                "DROP TABLE IF EXISTS students CASCADE"
                if is_pg
                else "DROP TABLE IF EXISTS students"
            )
        )
        await conn.execute(
            text(
                "DROP TABLE IF EXISTS courses CASCADE"
                if is_pg
                else "DROP TABLE IF EXISTS courses"
            )
        )
        await conn.execute(
            text(
                "DROP TABLE IF EXISTS classes CASCADE"
                if is_pg
                else "DROP TABLE IF EXISTS classes"
            )
        )

        # Create classes table
        if is_pg:
            await conn.execute(
                text("""
                CREATE TABLE classes (
                    id SERIAL PRIMARY KEY,
                    class_code VARCHAR(50) UNIQUE NOT NULL,
                    class_name VARCHAR(100) NOT NULL,
                    start_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            )
        else:
            await conn.execute(
                text("""
                CREATE TABLE classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_code VARCHAR(50) UNIQUE NOT NULL,
                    class_name VARCHAR(100) NOT NULL,
                    start_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            )

        # Create courses table
        if is_pg:
            await conn.execute(
                text("""
                CREATE TABLE courses (
                    id SERIAL PRIMARY KEY,
                    course_name VARCHAR(100) NOT NULL,
                    description TEXT,
                    credits INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            )
        else:
            await conn.execute(
                text("""
                CREATE TABLE courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_name VARCHAR(100) NOT NULL,
                    description TEXT,
                    credits INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            )

        # Create students table
        if is_pg:
            await conn.execute(
                text("""
                CREATE TABLE students (
                    id SERIAL PRIMARY KEY,
                    student_id VARCHAR(20) UNIQUE NOT NULL,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    date_of_birth DATE NOT NULL,
                    class_id INTEGER NOT NULL,
                    gpa DECIMAL(3,2),
                    enrollment_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (class_id) REFERENCES classes(id)
                )
            """)
            )
        else:
            await conn.execute(
                text("""
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id VARCHAR(20) UNIQUE NOT NULL,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    date_of_birth DATE NOT NULL,
                    class_id INTEGER NOT NULL,
                    gpa DECIMAL(3,2),
                    enrollment_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (class_id) REFERENCES classes(id)
                )
            """)
            )

        # Create enrollments table
        if is_pg:
            await conn.execute(
                text("""
                CREATE TABLE enrollments (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    enrollment_date DATE NOT NULL,
                    grade VARCHAR(2),
                    status VARCHAR(20) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id),
                    UNIQUE(student_id, course_id)
                )
            """)
            )
        else:
            await conn.execute(
                text("""
                CREATE TABLE enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    enrollment_date DATE NOT NULL,
                    grade VARCHAR(2),
                    status VARCHAR(20) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id),
                    UNIQUE(student_id, course_id)
                )
            """)
            )


async def insert_classes(engine: AsyncEngine, is_pg: bool) -> List[int]:
    """Insert class data into the database."""
    class_ids = []

    async with engine.begin() as conn:
        for class_code, class_name, start_date in CLASSES:
            if is_pg:
                result = await conn.execute(
                    text("""
                        INSERT INTO classes (class_code, class_name, start_date)
                        VALUES (:code, :name, :date)
                        RETURNING id
                    """),
                    {
                        "code": class_code,
                        "name": class_name,
                        "date": datetime.strptime(start_date, "%Y-%m-%d").date()
                        if isinstance(start_date, str)
                        else start_date,
                    },
                )
                class_ids.append(result.fetchone()[0])
            else:
                result = await conn.execute(
                    text("""
                        INSERT INTO classes (class_code, class_name, start_date)
                        VALUES (:code, :name, :date)
                    """),
                    {"code": class_code, "name": class_name, "date": start_date},
                )
                class_ids.append(result.lastrowid)

    print(f"✓ Inserted {len(CLASSES)} classes")
    return class_ids


async def insert_courses(engine: AsyncEngine, is_pg: bool) -> List[int]:
    """Insert course data into the database."""
    course_ids = []

    async with engine.begin() as conn:
        for course_name, description, credits in CS_COURSES:
            if is_pg:
                result = await conn.execute(
                    text("""
                        INSERT INTO courses (course_name, description, credits)
                        VALUES (:name, :desc, :credits)
                        RETURNING id
                    """),
                    {"name": course_name, "desc": description, "credits": credits},
                )
                course_ids.append(result.fetchone()[0])
            else:
                result = await conn.execute(
                    text("""
                        INSERT INTO courses (course_name, description, credits)
                        VALUES (:name, :desc, :credits)
                    """),
                    {"name": course_name, "desc": description, "credits": credits},
                )
                course_ids.append(result.lastrowid)

    print(f"✓ Inserted {len(CS_COURSES)} courses")
    return course_ids


def generate_student_id() -> str:
    """Generate a unique student ID."""
    year = random.randint(2020, 2024)
    number = random.randint(1000, 9999)
    return f"STU{year}{number}"


async def insert_students(
    engine: AsyncEngine, class_ids: List[int], students_per_class: int, is_pg: bool
) -> List[int]:
    """Insert student data into the database."""
    student_ids = []
    used_student_codes = set()
    used_emails = set()

    async with engine.begin() as conn:
        for class_id in class_ids:
            for _ in range(students_per_class):
                # Generate unique student ID
                while True:
                    student_id = generate_student_id()
                    if student_id not in used_student_codes:
                        used_student_codes.add(student_id)
                        break

                first_name = fake.first_name()
                last_name = fake.last_name()

                # Generate unique email
                while True:
                    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@university.edu"
                    if email not in used_emails:
                        used_emails.add(email)
                        break

                # Generate date of birth (18-25 years old)
                days_old = random.randint(18 * 365, 25 * 365)
                date_of_birth = (datetime.now() - timedelta(days=days_old)).strftime(
                    "%Y-%m-%d"
                )

                # Generate GPA (2.0 - 4.0)
                gpa = round(random.uniform(2.0, 4.0), 2)

                # Enrollment date within the last year
                enrollment_days_ago = random.randint(0, 365)
                enrollment_date = (
                    datetime.now() - timedelta(days=enrollment_days_ago)
                ).strftime("%Y-%m-%d")

                if is_pg:
                    result = await conn.execute(
                        text("""
                            INSERT INTO students (student_id, first_name, last_name, email, 
                                                 date_of_birth, class_id, gpa, enrollment_date)
                            VALUES (:sid, :fname, :lname, :email, :dob, :cid, :gpa, :edate)
                            RETURNING id
                        """),
                        {
                            "sid": student_id,
                            "fname": first_name,
                            "lname": last_name,
                            "email": email,
                            "dob": datetime.strptime(date_of_birth, "%Y-%m-%d").date(),
                            "cid": class_id,
                            "gpa": gpa,
                            "edate": datetime.strptime(
                                enrollment_date, "%Y-%m-%d"
                            ).date(),
                        },
                    )
                    student_ids.append(result.fetchone()[0])
                else:
                    result = await conn.execute(
                        text("""
                            INSERT INTO students (student_id, first_name, last_name, email, 
                                                 date_of_birth, class_id, gpa, enrollment_date)
                            VALUES (:sid, :fname, :lname, :email, :dob, :cid, :gpa, :edate)
                        """),
                        {
                            "sid": student_id,
                            "fname": first_name,
                            "lname": last_name,
                            "email": email,
                            "dob": date_of_birth,
                            "cid": class_id,
                            "gpa": gpa,
                            "edate": enrollment_date,
                        },
                    )
                    student_ids.append(result.lastrowid)

    print(f"✓ Inserted {len(student_ids)} students ({students_per_class} per class)")
    return student_ids


async def insert_enrollments(
    engine: AsyncEngine, student_ids: List[int], course_ids: List[int]
) -> int:
    """Insert enrollment data (students enrolled in courses)."""
    grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", None]
    statuses = ["active", "active", "active", "active", "completed", "completed"]

    enrollment_count = 0

    async with engine.begin() as conn:
        for student_id in student_ids:
            # Each student enrolls in 3-7 random courses
            num_courses = random.randint(3, 7)
            selected_courses = random.sample(course_ids, num_courses)

            for course_id in selected_courses:
                # Enrollment date within the last 6 months
                enrollment_days_ago = random.randint(0, 180)
                enrollment_date = (
                    datetime.now() - timedelta(days=enrollment_days_ago)
                ).strftime("%Y-%m-%d")

                status = random.choice(statuses)
                # Only completed courses have grades
                grade = random.choice(grades) if status == "completed" else None

                try:
                    await conn.execute(
                        text("""
                            INSERT INTO enrollments (student_id, course_id, enrollment_date, grade, status)
                            VALUES (:sid, :cid, :edate, :grade, :status)
                        """),
                        {
                            "sid": student_id,
                            "cid": course_id,
                            "edate": datetime.strptime(
                                enrollment_date, "%Y-%m-%d"
                            ).date()
                            if "postgresql" in str(conn.engine.url)
                            else enrollment_date,
                            "grade": grade,
                            "status": status,
                        },
                    )
                    enrollment_count += 1
                except IntegrityError:
                    # Skip if this enrollment already exists
                    pass

    print(f"✓ Inserted {enrollment_count} course enrollments")
    return enrollment_count


async def print_statistics(engine: AsyncEngine):
    """Print database statistics."""
    print("\n" + "=" * 60)
    print("DATABASE STATISTICS")
    print("=" * 60)

    async with engine.connect() as conn:
        # Classes
        result = await conn.execute(text("SELECT COUNT(*) FROM classes"))
        print(f"Total Classes: {result.fetchone()[0]}")

        # Courses
        result = await conn.execute(text("SELECT COUNT(*) FROM courses"))
        print(f"Total Courses: {result.fetchone()[0]}")

        # Students
        result = await conn.execute(text("SELECT COUNT(*) FROM students"))
        print(f"Total Students: {result.fetchone()[0]}")

        # Enrollments
        result = await conn.execute(text("SELECT COUNT(*) FROM enrollments"))
        print(f"Total Enrollments: {result.fetchone()[0]}")

        # Students per class
        print("\nStudents per class:")
        result = await conn.execute(
            text("""
            SELECT c.class_code, c.class_name, COUNT(s.id) as student_count
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            GROUP BY c.id, c.class_code, c.class_name
        """)
        )
        for row in result:
            print(f"  {row[0]} ({row[1]}): {row[2]} students")

        # Average GPA per class
        print("\nAverage GPA per class:")
        result = await conn.execute(
            text("""
            SELECT c.class_code, ROUND(AVG(s.gpa)::numeric, 2) as avg_gpa
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            GROUP BY c.id, c.class_code
        """)
            if "postgresql" in str(engine.url)
            else text("""
            SELECT c.class_code, ROUND(AVG(s.gpa), 2) as avg_gpa
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            GROUP BY c.id
        """)
        )
        for row in result:
            print(f"  {row[0]}: {row[1]}")

        # Most popular courses
        print("\nTop 5 most popular courses:")
        result = await conn.execute(
            text("""
            SELECT c.course_name, COUNT(e.id) as enrollment_count
            FROM courses c
            LEFT JOIN enrollments e ON c.id = e.course_id
            GROUP BY c.id, c.course_name
            ORDER BY enrollment_count DESC
            LIMIT 5
        """)
        )
        for row in result:
            print(f"  {row[0]}: {row[1]} enrollments")

    print("=" * 60)


async def check_tables_exist(engine: AsyncEngine, is_pg: bool) -> bool:
    """Return True if all required tables already exist in the target database.

    Required tables: classes, courses, students, enrollments.
    """
    required = {"classes", "courses", "students", "enrollments"}
    try:
        async with engine.connect() as conn:
            if is_pg:
                # Fetch all public tables and check set inclusion to avoid driver-specific array binding quirks
                result = await conn.execute(
                    text(
                        """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    """
                    )
                )
            else:
                result = await conn.execute(
                    text(
                        """
                    SELECT name as table_name
                    FROM sqlite_master
                    WHERE type='table'
                    """
                    )
                )

            found = {row[0] for row in result}
            return required.issubset(found)
    except Exception:
        # If anything goes wrong, assume tables do not fully exist
        return False


async def async_main(db_connection: str, students_per_class: int):
    """Async main function to generate the database."""
    print("\n" + "=" * 60)
    print("SCHOOL DATABASE GENERATOR")
    print("=" * 60 + "\n")

    # Normalize connection string
    connection_string = normalize_connection_string(db_connection)
    is_pg = is_postgres(connection_string)

    print(f"Database: {db_connection}")
    print(f"Connection String: {connection_string}")
    print(f"Database Type: {'PostgreSQL' if is_pg else 'SQLite'}")
    print(f"Students per class: {students_per_class}\n")

    try:
        # Create async engine
        engine = create_async_engine(connection_string, echo=False)

        # If all tables already exist, only print statistics
        if await check_tables_exist(engine, is_pg):
            print(
                "Existing database detected. Tables already present. Showing statistics only...\n"
            )
            await print_statistics(engine)
            await engine.dispose()
            print("\n✓ Statistics displayed. No changes made.")
            print(f"✓ Connection string: {connection_string}\n")
            return

        print("Creating database schema...")
        await create_database(engine, is_pg)

        print("Populating database with fake data...\n")

        # Insert data
        class_ids = await insert_classes(engine, is_pg)
        course_ids = await insert_courses(engine, is_pg)
        student_ids = await insert_students(
            engine, class_ids, students_per_class, is_pg
        )
        await insert_enrollments(engine, student_ids, course_ids)

        # Print statistics
        await print_statistics(engine)

        # Close engine
        await engine.dispose()

        print("\n✓ Database populated successfully!")
        print(f"✓ Connection string: {connection_string}\n")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a school management database with fake data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # SQLite
  %(prog)s school_management.db
  %(prog)s sqlite:///school.db

  # PostgreSQL with asyncpg
  %(prog)s "postgresql+asyncpg://user:pass@localhost/schooldb"
  %(prog)s "postgresql://user:pass@localhost:5432/schooldb"

  # Custom students per class
  %(prog)s school.db --students-per-class 50
        """,
    )

    parser.add_argument(
        "database",
        type=str,
        help="Database connection string (e.g., postgresql+asyncpg://user:pass@host/db or file.db for SQLite)",
    )

    parser.add_argument(
        "--students-per-class",
        type=int,
        default=30,
        metavar="N",
        help="Number of students per class (default: 30)",
    )

    args = parser.parse_args()

    # Run async main
    asyncio.run(async_main(args.database, args.students_per_class))


if __name__ == "__main__":
    main()
