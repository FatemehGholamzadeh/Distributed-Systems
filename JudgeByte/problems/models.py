from django.db import models
from coders.models import UserProfile
from django.utils.text import slugify
from django.urls import reverse
from private_storage.fields import PrivateFileField


def user_directory_path(instance, filename):
    return 'problems/problem_{}/{}'.format(instance.slug, filename)

DEFAULT_SETTER_ID = 1
DEFAULT_TIME_LIMIT = 1
DEFAULT_MEM_LIMIT = 512
DEFAULT_SRC_CODE_SZ = 50000
DEFAULT_BASE_FILE_SIZE = 1024**2

class Problem(models.Model):
    problem_name = models.CharField(max_length = 1000, unique = True)
    slug = models.SlugField(unique=True)
    problem_statement = models.TextField()
    setter = models.ForeignKey(UserProfile, default = DEFAULT_SETTER_ID, on_delete=models.SET_DEFAULT)
    score = models.PositiveIntegerField(blank=True, null=True, default = 100)
    time_limit = models.PositiveIntegerField(default = DEFAULT_TIME_LIMIT)
    memory_limit = models.PositiveIntegerField(default = DEFAULT_MEM_LIMIT)
    src_code_size = models.PositiveIntegerField(default = DEFAULT_SRC_CODE_SZ)
    solution_file = PrivateFileField(upload_to = user_directory_path, max_file_size = DEFAULT_SRC_CODE_SZ)
    test_file = PrivateFileField(upload_to = user_directory_path, max_file_size = DEFAULT_BASE_FILE_SIZE*30)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.problem_name)
        super(Problem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('problems:problem_page', kwargs={'slug':self.slug})

    def __str__(self):
        return self.problem_name
