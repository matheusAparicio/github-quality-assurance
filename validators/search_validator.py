from validators.github_validator import GithubValidator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SearchValidator(GithubValidator):

    def __init__(self, driver: webdriver):
        super().__init__(driver)
        # Words with almost granted search results.
        self.commonWords = ["project", 'a', "car", "light", "color", "api", "ufsc", "letter", "matheus"]

    def validateSearch(self):
        testsPassed = 0
        failedWords = []
        for word in self.commonWords:
            if self.validateSingleSearch(word):
                testsPassed += 1
            else:
                failedWords.append(word)

        if testsPassed < len(self.commonWords):
            print(f"[!] Search failed! {testsPassed}/{len(self.commonWords)} tests passed. "
                  f"The failed words was {failedWords}")
        else:
            print("[+] Search successful!")

    def validateSingleSearch(self, searchTerm='a'):
        self.driver.get("https://github.com/")
        searchBar = self.driver.find_element(By.NAME, 'q')
        searchBar.clear()
        searchBar.send_keys(searchTerm)
        searchBar.submit()

        # If both tests are successfully, the search is validated.
        if self.__validateSingleSearchMatchNumber(searchTerm) and self.__validateSingleSearchMatches(searchTerm):
            return True
        return False

    # Check if more than 0 results exists in at least half of the search categories verified.
    def __validateSingleSearchMatchNumber(self, searchTerm: str):
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

        # If at least half of the matches counters has a value different from 0.
        if zeroMatchesFound < len(counterTexts) / 2:
            return True
        return False

    # Get the search results and pass through repositories names and descriptions.
    # If the searchTerm is encountered in at least half of these, the search term is validated.
    def __validateSingleSearchMatches(self, searchTerm: str):
        # Check if at last 2 possible search match are visible.
        WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "v-align-middle")),
            EC.visibility_of_element_located((By.CLASS_NAME, "mb-1"))
        )

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

        # If search term match with enough repository titles & descriptions.
        if searchMatches >= (len(loadedResults) // 2):
            return True
        return False
