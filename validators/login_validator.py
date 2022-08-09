from validators.github_validator import GithubValidator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginValidator(GithubValidator):

    def __init__(self, driver: webdriver, userName: str, password: str):
        super().__init__(driver)
        self.userName = userName
        self.password = password

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
            self.finalizeValidator()
        else:
            if self.driver.current_url != "https://github.com/sessions/verified-device":
                print("[+] Login successful!")
            else:
                print("[!] Login partially successful. Email authentication required.")
