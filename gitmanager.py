import subprocess
import os
import git
from constantdata import GIT_PULL, REPO_LOCAL_FILE_PATH

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
    print("GitManager::getDataFromGithub: Pulling Repository")
    repoPath.remotes.origin.pull()
    print("GitManager::getDataFromGithub: Pulling Repository Finished")
