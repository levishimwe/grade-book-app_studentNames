import pickle
import os

class Student:
    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.courses = {}  # {course_name: grade}
        self.gpa = 0.0

    def register_course(self, course):
        self.courses[course.name] = None  # Initially no grade

    def add_grade(self, course_name, grade):
        if course_name in self.courses:
            self.courses[course_name] = grade
            self.calculate_gpa()

    def calculate_gpa(self):
        total_points = sum(self.courses.values())
        self.gpa = total_points / len(self.courses) if self.courses else 0.0

    def generate_transcript(self):
        transcript = f"Transcript for {self.first_name} {self.last_name} ({self.email})\n"
        transcript += f"GPA: {self.gpa:.2f}\n"
        transcript += "Courses:\n"
        for course, grade in self.courses.items():
            transcript += f"- {course}: {grade if grade is not None else 'Not graded'}\n"
        return transcript

class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits

class GradeBook:
    def __init__(self):
        self.students = []
        self.courses = []
        self.data_file = 'gradebook_data.pkl'

    def add_student(self, student):
        self.students.append(student)

    def add_course(self, course):
        self.courses.append(course)

    def get_student_by_email(self, email):
        return next((s for s in self.students if s.email == email), None)

    def get_course_by_name(self, name):
        return next((c for c in self.courses if c.name == name), None)

    def register_student_for_course(self, student_email, course_name):
        student = self.get_student_by_email(student_email)
        course = self.get_course_by_name(course_name)
        if student and course:
            student.register_course(course)
            return True
        return False

    def add_grade_to_student(self, student_email, course_name, grade):
        student = self.get_student_by_email(student_email)
        if student:
            student.add_grade(course_name, grade)
            return True
        return False

    def rank_students_by_gpa(self):
        return sorted(self.students, key=lambda s: s.gpa, reverse=True)

    def search_students_by_grade(self, course_name, grade):
        return [s for s in self.students if s.courses.get(course_name) == grade]
    
    def save_data(self):
        with open(self.data_file, 'wb') as file:
            pickle.dump((self.students, self.courses), file)
        print("Data saved successfully.")

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as file:
                self.students, self.courses = pickle.load(file)
            print("Data loaded successfully.")
        else:
            print("No saved data found.")
    def list_all_courses(self):
        return self.courses


# User Interface
def main():
    grade_book = GradeBook()
    grade_book.load_data()

    while True:
        print("\nGrade Book Application")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Add Grade")
        print("5. View Student Transcript")
        print("6. Rank Students by GPA")
        print("7. Search Students by Grade")
        print("8. List all courses")
        print("9. Save Data")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            num_students = int(input("Enter the number of students to add: "))
            for _ in range(num_students):
               email = input("Enter student email: ")
               first_name = input("Enter first name: ")
               last_name = input("Enter last name: ")
               student = Student(email, first_name, last_name)
               grade_book.add_student(student)
               print(f"Student {first_name} {last_name} added successfully.")
               print(f"{num_students} students added to the grade book.")

        elif choice == '2':
              name = input("Enter course name: ")
              trimester = input("Enter trimester: ")
              credits = int(input("Enter credits: "))
              course = Course(name, trimester, credits)
              grade_book.add_course(course)
              print("Course added successfully.")

        elif choice == '3':
              email = input("Enter student email: ")
              course_name = input("Enter course name: ")
              if grade_book.register_student_for_course(email, course_name):
                print("Student registered for course successfully.")

        elif choice == '4':
              email = input("Enter student email: ")
              course_name = input("Enter course name: ")
              grade = float(input("Enter grade: "))
              if grade_book.add_grade_to_student(email, course_name, grade):
                print("Grade added successfully.")
        
        elif choice == '5':
            number_of_students = int(input("Enter the number of students to generate their transcripts: "))
            # put all emails together
            emails = []
            for i in range(number_of_students):
                       email = input(f"Enter student email {i+1}: ")
                       emails.append(email)

            # create  transcripts for all students
            for i, email in enumerate(emails):
                student = grade_book.get_student_by_email(email)
                if student:
                    print(f"Transcript for student {i}:\n{student.generate_transcript()}")

        elif choice == '6':
              ranked_students = grade_book.rank_students_by_gpa()
              for i, student in enumerate(ranked_students, 1):
                print(f"{i}. {student.first_name} {student.last_name} - GPA: {student.gpa:.2f}")

        elif choice == '7':
          course_name = input("Enter course name: ")
          grade = float(input("Enter grade to search for: "))
          students = grade_book.search_students_by_grade(course_name, grade)
          for student in students:
                 print(f"{student.first_name} {student.last_name} - {student.email}")

        elif choice == '8':
          grade_book.list_all_courses()
        
        elif choice == '9':
         grade_book.save_data()
         

        elif choice == '10':
         print("Thank you for using the Grade Book Application. Goodbye!")
         break

        else:
         print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()