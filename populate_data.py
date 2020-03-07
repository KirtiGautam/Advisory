import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Advisory.settings')

import django
django.setup()

from Advisor.models import teachers, department

from faker import Faker

import random

fakegen = Faker()
lis = ['M', "F"]


def populate(N):
    for entry in range(N):
        name = fakegen.name()
        email = fakegen.email()
        contact = fakegen.random_number(10)
        gender = random.choice(lis)
        ids = random.randint(1,4)
        teach = teachers.objects.create(full_name=name,
                                        gender=gender,
                                        email=email,
                                        contact=contact,
                                        department=department.objects.get(id=ids))
        teach.save()


if __name__ == '__main__':
    print('Populating Data....')
    populate(25)
    print('Done')
