from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


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

        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        errorMessage = "Incorrect username or password"
        errors = self.driver.find_elements(By.CLASS_NAME, "flash-error")
        if any(errorMessage in e.text for e in errors):
            print(f"[!] Login failed! {errorMessage}")
        else:
            print("[+] Login successful!")

    def finalizeValidator(self):
        self.driver.quit()
