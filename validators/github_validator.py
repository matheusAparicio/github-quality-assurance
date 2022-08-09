from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class GithubValidator:

    def __init__(self, driver: webdriver):
        self.driver = driver

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
