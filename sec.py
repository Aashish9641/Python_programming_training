import csv

class Student:
    def __init__(self, student_id, name, age, roll_no, grade, courses=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.roll_no = roll_no
        self.grade = grade
        self.courses = courses if courses else []

    def __str__(self):
        courses_str = ", ".join(self.courses) if self.courses else "None"
        return (f"Student ID: {self.student_id}, Name: {self.name}, Age: {self.age}, "
                f"Roll No: {self.roll_no}, Grade: {self.grade}, Courses: {courses_str}")


class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

    def __str__(self):
        return f"Course ID: {self.course_id}, Name: {self.course_name}"


class StudentManager:
    def __init__(self):
        self.FILE_NAME = "students.csv"
        self.COURSE_FILE_NAME = "courses.csv"
        self.students = []
        self.courses = []

    def load_students(self):
        """Load students from the CSV file."""
        try:
            with open(self.FILE_NAME, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.students.append(
                        Student(
                            student_id=row["student_id"],
                            name=row["name"],
                            age=int(row["age"]),
                            roll_no=row["roll_no"],
                            grade=row["grade"],
                            courses=row.get("courses", "").split(",") if row.get("courses") else []
                        )
                    )
        except FileNotFoundError:
            print(f"File '{self.FILE_NAME}' not found. Starting with an empty list of students.")

    def load_courses(self):
        """Load courses from the CSV file."""
        try:
            with open(self.COURSE_FILE_NAME, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.courses.append(Course(course_id=row["course_id"], course_name=row["course_name"]))
        except FileNotFoundError:
            print(f"File '{self.COURSE_FILE_NAME}' not found. Starting with an empty list of courses.")

    def display_students(self):
        """Display all students."""
        if not self.students:
            print("No students available.")
        else:
            for student in self.students:
                print(student)

    def display_courses(self):
        """Display all courses."""
        if not self.courses:
            print("No courses available.")
        else:
            for course in self.courses:
                print(course)

    def add_student(self, student):
        """Add a new student and save to file."""
        self.students.append(student)
        self.save_students()

    def add_student_interactive(self):
        """Interactively add a new student."""
        print("\nEnter the details of the new student:")
        student_id = input("Student ID: ")
        name = input("Name: ")
        age = int(input("Age: "))
        roll_no = input("Roll No: ")
        grade = input("Grade: ")

        new_student = Student(student_id=student_id, name=name, age=age, roll_no=roll_no, grade=grade)
        self.add_student(new_student)
        print("\nStudent added successfully!")

    def delete_student(self, student_id=None):
        """Delete a student based on student ID (interactively or passed as argument)."""
        if student_id is None:
            student_id = input("Enter the Student ID of the student to delete: ")

        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                self.save_students()
                print(f"\nStudent with ID {student_id} deleted successfully!")
                return
        print(f"\nStudent with ID {student_id} not found.")

    def add_course(self):
        """Interactively add a new course."""
        course_id = input("Enter Course ID: ")
        course_name = input("Enter Course Name: ")

        self.courses.append(Course(course_id=course_id, course_name=course_name))
        self.save_courses()
        print("\nCourse added successfully!")

    def delete_course(self):
        """Delete a course by course ID."""
        course_id = input("Enter Course ID to delete: ")
        for course in self.courses:
            if course.course_id == course_id:
                self.courses.remove(course)
                self.save_courses()
                print(f"\nCourse with ID {course_id} deleted successfully!")
                return
        print(f"\nCourse with ID {course_id} not found.")

    def assign_course_to_student(self):
        """Assign a course to a student."""
        student_id = input("Enter Student ID: ")
        for student in self.students:
            if student.student_id == student_id:
                course_id = input("Enter Course ID to assign: ")
                for course in self.courses:
                    if course.course_id == course_id:
                        student.courses.append(course.course_name)
                        self.save_students()
                        print(f"\nCourse '{course.course_name}' assigned to student {student.name}.")
                        return
                print(f"\nCourse with ID {course_id} not found.")
                return
        print(f"\nStudent with ID {student_id} not found.")

    def save_students(self):
        """Save students to the CSV file."""
        with open(self.FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["student_id", "name", "age", "roll_no", "grade", "courses"])
            writer.writeheader()
            for student in self.students:
                writer.writerow({
                    "student_id": student.student_id,
                    "name": student.name,
                    "age": student.age,
                    "roll_no": student.roll_no,
                    "grade": student.grade,
                    "courses": ",".join(student.courses)
                })

    def save_courses(self):
        """Save courses to the CSV file."""
        with open(self.COURSE_FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["course_id", "course_name"])
            writer.writeheader()
            for course in self.courses:
                writer.writerow({"course_id": course.course_id, "course_name": course.course_name})


# Main program
manager = StudentManager()
manager.load_students()
manager.load_courses()

while True:
    print("\nMenu:")
    print("1. Display Students")
    print("2. Add Student")
    print("3. Delete Student")
    print("4. Display Courses")
    print("5. Add Course")
    print("6. Delete Course")
    print("7. Assign Course to Student")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nCurrent Students:")
        manager.display_students()
    elif choice == "2":
        manager.add_student_interactive()
    elif choice == "3":
        manager.delete_student()
    elif choice == "4":
        print("\nAvailable Courses:")
        manager.display_courses()
    elif choice == "5":
        manager.add_course()
    elif choice == "6":
        manager.delete_course()
    elif choice == "7":
        manager.assign_course_to_student()
    elif choice == "8":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please try again.")
