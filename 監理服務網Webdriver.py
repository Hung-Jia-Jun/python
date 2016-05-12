# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,os

class WebDriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        os.system("pause")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.mvdis.gov.tw/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_web_driver(self):
        driver = self.driver
        driver.get(self.base_url + "/m3-emv-plate/webpickno/queryPickNo#anchor")
        driver.find_element_by_link_text("1750-S5").click()
        driver.find_element_by_css_selector("span.enable").click()
        Select(driver.find_element_by_id("ownerType")).select_by_visible_text(u"自然人")
        driver.find_element_by_css_selector("option[value=\"1\"]").click()
        driver.find_element_by_css_selector("div.blockUI.blockOverlay").click()
        driver.find_element_by_css_selector("span.enable").click()
        Select(driver.find_element_by_id("processType")).select_by_visible_text(u"代辦")
        driver.find_element_by_css_selector("#processType > option[value=\"2\"]").click()
        # ERROR: Caught exception [Error: Dom locators are not implemented yet!]
        Select(driver.find_element_by_name("countyText")).select_by_visible_text(u"臺北市")
        driver.find_element_by_id("carSeriesNo").click()
        driver.find_element_by_id("carSeriesNo").clear()
        driver.find_element_by_id("carSeriesNo").send_keys("WDC1569421J239617")
        driver.find_element_by_id("ownerName").clear()
        driver.find_element_by_id("ownerName").send_keys("DSAFAD")
        driver.find_element_by_id("ownerUid").clear()
        driver.find_element_by_id("ownerUid").send_keys("A129162302")
        driver.find_element_by_link_text(u"確定").click()
        driver.find_element_by_name("Accept").click()
        driver.find_element_by_id("rdoBank").click()
        Select(driver.find_element_by_id("bankId")).select_by_visible_text(u"008,華南商業銀行")
        driver.find_element_by_id("accountNo").clear()
        driver.find_element_by_id("accountNo").send_keys("451231234564213")
        driver.find_element_by_id("acceptWarning").click()
        driver.find_element_by_id("confirm").click()
        driver.find_element_by_link_text(u"自然人憑證驗證").click()
        driver.find_element_by_xpath("(//input[@id='pin'])[2]").clear()
        driver.find_element_by_xpath("(//input[@id='pin'])[2]").send_keys("a80720A")
        driver.find_element_by_xpath(u"(//a[contains(text(),'確定')])[3]").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
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
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
