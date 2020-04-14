import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Advisory.settings')

import django
django.setup()

from Advisor.models import teachers, department, students, Class
from faker import Faker

fakegen = Faker()
import random


def student(N):
    lis = ['M', "F"]
    ty = ['A', 'B', 'O', 'AB']
    sig = ['+', '-']
    liv = ['DAY SCHOLAR', 'HOSTELLER']
    for _ in range(N):
        mark = [1,2]
        if (random.choice(mark)==1):
            mark12=random.uniform(34.00, 99.00)
            mark10=0
        else:
            mark10=random.uniform(34.00, 99.00)
            mark12=0
        print([mark10, mark12])
        stu = students.objects.create(
            urn=random.randint(1000000, 2000000),
            crn=random.randint(1000000, 2000000),
            full_name=fakegen.name(),
            gender=random.choice(lis),
            blood_group=(random.choice(ty) + random.choice(sig)),
            category='General',
            height=random.uniform(5.0, 6.11),
            weight=random.uniform(40.0, 90.0),
            dob=fakegen.date_of_birth(),
            X_marks=random.uniform(34.00, 99.00),
            XII_marks=mark12,
            diploma_marks=mark10,
            living=random.choice(liv),
            Father_name=fakegen.name(),
            Father_contact=random.randint(1000000000, 99999999999),
            Mother_name=fakegen.name(),
            Mother_contact=random.randint(1000000000, 99999999999),
            Address=fakegen.address(),
            City=fakegen.city(),
            State=fakegen.state(),
            District=fakegen.city(),
            Pincode=random.randint(100000, 999999),
            Contact=random.randint(1000000000, 99999999999),
            email=fakegen.email(),
            Class=Class.objects.get(id=1))
        stu.save()


def teacher(N):
    lis = ['M', "F"]
    for _ in range(N):
        name = fakegen.name()
        email = fakegen.email()
        contact = fakegen.random_number(10)
        gender = random.choice(lis)
        ids = random.randint(1, 4)
        teach = teachers.objects.create(full_name=name,
                                        gender=gender,
                                        email=email,
                                        contact=contact,
                                        department=department.objects.get(id=ids))
        teach.save()


if __name__ == '__main__':

    print('Populating Data....')
    student(25)
    # teacher(100)
    print('Done')
