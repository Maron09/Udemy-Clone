from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField



class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("Email Address Required")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            password= password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
        TEACHER = 1
        STUDENT = 2
        
        ROLE_CHIOCE =(
            (TEACHER, 'Teacher'),
            (STUDENT, 'Student')
        )
        
        
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.EmailField(max_length=100, unique=True)
        role = models.PositiveSmallIntegerField(choices=ROLE_CHIOCE, blank=True, null=True)
        
        date_joined = models.DateTimeField(auto_now_add=True)
        last_login = models.DateTimeField(auto_now_add=True)
        create_date = models.DateTimeField(auto_now=True)
        modified_date = models.DateTimeField(auto_now=True)
        is_active = models.BooleanField(default=False)
        is_admin = models.BooleanField(default=False)
        is_staff = models.BooleanField(default=False)
        is_superadmin = models.BooleanField(default=False)
        
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['first_name', 'last_name']
        
        objects = UserManager()
        
        
        def __str__(self):
            return self.email
        
        def has_perm(self, perm, obj=None):
            return self.is_admin
        
        def has_module_perms(self, app_label):
            return True
        
        def get_role(self):
            if self.role == 1:
                user_role = 'Teacher'
            elif self.role == 2:
                user_role = 'Student'
            return user_role


class UserPofile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email