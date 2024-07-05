from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

data = {
    'League':[],
    'Teams':[],
    'Score':[]
}
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without opening GUI)
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (often necessary in headless mode)

# Initialize Chrome WebDriver
# service = Service(executable_path=chromedriver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome()

count = 30

url = 'https://www.whoscored.com/LiveScores'
driver.get(url)

try:
    leagues = driver.find_elements(By.CSS_SELECTOR,'div[class="Accordion-module_accordion__UuHD0"]')
    for league in leagues:
        league.click()
        league_name = league.find_element(By.CSS_SELECTOR,'a')
        matches = league.find_elements(By.CSS_SELECTOR,'div[class="Match-module_row__zwBOn"]')
        if len(matches)==0:
            league.find_element(By.CSS_SELECTOR,'div[class="RotatingChevron-module_chevronDown__4mhZF"]').click()
            matches = league.find_elements(By.CSS_SELECTOR,'div[class="Match-module_row__zwBOn"]')
        for match in matches:
            scores = []
            teams = []
            try:
                score_spans = match.find_element(By.CSS_SELECTOR,'a')
            except:
                score_spans = match.find_element(By.CSS_SELECTOR,'a[id="scoresBtn-1832774"]')
            score_spans = score_spans.find_elements(By.CSS_SELECTOR,'span')
            for span in score_spans:
                scores.append(span.text)
            data['Score'].append(scores)

            teams_div = match.find_elements(By.CSS_SELECTOR,'a[class="Match-module_teamNameText__Dqv-G"]')
            for team in teams_div:
                teams.append(team.text)
            data['Teams'].append(teams)
            data['League'].append(league_name.text)
        print(league_name.text, len(matches))



finally:
    # Close the WebDriver
    df = pd.DataFrame.from_dict(data)
    df.columns = data.keys()
    df.to_csv("data.csv",index=False)
    driver.quit()
