from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class GithubValidator:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.driver = webdriver.Firefox()
        self.commonWords = ["project", 'a', "car", "light", "color", "api", "ufsc", "letter", "matheus"]

    def validateLogin(self):
        self.driver.get("https://github.com/login")
        self.driver.find_element(By.ID, "login_field").send_keys(self.login)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "commit").click()

        self.waitPageLoadScript()

        errorMessage = "Incorrect username or password"
        errors = self.driver.find_elements(By.CLASS_NAME, "flash-error")
        if any(errorMessage in e.text for e in errors):
            print(f"[!] Login failed! {errorMessage}")
        else:
            print("[+] Login successful!")

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

        WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.js-codesearch-count")),
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.js-codesearch-count"))
        )

        counterTexts = []
        zeroMatchesFound = 0
        for i in self.driver.find_elements(By.CSS_SELECTOR, "span.js-codesearch-count"):
            if i.text != '':
                counterTexts.append(i.text)
                if i.text == '0':
                    zeroMatchesFound += 1

        if zeroMatchesFound < len(counterTexts) / 2:
            return True
        return False

    def validateRepositoryCreation(self):
        self.driver.get("https://github.com/")

        WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Create repository"))
        )

        newRepositoryButton = self.driver.find_element(By.LINK_TEXT, "Create repository")
        newRepositoryButton.click()

    def validateOther(self):
        pass

    def waitPageLoadScript(self, timeout=10, script="return document.readyState === 'complete'"):
        try:
            WebDriverWait(driver=self.driver, timeout=timeout).until(
                lambda x: x.execute_script(script)
            )
        except ConnectionError:
            print("Falha ao executar script.")

    def finalizeValidator(self):
        self.driver.quit()
