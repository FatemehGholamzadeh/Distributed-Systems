import os
import sys
import subprocess
import shlex
import time
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turingoj.settings")

import django
django.setup()

from django.shortcuts import get_object_or_404
from submissions.models import SubmissionCache, MainSubmission, Leaderboard, lang_extensions
from problems.models import Problem
from coders.models import UserProfile

DEFAULT_UID = 1000      # Set these both according to needs
DEFAULT_GID = 1000
ROOT_UID = 0
ROOT_GID = 0

TIME_QUANTUM = 0.01      # Update for more granular control over Execution Time

CHROOTPATH = "C:/Users/SG/PycharmProjects/jail"
JUDGEDIR = CHROOTPATH + '/judgedir'
JUDGE_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

# global vars
cpl_solution_path = JUDGE_SCRIPT_PATH + '/ven/curr_solution'

SCORE_UPDATED = False                   # To void Leaderboard updation


# def backToHostRoot():
#     os.fchdir(HOST_ROOT)
#     os.chroot(".")
#     os.chdir(JUDGE_SCRIPT_PATH)


def cleanFiles(problem_directory):
    subprocess.call(['rm', '-rf', JUDGEDIR + '/*'])           # BE VERY CAUTIOUS!! REMOVING TEMPORARY FILES
    subprocess.call(['cp', '-r', problem_directory + '/input', JUDGEDIR + '/'])
    subprocess.call(['cp', '-r', problem_directory + '/output', JUDGEDIR + '/'])
    subprocess.call(['cp', cpl_solution_path, JUDGEDIR + '/'])
    subprocess.call(['rm', cpl_solution_path])


def runCpp(csubmission):
    retStatus = 0                                   # 0 for accepted, 1 WA, 2 NZEC, 3 TLE
    mxTime = 0
    verdict = "Accepted"
    corr_problem = csubmission.problem_submitted
    problem_directory = os.path.dirname(corr_problem.test_file.path)
    tot_files = subprocess.Popen(['ls', '-1', problem_directory + '/input'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)  # Find total number of test cases
    tot_files.wait()
    stdout = tot_files.communicate()[0]
    total = stdout.decode('utf-8').count('\n')
    # os.setgid(ROOT_GID)
    # os.setuid(ROOT_UID)  # root
    # cleanFiles(problem_directory)
    # os.chroot(CHROOTPATH)
    executablePath = '/judgedir/curr_solution'
    for i in range(0, total):
        testCaseNo = i + 1
        print("Running Test Case " + str(testCaseNo))
        currID = ""
        if i <= 9:
            currID = '0' + str(i)
        else:
            currID = str(i)
        curr_input_file = open('/judgedir/input/input' + currID + '.txt')
        execFilePath = '/judgedir/expout.txt'
        exec_output_file = open(execFilePath, 'w')
        currProc = subprocess.Popen([executablePath], stdin=curr_input_file, stdout=exec_output_file)
        currTime = 0
        TL = corr_problem.time_limit
        while currTime < TL:
            time.sleep(TIME_QUANTUM)
            currTime += TIME_QUANTUM
            mxTime = max(mxTime, currTime)
            if currProc.poll() is not None:
                break
        exec_output_file.close()
        curr_input_file.close()
        if currProc.poll() is None:
            currProc.kill()
            retStatus = 3
            verdict = "TLE on test case {}".format(testCaseNo)
            return retStatus, currTime, verdict

        if currProc.returncode != 0:
            retStatus = 2
            verdict = "NZEC on test case {}".format(testCaseNo)
            return retStatus, currTime, verdict

        outputFilePath = '/judgedir/output/output' + currID + '.txt'
        diffFile = open('/judgedir/differences.txt', 'w')
        currProc = subprocess.Popen(['diff', '-Z', outputFilePath, execFilePath], stdout=diffFile)
        currProc.wait()
        diffFile.close()
        diffFile = open('/judgedir/differences.txt', 'r')
        if len(diffFile.read()) != 0:
            retStatus = 1
            verdict = "WA on test case {}".format(testCaseNo)
            return retStatus, currTime, verdict
    return retStatus, mxTime, verdict


def compileCpp(csubmission):
    src_file = open(csubmission.solution.path, 'r')
    solution_path = JUDGE_SCRIPT_PATH + '/ven'
    new_src_file_path = solution_path + '/curr_solution.' + lang_extensions[csubmission.language]
    solution_file = open(new_src_file_path, 'w')
    solution_file.write(src_file.read())
    src_file.close()
    solution_file.close()
    cpl_src = subprocess.Popen(['g++', '-w', '-std=c++14', new_src_file_path,
                                '-o', solution_path + '/curr_solution'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cpl_src.wait()
    stdout, stderr = cpl_src.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if stderr != "":
        return False
    return True


def updateScore(csubmission):
    global SCORE_UPDATED
    SCORE_UPDATED = False
    if (MainSubmission.objects.filter(user_handle=csubmission.user_handle, problem_submitted=csubmission.problem_submitted, verdict="Accepted").count() == 0):
        csubmission.user_handle.score += csubmission.problem_submitted.score
        print('Score Updated:\nUser: {}\nScore: {}'.format(csubmission.user_handle, csubmission.user_handle.score))
        SCORE_UPDATED = True


def updateLeaderBoard():
    print('Updating Leaderboard')
    allUsers = UserProfile.objects.all().order_by('-score')
    Leaderboard.objects.all().delete()
    currRank = 1
    prevScore = allUsers[0].score
    sameRank = 0
    for user in allUsers:
        if(prevScore != user.score):
            currRank += sameRank
            prevScore = user.score
            sameRank = 1
        else:
            sameRank += 1
        new_entry = Leaderboard.objects.create(user_handle=user, rank=currRank)
        new_entry.save()


def evaluate(csubmission):
    verdict = ""
    executionTime = 0
    memory = 0
    retStatus = 4
    if compileCpp(csubmission) == False:
        verdict = "Compilation Error"
    else:
        retStatus, executionTime, verdict = runCpp(csubmission)
    print('Status - {}\nETime - {}\nVerdict - {}'.format(retStatus, executionTime, verdict))
    time.sleep(0.01)
    submission_main = get_object_or_404(MainSubmission, id=csubmission.sidno)
    if retStatus == 0:
        updateScore(csubmission)
    csubmission.user_handle.save()
    submission_main.verdict = verdict
    submission_main.execution_time = executionTime
    submission_main.save()
    csubmission.judged = 'yes'
    csubmission.save()
    # backToHostRoot()


def judgement(threadID,numberOfThreads):
    print('Judge Running...')
    while True:
        # HOST_ROOT = os.open("C:/Users/SG/PycharmProjects", os.O_RDONLY)
        # HOST_ROOT = os.open("C:/Users/SG/PycharmProjects",)
        if 'leaderboard' in sys.argv:
            updateLeaderBoard()
            sys.exit(0)
        if len(sys.argv) > 1:
            cache_submissions = SubmissionCache.objects.filter(sidno__range=(int(sys.argv[1]), int(sys.argv[2])))
        else:
            cache_submissions = SubmissionCache.objects.filter(judged__iexact='no').order_by('id')
        for csubmission in cache_submissions:
            if(threadID % numberOfThreads == csubmission.id %numberOfThreads):
                print("ID of thread : ")
                print(threadID)
                print("@@@@@@@@@@@@@@@@@@@@@")
                print('Judging cache submission - {}\nMain - {}\nProblem - {}'.format(csubmission.id, csubmission.sidno,
                                                                                      csubmission.problem_submitted.slug))
                evaluate(csubmission)
                updateLeaderBoard()
                SCORE_UPDATED = False
                # print("##########################")

        # if SCORE_UPDATED:
        #     updateLeaderBoard()
        #     SCORE_UPDATED = False
        # os.close(HOST_ROOT)
        if len(sys.argv) > 1:
            sys.exit(0)
        time.sleep(2.0)
