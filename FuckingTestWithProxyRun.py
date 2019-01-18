# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


ProxyHost = "54.84.95.51"
ProxyPort = "8083"


class ProxyCh(webdriver.FirefoxProfile):

    def ChangeProxy(self, ProxyHost, ProxyPort):
        self.profile = webdriver.FirefoxProfile()
        profile = self.profile
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", ProxyHost)
        profile.set_preference("network.proxy.http_port", int(ProxyPort))
        profile.update_preferences()
        return webdriver.Firefox(firefox_profile=profile)


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        self.driver = ProxyCh.ChangeProxy(self,ProxyHost, ProxyPort)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.ie/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test(self):
        driver = self.driver
        driver.get("https://ya.ru/")
        driver.find_element_by_id("text").send_keys("python emoji")
        driver.find_element_by_id("text").send_keys(Keys.DOWN)
        driver.find_element_by_id("text").send_keys(Keys.ENTER)


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()

