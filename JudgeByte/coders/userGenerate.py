import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from coders.models import UserProfile,AbstractUser

def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_'+str(i+10)
        name = 'name_'+str(i+10)
        email = '{}@example.com'.format(username)
        password = "mitra1341"
        new_user = User.objects.create(username=username, email=email, password=password,name=name)
        new_user.save()
        p = UserProfile.objects.create(user=new_user)
        p.save()
    # return '{} random users created with success!'.format(total)

# create_random_user_accounts(2)
