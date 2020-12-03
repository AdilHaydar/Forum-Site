from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
# Create your models here.

def upload_to(instance,filename):
    return '%s/%s/%s'%('users_avatar',instance.email,filename)

def validate_email(value):
    if not '@' in value:
        raise ValidationError(_('%(value)s is not an invalid mail address'), params={'value':value})

def validate_username(value):
    if len(value) < 6:
        raise ValidationError(_("%(value)s is can't be less than 6 characters."), params={'value':value})


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        
        user.username = username
        user.set_password(password) 
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, password=None, **extra_fields):
        email = input('Email: ')

        perm = UserPermission()
        perm.permission = 'Admin'

        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email)
        )
        
        user.username = username
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        perm.user = user
        perm.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length = 15, validators=[validate_username], unique=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name = 'Email Address', validators=[validate_email], max_length=255)
    is_banned = models.BooleanField(default=False, verbose_name = 'Banned')
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)
    active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default = 0, verbose_name = 'Comment Count', blank=False, null=False)
    topic_count = models.IntegerField(default = 0, verbose_name = 'Topic Count', blank=False, null=False)

    


    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "User"

    def save(self, *args, **kwargs):

        super(User, self).save(*args,**kwargs)

        
        uis = UserPermission.objects.filter(user = self.id)
        if len(uis) == 0:
            perm = UserPermission()
            perm.permission = ''
            perm.user = self
            perm.save()
            
    @property
    def get_image_or_default(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/media/def_image/default-user-image.png'

    def __str__(self):
        return self.username

    def get_short_name(self):
        pass

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
       return self.admin

    def has_module_perms(self, app_label):
       return self.admin


class UserUpdateModel(models.Model):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name = "Email",
    )
    
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)


permissions = (
    ('Admin', 'Administrator'),
    ('Co-Admin','Co-Administrator'),
    ('Site Police', 'Site Police'),
    ('Super Mod', 'Super Moderator'),
    ('Mod', 'Moderator'),
    ('VIP','VIP'),
    ('Banned','Banned')
)

class UserPermission(models.Model):
    user = models.OneToOneField('user.User', on_delete = models.CASCADE)
    permission = models.CharField(max_length = 20, choices = permissions, verbose_name = 'Permissions')

    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        super(UserPermission,self).save(*args,**kwargs)
        if self.permission == 'Admin':
            self.user.admin = True
            self.user.staff = True
        elif self.permission == 'Banned':
            self.user.admin = False
            self.user.staff = False
            self.user.active = False
            self.user.is_banned = True
        elif self.permission == '':
            self.user.admin = False
            self.user.staff = False
            self.user.active = True
            self.user.is_banned = False
        else:
            self.user.staff = True
            self.user.admin = False
            self.user.is_banned = False
            self.user.active = True
        self.user.save()

    @property
    def get_icon(self):
        if self.permission:
            return '/media/perm_icon/'+self.permission+'.png'
        else:
            return '/media/perm_icon/user.png'

    @property
    def get_color(self):
        if self.permission == 'Admin':
            return 'red'
        elif self.permission == 'Co-Admin':
            return 'blue'
        elif self.permission == 'Site Police':
            return 'purple'
        elif self.permission == 'Super Mod':
            return 'orange'
        elif self.permission == 'Mod':
            return 'green'
        elif self.permission == 'VIP':
            return 'lightblue'
        elif self.permission == 'Banned':
            return 'black'
        else:
            return 'black'
    