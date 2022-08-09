from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities import utilities


class GithubValidator:

    def __init__(self, userName: str, password: str):
        self.userName = userName
        self.password = password
        self.driver = webdriver.Firefox()
        self.commonWords = ["project", 'a', "car", "light", "color", "api", "ufsc", "letter", "matheus"]

    def validateLogin(self):
        self.driver.get("https://github.com/login")

        WebDriverWait(self.driver, timeout=5).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )

        self.driver.find_element(By.ID, "login_field").send_keys(self.userName)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "commit").click()

        self.waitPageLoadScript()

        errorMessage = "Incorrect username or password"
        errors = self.driver.find_elements(By.CLASS_NAME, "flash-error")
        if any(errorMessage in e.text for e in errors):
            print(f"[!] Login failed! {errorMessage}")
            #self.finalizeValidator()
        else:
            if self.driver.current_url != "https://github.com/sessions/verified-device":
                print("[+] Login successful!")
            else:
                print("[!] Login parcially successful. Email authentication required.")


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

        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.visibility_of_any_elements_located((By.XPATH, "/html/body/div[5]/div/aside/div/div[2]/div/h2/a | /html/body/div[5]/div/aside/div/div[1]/div/div/a[1]"))
            )
            newRepositoryButton = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/aside/div/div[2]/div/h2/a | /html/body/div[5]/div/aside/div/div[1]/div/div/a[1]")
            newRepositoryButton.click()
            WebDriverWait(self.driver, timeout=10).until(
                EC.visibility_of_element_located((By.ID, "repository_name"))
            )
            self.driver.find_element(By.ID, "repository_name").send_keys(f"{utilities.randomString(6)}-{utilities.randomString(6)}")
            self.driver.find_element(By.ID, "repository_visibility_private").click()
            try:
                WebDriverWait(self.driver, timeout=10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
                )
                self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
            except:
                print("[!] Failure! Project name wasn't accepted.")

            try:
                WebDriverWait(self.driver, timeout=5).until(
                    EC.visibility_of_element_located((By.ID, "code-tab"))
                )
                print("[+] Repository created successfully!")
            except:
                print("[!] Repository creation failure.")

        except:
            print("[!] Repository creation error! No create repository button was found.")
            return

    def validateOther(self):
        pass

    def waitPageLoadScript(self, timeout=10, script="return document.readyState === 'complete'"):
        try:
            WebDriverWait(driver=self.driver, timeout=timeout).until(
                lambda x: x.execute_script(script)
            )
        except TimeoutError:
            print("Falha ao executar script.")

    def finalizeValidator(self):
        self.driver.quit()
        exit(1)
