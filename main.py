from dataprocessmanager import processAllData
from gitmanager import get_data_from_github, getDataFromGithub
from paths import DEFAULT_COUNTRIES_LIST
from uimanager import startApp


getDataFromGithub()
processAllData(DEFAULT_COUNTRIES_LIST)
startApp()
