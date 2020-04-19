import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Advisory.settings')

import django
django.setup()

from Advisor.models import teachers, department, students, Class
from faker import Faker

fakegen = Faker()
import random
import MySQLdb
import csv


def student(N):
    lis = ['M', "F"]
    ty = ['A', 'B', 'O', 'AB']
    sig = ['+', '-']
    liv = ['DAY SCHOLAR', 'HOSTELLER']
    for _ in range(N):
        mark = [1, 2]
        if (random.choice(mark) == 1):
            mark12 = random.uniform(34.00, 99.00)
            mark10 = 0
        else:
            mark10 = random.uniform(34.00, 99.00)
            mark12 = 0
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
            PAddress=fakegen.address(),
            PCity=fakegen.city(),
            PState=fakegen.state(),
            PDistrict=fakegen.city(),
            PPincode=random.randint(100000, 999999),
            CAddress=fakegen.address(),
            CCity=fakegen.city(),
            CState=fakegen.state(),
            CDistrict=fakegen.city(),
            CPincode=random.randint(100000, 999999),
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


def pin():
    mydb = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",
        database="advisory"
    )

    mycursor = mydb.cursor()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sql = "INSERT INTO advisor_pincodes (Pincode, District, State) VALUES (%s, %s, %s)"
    line_count = 0
    with open(os.path.join(BASE_DIR,  'Advisory\\pincodes.csv'), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        print('Adding pincode data, Please wait .....')
        for row in csv_reader:
            if line_count == 0:
                print(", ".join(row))
                line_count += 1
            else:
                val = (row[0], row[1], row[2])
                mycursor.execute(sql, val)
                line_count += 1
        print(line_count)

    mydb.commit()

    print(line_count, " record inserted.")


if __name__ == '__main__':

    print('Populating Table Data....')
    student(25)
    # teacher(100)
    print('Done')
    pin()
