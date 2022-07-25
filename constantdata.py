GIT_PULL = '/usr/bin/git pull'
REPO_LOCAL_FILE_PATH = './data/raw/covid-19-data/' #raw file path
PROCESSED_DATA_FILE_PATH = './data/processed/'

POPULATION_RAW_FILE_PATH   = REPO_LOCAL_FILE_PATH + 'scripts/input/un/population_latest.csv'
VACCINATION_RAW_FILE_PATH  = REPO_LOCAL_FILE_PATH + 'public/data/vaccinations/vaccinations.csv' 
CASES_DEATHS_RAW_FILE_PATH = REPO_LOCAL_FILE_PATH + 'public/data/jhu/full_data.csv'

PROCESSED_RELATIONAL_INTERMEDIARY_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'COVID_relational_intermediary.csv'
PROCESSED_RELATIONAL_FINAL_FILE_PATH        = PROCESSED_DATA_FILE_PATH + 'COVID_final_data_set.csv'

SIR_INTERMEDIARY_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'SIR_intermediary.csv'
SIR_FINAL_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'SIR_final.csv'

DEFAULT_COUNTRIES_LIST = ["Germany","Portugal","Italy"]

STATE_KEY = 'state'
COUNTRY_KEY = 'country'
DATE_KEY = 'date'
CASES_KEY = 'confirmed'
CASES_POP_KEY = 'confirmed_per_pop'
CASES_FILTERED_KEY = 'confirmed_filtered'
CASES_DR_KEY = 'confirmed_DR'
CASES_FILTERED_DR_KEY = 'confirmed_filtered_DR'
DEATHS_KEY = 'total_deaths'
DEATHS_POP_KEY = 'total_deaths_per_pop'
FULLY_VACCINATED_KEY = 'people_fully_vaccinated'
FULLY_VACCINATED_POP_KEY = 'total_fully_vaccinated_per_pop'