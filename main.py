from dataprocessmanager import processAllData
from gitmanager import get_data_from_github, getDataFromGithub
from uimanager import startApp

getDataFromGithub()
processAllData()
startApp()
