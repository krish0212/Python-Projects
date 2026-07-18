from abc import ABC, abstractmethod
class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def get_role(self):
        pass

class Student(Person):
    def __init__(self, name, age, student_id, grade):
        super().__init__(name, age) 
        self.student_id = student_id
        
        self.__gpa = 0.0 
        self.grade = grade

    def get_gpa(self):
        return self.__gpa

    def set_gpa(self, new_gpa):
        if 0.0 <= new_gpa <= 4.0:
            self.__gpa = new_gpa
        else:
            print(" Invalid GPA! Must be between 0.0 and 4.0")

    def get_role(self):
        return "Student"

def print_person_profile(person_object):
    print(f"Profile -> Name: {person_object.name} | Role: {person_object.get_role()}")

class StudentManagementSystem:
    def __init__(self):
        self.students = {}

    def add_student(self):
        print("\n--- Register Student ---")
        student_id = input("Enter Student ID: ").strip()
        if student_id in self.students:
            print(" Student ID already exists!")
            return

        name = input("Enter Name: ").strip()
        try:
            age = int(input("Enter Age: "))
            grade = input("Enter Grade: ").strip()
            gpa = float(input("Enter starting GPA (0.0 - 4.0): "))
        except ValueError:
            print(" Invalid input data types. Try again.")
            return

        new_student = Student(name, age, student_id, grade)
        new_student.set_gpa(gpa)  
        
        self.students[student_id] = new_student
        print(f"{new_student.name} registered successfully!")

    def show_all_profiles(self):
        print("\n--- Student Profiles ---")
        if not self.students:
            print("No student records found.")

        for student in self.students.values():
            print_person_profile(student)
            print(f"   Details: ID {student.student_id}, Grade {student.grade}, GPA: {student.get_gpa()}")

def main():
    sms = StudentManagementSystem()
    
    while True:
        print("\n==============================")
        print("  STUDENT MANAGEMENT SYSTEM  ")
        print("==============================")
        print("1. Add Student Details")
        print("2. View All System Roles ")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            sms.add_student()
        elif choice == '2':
            sms.show_all_profiles()
        elif choice == '3':
            print("Thank you for using the Student Management System.")
            break
        else:
            print(" Invalid choice.")

if __name__ == "__main__":
    main()