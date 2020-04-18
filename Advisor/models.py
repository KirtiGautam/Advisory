from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    HOD = models.CharField(max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class teachers(models.Model):
    full_name = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=255)
    contact = models.CharField(max_length=50)
    department = models.ForeignKey(department, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Class(models.Model):
    section = models.CharField(max_length=4)
    batch = models.PositiveIntegerField()
    department = models.ForeignKey(department, on_delete=models.CASCADE)
    Mentor = models.ForeignKey(teachers, on_delete=models.CASCADE)

    def __str__(self):
        send = self.section + self.batch
        return send


class students(models.Model):
    urn = models.PositiveIntegerField(primary_key=True)
    crn = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='students', default=None, null=True)
    full_name = models.CharField(max_length=255)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    blood_group = models.CharField(max_length=4)
    category = models.CharField(max_length=255)
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    living_choices = (
        ('DAY SCHOLAR', 'DAY SCHOLAR'),
        ('HOSTELLER', 'HOSTELLER'),
    )
    living = models.CharField(choices=living_choices, max_length=12)
    X_marks = models.DecimalField(max_digits=4, decimal_places=2)
    XII_marks = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    diploma_marks = models.DecimalField(
        default=0, max_digits=4, decimal_places=2)
    Father_pic = models.ImageField(upload_to='father', default=None, null=True)
    Father_name = models.CharField(max_length=255)
    Father_contact = models.CharField(max_length=15)
    Mother_pic = models.ImageField(upload_to='mother', default=None, null=True)
    Mother_name = models.CharField(max_length=255)
    Mother_contact = models.CharField(max_length=15)
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    Pincode = models.PositiveIntegerField()
    Contact = models.CharField(max_length=15)
    email = models.EmailField()
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Subjects(models.Model):
    sub_code = models.CharField(max_length=255, primary_key=True)
    Name = models.CharField(max_length=255)
    credits = models.PositiveIntegerField()
    department = models.ForeignKey(department, on_delete=models.CASCADE)


class detailed_Marks(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    Sgpa = models.DecimalField(
        default=0.0, max_digits=3, decimal_places=2)
    passive_back = models.BooleanField(default=False)
    exam_date = models.DateField(default=None, null=True, blank=True)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, teacher=None, is_admin=False, is_superuser=False):
        if not username:
            raise ValueError('User must have a username')
        if not password:
            raise ValueError('User must have a password')
        user_obj = self.model(username=username)
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.is_superuser = is_superuser
        user_obj.teacher = teacher
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, password=None, teacher=None):
        user = self.create_user(username,
                                password,
                                teacher=teacher,
                                is_superuser=True)
        return user

    def create_admin(self, username, password=None, teacher=None):
        user = self.create_user(username,
                                password,
                                teacher=teacher,
                                is_admin=True)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to='teachers', default=None, null=True)
    teacher = models.OneToOneField(
        teachers,  on_delete=models.CASCADE, default=None, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        permissions = [
            ('can_upload_students', 'Can upload student data'),
            ('can_assign_mentors', 'Can assign mentors to class'),
        ]

    def __str__(self):
        return str(self.teacher)


class Pincodes(models.Model):
    Pincode =  models.PositiveIntegerField(primary_key=True)
    District = models.CharField(max_length=255)
    State = models.CharField(max_length=255)