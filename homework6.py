class Student:
    students_list = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.students_list.append(self)

    def rate_lecturer(self, course, lecturer, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and lecturer.courses_attached and grade in range(
            1, 11):
            if course in lecturer.lecturer_grades:
                lecturer.lecturer_grades[course] += [grade]
            else:
                lecturer.lecturer_grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        sum_grades = 0
        for grade_list in self.grades.values():
            for grade in grade_list:
                sum_grades += grade
        av_grade = sum_grades / len(self.grades.values())
        return av_grade

    def __str__(self):
        return f'\nИмя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за домашние задания: {self.average_grade()} \nКурсы в процессе обучения: {", ".join(self.courses_in_progress)} \nЗавершенные курсы: {", ".join(self.finished_courses)}'

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Not a Student!')
        return self.average_grade() < other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    lecturers_list = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lecturer_grades = {}
        Lecturer.lecturers_list.append(self)

    def average_grade(self):
        sum_grades = 0
        count = 0
        for grade_list in self.lecturer_grades.values():
            for grade in grade_list:
                    sum_grades += grade
                    count += 1
        av_grade = sum_grades/count
        return av_grade

    def __str__(self):
        return f'\nИмя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {self.average_grade()}'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a Lecturer!')
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'\nИмя: {self.name} \nФамилия: {self.surname} \n'


def av_grade_hw(course, students_list=Student.students_list):
    grade = 0
    count = 0
    for student in students_list:
        if course in student.courses_in_progress:
            count += 1
            for grade_in_list in student.grades[course]:
                grade += grade_in_list
    av_grade = grade / count
    print(av_grade)


def av_grade_lecture(course, lecturers_list=Lecturer.lecturers_list):
    grade = 0
    count = 0
    for lecturer in lecturers_list:
        if course in lecturer.courses_attached:
            for grade_in_list in lecturer.lecturer_grades[course]:
                count += 1
                grade += grade_in_list
    av_grade = grade / count
    print(av_grade)


best_student = Student('Slava', 'Orlov', 'male')
best_student.courses_in_progress += ['Python', 'C#', 'Information Security', 'Git']
best_student.finished_courses += ['Введение в программирование']

cool_student = Student('Lyubov', 'Orlova', 'female')
cool_student.courses_in_progress += ['Java', 'Python', 'C']
cool_student.finished_courses += ['Введение в программирование']

best_lecturer = Lecturer('Anton', 'Lebedev')
best_lecturer.courses_attached = ['Python', 'Information Security', 'Git']
best_student.rate_lecturer('Information Security', best_lecturer, 10)
best_student.rate_lecturer('Python', best_lecturer, 9)
best_student.rate_lecturer('Git', best_lecturer, 10)
cool_student.rate_lecturer('Python',best_lecturer,8)

cool_lecturer = Lecturer('Marina', 'Popova')
cool_lecturer.courses_attached = ['C#', 'Java', 'C']
cool_student.rate_lecturer('C', cool_lecturer, 9)
cool_student.rate_lecturer('Java', cool_lecturer, 9)
best_student.rate_lecturer('C#', cool_lecturer, 7)

best_reviewer = Reviewer('Oleg', 'Petrov')
best_reviewer.courses_attached = ['Python', 'C#', 'Information Security']
best_reviewer.rate_hw(best_student, 'Python', 10)
best_reviewer.rate_hw(best_student, 'C#', 9)
best_reviewer.rate_hw(best_student, 'Information Security', 10)
best_reviewer.rate_hw(cool_student, 'Python', 8)

cool_reviewer = Reviewer('Sergey', 'Serov')
cool_reviewer.courses_attached = ['C', 'Java', 'Git']
cool_reviewer.rate_hw(best_student, 'Git', 9)
cool_reviewer.rate_hw(cool_student, 'Java', 8)
cool_reviewer.rate_hw(cool_student, 'C', 8)

print(best_student)
print(cool_student)
print(best_lecturer)
print(cool_lecturer)
print(best_reviewer)
print(cool_reviewer)

print(f'Сравниваем лекторов best_lecturer и cool_lecturer (>): {best_lecturer > cool_lecturer}')
print(f'Сравниваем студентов best_student и cool_student (<): {best_student < cool_student}')

print('\nСредняя оценка за ДЗ по всем студентам по определенному курсу:')
av_grade_hw('Python')
print('\nСредняя оценка за лекции всех лекторов по определенному курсу: ')
av_grade_lecture('Python')