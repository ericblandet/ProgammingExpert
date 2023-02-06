import os
import json


NUM_STUDENTS = 1000
SUBJECTS = ["math", "science", "history", "english", "geography"]


def load_report_card(directory, student_number):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, f"{student_number}.json")
    path = os.path.join(base_path, file_path)

    try:
        with open(path, "r") as file:
            report_card = json.load(file)
    except FileNotFoundError:
        return {}

    return report_card


def compute_student_avg_grade(card):
    _sum = 0
    for subject in SUBJECTS:
        _sum += card[subject]
    return _sum / len(SUBJECTS)


def compute_grades(grades):
    best_grade = (None, 0)
    worst_grade = (0, 100)
    for k, v in grades.items():

        if v['avg'] > best_grade[1]:
            best_grade = (k, v['avg'])
        if v['avg'] < worst_grade[1]:
            worst_grade = (k, v['avg'])

    return best_grade, worst_grade


studs_avg = (0, 0)
best_student = (None, 0)
worst_student = (None, 100)
avg_per_grades = {}
avg_per_subject = {}

for i in range(0, NUM_STUDENTS):
    card = load_report_card("students", i)
    if card == {}:
        print(f"Card {i} seems corrupted.")
        continue

    stud_avg = compute_student_avg_grade(card)
    card['average'] = stud_avg

    studs_avg = studs_avg[0] + stud_avg, studs_avg[1] + 1

    if stud_avg > best_student[1]:
        best_student = (card['id'], stud_avg)
    if stud_avg < worst_student[1]:
        worst_student = (card['id'], stud_avg)

    if avg_per_grades.get(card['grade']) is None:
        avg_per_grades[card['grade']] = {
            'sum': stud_avg, 'len': 1, 'avg': stud_avg}
    else:
        avg_per_grades[card['grade']]['sum'] += stud_avg
        avg_per_grades[card['grade']]['len'] += 1
        avg_per_grades[card['grade']]['avg'] = avg_per_grades[card['grade']
                                                              ]['sum'] / avg_per_grades[card['grade']]['len']

    for subject in SUBJECTS:
        if avg_per_subject.get(subject) is None:
            avg_per_subject[subject] = {
                'sum': stud_avg, 'len': 1, 'avg': card[subject]}
        else:
            avg_per_subject[subject]['sum'] += card[subject]
            avg_per_subject[subject]['len'] += 1
            avg_per_subject[subject]['avg'] = avg_per_subject[subject
                                                              ]['sum'] / avg_per_subject[subject]['len']

overall_avg = round(studs_avg[0]/studs_avg[1], 2)
best_grade, worst_grade = compute_grades(avg_per_grades)
easiest_subject, hardest_subject = compute_grades(avg_per_subject)
print("Average Student Grade: ", overall_avg)
print("Hardest subject: ", hardest_subject[0])
print("Easiest subject: ", easiest_subject[0])
print("Best performing grade: ", best_grade[0])
print("Worst performing grade: ", worst_grade[0])
print("Best student ID: ", best_student[0])
print("Worst student ID: ", worst_student[0])
