from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


class GithubValidator:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.driver = webdriver.Firefox()

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
        self.driver.get("https://github.com/")
        searchBar = self.driver.find_element(By.NAME, 'q')
        searchBar.send_keys("a")
        searchBar.submit()

        sleep(3)

        searchCountersTexts = []
        for i in self.driver.find_elements(By.CLASS_NAME, "js-codesearch-count"):
            if i.text != '':
                searchCountersTexts.append(i.text)

        print(searchCountersTexts)

    def waitPageLoadScript(self, timeout=10, script="return document.readyState === 'complete'"):
        WebDriverWait(driver=self.driver, timeout=timeout).until(
            lambda x: x.execute_script(script)
        )

    def waitPageLoadElementLocated(self, element: str, by=By.ID, timeout=10):
        WebDriverWait(driver=self.driver, timeout=timeout).until(
            EC.presence_of_element_located((by, element))
        )

    def finalizeValidator(self):
        self.driver.quit()
