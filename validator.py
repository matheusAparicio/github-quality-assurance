from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class GithubValidator:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.driver = webdriver.Firefox()

    def validateLogin(self):
        self.driver.get("https://github.com/login")

    def validateFinalize(self):
        self.driver.quit()

