GIT_PULL = '/usr/bin/git pull'
REPO_LOCAL_FILE_PATH = './data/raw/covid-19-data/' #raw file path
PROCESSED_DATA_FILE_PATH = './data/processed/'

POPULATION_RAW_FILE_PATH   = REPO_LOCAL_FILE_PATH + 'scripts/input/un/population_latest.csv'
VACCINATION_RAW_FILE_PATH  = REPO_LOCAL_FILE_PATH + 'public/data/vaccinations/vaccinations.csv' 
CASES_DEATHS_RAW_FILE_PATH = REPO_LOCAL_FILE_PATH + 'public/data/jhu/full_data.csv'

PROCESSED_RELATIONAL_INTERMEDIARY = PROCESSED_DATA_FILE_PATH + 'COVID_relational_intermediary.csv'
PROCESSED_RELATIONAL_FINAL        = PROCESSED_DATA_FILE_PATH + 'COVID_final_data_set.csv'

DEFAULT_COUNTRIES_LIST = ["Germany","France","Italy"]