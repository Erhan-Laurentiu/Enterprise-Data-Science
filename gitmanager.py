import subprocess
import os
import git
from paths import GIT_PULL, REPO_LOCAL_FILE_PATH

# REPO_LOCAL_FILE_PATH = './data/raw/covid-19-data/'

def get_data_from_github():
    ''' Get data by a git pull request, the source code has to be pulled first
        Result is stored in the predifined csv structure
    '''
    git_pull = subprocess.Popen(GIT_PULL ,
                         cwd = os.path.dirname(REPO_LOCAL_FILE_PATH[2:] ),
                         shell = True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE )
    (out, error) = git_pull.communicate()

    print("Error : " + str(error))
    print("out : " + str(out))

def getDataFromGithub():
    repoPath = git.Repo(REPO_LOCAL_FILE_PATH[2:])
    print("GitManager: Pulling Repository")
    repoPath.remotes.origin.pull()
    print("GitManager: Pulling Repository Finished")

# get_data_from_github()
