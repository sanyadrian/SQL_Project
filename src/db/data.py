import random
import string


COURSES = {
    'Aviation': 'description Aviation',
    'Art': 'description Art',
    'Chemistry': 'description Chemistry',
    'Economics': 'description Economics',
    'Engineering': 'description Engineering',
    'Journalism': 'description Journalism',
    'Music': 'description Music',
    'Geography' : 'description Geography',
    'Maths': 'description Maths',
    'Computer Science' : 'description Computer Science',
}

FIRST_NAMES = [
    'Noel',
    'Joel',
    'Mateo',
    'Ergi',
    'Luis',
    'Anna',
    'Hannah',
    'Sophia',
    'Emma',
    'Marie',
    'Sam',
    'David',
    'Max',
    'Alice',
    'Maria',
    'Bob',
    'George',
    'Marina',
    'Alex',
    'Jason',
]

LAST_NAMES = [
    'Collymore',
    'Stoll',
    'Verlice',
    'Adler',
    'Huxley',
    'Ledger',
    'Hayes',
    'Ford',
    'Finnegan',
    'Beckett',
    'Phillips',
    'Rogers',
    'Hetfield',
    'Fafara',
    'Friden',
    'Stanne',
    'Hammet',
    'Sweigart',
    'Rhinehart',
    'Dickens',
]


def data_creator_students(first_name: list, last_name: list, n: int = 200) -> list:
    students = []
    for i in range(n+1):
        f_index = random.randint(0, len(first_name)-1)
        l_index = random.randint(0, len(last_name)-1)
        students.append((first_name[f_index], last_name[l_index]))
    return students


def data_creator_groups(n: int = 10):
    groups = {}
    while len(groups) < n:
        group_name = (random.choice(string.ascii_letters).upper() +
                      random.choice(string.ascii_letters).upper() +
                      '-' + str(random.randint(10, 99)))
        if group_name not in groups:
            groups[group_name] = []
    return groups


def generate_group_id(groups):
    group_id = random.randint(1, 10)
    count_of_existing_students = groups.get(group_id, 0)
    if not count_of_existing_students:
        groups[group_id] = 0
    if count_of_existing_students > 30:
        group_id = generate_group_id(groups)
    groups[group_id] += 1
    return group_id


def assign_students_to_groups(students, groups_id):
    for student in students:
        least_populated_groups = sorted([name for name in groups_id], key=lambda name: len(groups_id[name]))
        weights = [30 - len(groups_id[name]) for name in least_populated_groups]
        group = random.choice(random.choices(least_populated_groups, weights=weights, k=3))
        if len(groups_id[group]) < 30:
            groups_id[group].append(student)
    return groups_id



def assign_students_to_courses():
    return random.sample(range(1, 11), random.randrange(1, 4))

