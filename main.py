from dataprocessmanager import processAllData
from gitmanager import getDataFromGithub
from uimanager import startApp

getDataFromGithub()
processAllData()
startApp()
