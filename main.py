from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd

country = input("Which country do you want to select? (England,Spain,Germany,Italy,France,Scotland,Netherlands,Portugal,Turkey,Greece,Belgium,Brazil,Austria,Russia,Argentina,Denmark,Poland,USA,Norway,Sweden,Finland,Switzerland,Australia,Japan,China,Mexico,Ukraine,Czechia,Saudi Arabia,Colombia,Peru,Ecuador,South Korea) (The casing should match): ")

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')

url = "https://www.adamchoi.co.uk/teamgoals/detailed"

driver = webdriver.Chrome(service=Service(executable_path="chromedriver.exe"), options=chrome_options)

driver.maximize_window()
driver.get(url)

all_matches_button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH,'//label[@analytics-event="All matches"]')))

driver.execute_script("arguments[0].click();", all_matches_button)

# Select the country from the dropdown
dropdown = driver.find_element(By.XPATH, "//select[@id='country']")
dropdown.click()
dropdown.send_keys(country + Keys.RETURN)

# Wait for the matches to load
matches = WebDriverWait(driver, 60).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))

date = []
home_team = []
score = []
away_team = []

# Extract match details
for match in matches:
    date_values = match.find_elements(By.XPATH, './td[1]')
    for date_value in date_values:
        date.append(date_value.get_attribute("innerText"))

    home_team_values = match.find_elements(By.XPATH, './td[2]')
    for home_team_value in home_team_values:
        home_team.append(home_team_value.get_attribute("innerText"))

    score_values = match.find_elements(By.XPATH, './td[3]')
    for score_value in score_values:
        score.append(score_value.get_attribute("innerText"))

    away_team_values = match.find_elements(By.XPATH, './td[4]')
    for away_team_value in away_team_values:
        away_team.append(away_team_value.get_attribute("innerText"))

driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame({"date": date, "home_team": home_team, "score": score, "away_team": away_team})
df.to_csv('football_data.csv', index=False)
print(df)