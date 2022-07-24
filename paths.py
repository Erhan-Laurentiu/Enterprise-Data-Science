GIT_PULL = '/usr/bin/git pull'
REPO_LOCAL_FILE_PATH = './data/raw/covid-19-data/' #raw file path
PROCESSED_DATA_FILE_PATH = './data/processed/'

POPULATION_RAW_FILE_PATH = REPO_LOCAL_FILE_PATH + 'scripts/input/un/population_latest.csv'
POPULATION_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'population_small_flat_table.csv'

VACCINATION_RAW_FILE_PATH = './data/raw/covid-19-data/public/data/vaccinations/vaccinations.csv' 

VACCINATION_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'vaccinated_flat_table.csv'
VACCINATION_POP_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'ui/vaccinated_pop_flat_table.csv'

CASES_DEATHS_RAW_FILE_PATH = './data/raw/covid-19-data/public/data/jhu/full_data.csv'

CASES_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'cases_flat_table.csv'
CASES_POP_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'ui/cases_pop_flat_table.csv'
CASES_INTERMEDIARY_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'cases_intermediary_flat_table.csv'
CASES_FILTERING_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'cases_filtering_flat_table.csv'
CASES_FILTERED_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'ui/cases_filtered_flat_table.csv'
CASES_DR_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'ui/cases_dr_flat_table.csv'
CASES_FILTERED_DR_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'ui/cases_filtered_dr_flat_table.csv'

DEATHS_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'deaths_flat_table.csv'
DEATHS_POP_PROCESSED_FILE_PATH = PROCESSED_DATA_FILE_PATH + 'ui/deaths_pop_flat_table.csv'


DEFAULT_COUNTRIES_LIST = ["Germany","France","Italy"]