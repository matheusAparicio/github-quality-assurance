from validators.github_validator import GithubValidator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SearchValidator(GithubValidator):

    def __init__(self, driver: webdriver):
        super().__init__(driver)
        self.commonWords = ["project", 'a', "car", "light", "color", "api", "ufsc", "letter", "matheus"]

    def validateSearch(self):
        testsPassed = 0
        for word in self.commonWords:
            if self.validateSingleSearch(word):
                testsPassed += 1
        if testsPassed < len(self.commonWords):
            print("[!] Search failed!")
        else:
            print("[+] Search successful!")

    def validateSingleSearch(self, searchTerm='a'):
        self.driver.get("https://github.com/")
        searchBar = self.driver.find_element(By.NAME, 'q')
        searchBar.clear()
        searchBar.send_keys(searchTerm)
        searchBar.submit()

        # Check if at last 2 search match counter are visible.
        WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.js-codesearch-count")),
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.js-codesearch-count"))
        )

        counterTexts = []
        zeroMatchesFound = 0
        # Pass through loaded counters and check how many 0 matches exists.
        for i in self.driver.find_elements(By.CSS_SELECTOR, "span.js-codesearch-count"):
            if i.text != '':
                counterTexts.append(i.text)
                if i.text == '0':
                    zeroMatchesFound += 1

        resultTitles = []
        for i in self.driver.find_elements(By.CLASS_NAME, "v-align-middle"):
            if i.is_displayed() and i.text != '':
                resultTitles.append(i)
        resultDescriptions = self.driver.find_elements(By.CLASS_NAME, "mb-1")
        loadedResults = resultTitles + resultDescriptions
        searchMatches = 0

        for i in (resultTitles + resultDescriptions):
            if searchTerm.lower() in i.text.lower():
                searchMatches += 1

        # If at least half of the matches counters has a value different from 0 and
        # if search term match with enough repository titles & descriptions.
        if zeroMatchesFound < len(counterTexts) / 2 and searchMatches >= (len(loadedResults) // 2):
            return True
        return False
