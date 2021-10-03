import os
import os
import sys
import subprocess
import shlex
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turingoj.settings")

import django
django.setup()

from django.shortcuts import get_object_or_404
from submissions.models import SubmissionCache, MainSubmission, Leaderboard, lang_extensions
from problems.models import Problem
from coders.models import UserProfile
import django
django.setup()
from submissions.models import SubmissionCache

while True:
    cache_submissions = SubmissionCache.objects.filter(judged__iexact='no').order_by('id')
    container_nums = int(len(cache_submissions) / 3) + 1
    id_list = []
    for csubmission in cache_submissions:
        id_list.append(csubmission.id)
    for id in id_list:
        f = open("C:/Users/SG/PycharmProjects/turingoj/turingoj/private_media/submissions/cache/" + str(
            id % container_nums) + ".txt", "a")
        f.write(str(id) + "$")
        f.close()
    for i in range(container_nums):
        os.system('docker run -it --name myapp' + str(
            i) + ' -v C:/Users/SG/PycharmProjects/turingoj/turingoj/private_media/submissions/cache:/judgebyte/turingoj/private_media/submissions/cache --env containerID=' + str(
            i) + ' turingoj_web')
    # time.sleep(2)
    for i in range(container_nums):
        os.system('docker rm myapp' + str(i))
    for i in range(container_nums):
        f = open("C:/Users/SG/PycharmProjects/turingoj/turingoj/private_media/submissions/cache/" + str(
            i) + ".txt", 'r+')
        f.truncate(0)

