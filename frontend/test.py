import selenium
from selenium import webdriver
import unittest
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pprint import pprint
from pathlib import Path
import json
import random
import sys


class buy_parking_dining(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = webdriver.support.ui.WebDriverWait(self.browser, time_out)
        self.coupon_index = None
        self.guest_number = None

    def test_buy(self):
        self.select_event()
        # check core elements supposed to appear when landing on book page
        # self.find_nav_step('parking', True)
        # self.find_nav_step('dining', False)
        # self.find_parking_category(True)
        # self.find_dining_category(False)
        # self.find_event_banner()
        # self.find_event_image()
        # self.find_cart(0)
        # self.find_language_selector()
        category = self.check_activate_category()

        if category == translations['parking']:
            self.select_random_parking()
            self.click_dining()
            self.check_random_coupon_with_changes()
        elif category == translations['dining']:
            self.check_random_coupon_with_changes()
            self.click_parking()
            self.select_random_parking()
        # Todo add hotel select

        self.click_confirmation()
        # should wait a bit to make sure the usr_sesson update api response
        time.sleep(3)
        # refresh page to see if the usr_session can be restored
        self.browser.refresh()
        self.click_confirmation()
        self.fill_personal_info()
        self.fill_credit_card()
        self.click_buy()
        self.check_buy_success()
        time.sleep(5)

    def select_event(self):
        print('Loading page: ', landing_url)
        self.browser.get(landing_url)
        print('Loaded page: ', landing_url)
        event_list = self.wait.until(
            lambda browser: self.browser.find_element_by_class_name('Select-placeholder'))
        event_list.click()
        # automatically get the first element
        option = self.wait.until(
            lambda browser: self.browser.find_element_by_class_name('Select-option'))
        option.click()

    def query_equal(self, selector, expect):
        element = self.wait.until(
            lambda browser: self.browser.find_element_by_css_selector(selector))
        if element.text == expect:
            return element
    # catory box

    def check_activate_category(self):
        selector = 'div.category-btn.active > span.category-item'
        cateory = self.wait.until(
            lambda browser: self.browser.find_element_by_css_selector(selector))
        return cateory.text

    def find_event_banner(self):
        selector = "div.soleil-desc p"
        self.wait.until_not(
            lambda browser: self.browser.find_element_by_css_selector(selector).text == '')
        print('Finding event banner text-event')
        selector = "div.soleil-desc p strong"
        self.wait.until_not(
            lambda browser: self.browser.find_element_by_css_selector(selector).text == '')
        print('Event banner text-event found')

        print('Finding event banner text-event')
        selector = "div.soleil-desc p i"
        self.wait.until_not(
            lambda browser: self.browser.find_element_by_css_selector(selector).text == '')
        print('Event banner text-event found')

    def find_event_image(self):
        selector = '.soleil-img img'
        image = self.wait.until(
            lambda browser: self.browser.find_element_by_css_selector(selector))
        if not image.size['width'] > 0 or not image.size['height'] > 0:
            raise Exception('Event image not display correctly')

    def find_dining_category(self, active):
        print('Finding Dining category element')
        selector = "div.category-box-wrapper ul > li:nth-child(2) div.category-btn span.category-item"
        if active:
            selector = "div.category-box-wrapper ul > li:nth-child(2) div.category-btn.active span.category-item"
        return self.query_equal(selector, translations['dining'])

    def click_dining(self):
        self.find_dining_category(False).click()

    def find_parking_category(self, active):
        print('Finding parking category element')
        selector = "div.category-box-wrapper ul > li:nth-child(1) div.category-btn span.category-item"
        if active:
            selector = "div.category-box-wrapper ul > li:nth-child(1) div.category-btn.active span.category-item"
        return self.query_equal(selector, translations['parking'])

    def click_parking(self):
        self.find_parking_category(False).click()

    def find_confirmation_category(self, active):
        print('Finding confirmation category item')
        selector = "div.category-box-wrapper  ul > li:nth-child(3) div.category-btn span"
        if active:
            selector = "div.category-box-wrapper  ul > li:nth-child(3) div.category-btn.active span"
        return self.query_equal(selector, translations['confirmation'])

    def click_confirmation(self):
        self.find_confirmation_category(False).click()

    # Parking container
    def select_random_parking(self):
        parkings = self.wait.until(
            lambda browser: self.browser.find_elements_by_class_name("parking-item"))
        index = random.randint(0, len(parkings) - 1)
        parkings[index].find_element_by_class_name('plus-btn').click()

    def find_map(self):
        print('Finding map')
        selector = "div.map-wrapper"
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    # dining
    def select_random_coupon(self):
        coupons = self.wait.until(
            lambda browser: self.browser.find_elements_by_class_name("restaurant-coupon"))
        if not self.coupon_index and self.coupon_index != 0:
            self.coupon_index = random.randint(0, len(coupons) - 1)
        return coupons[self.coupon_index]

    def check_random_coupon(self):
        self.select_random_coupon().find_element_by_class_name('plus-btn').click()

    def check_random_coupon_with_changes(self):
        self.select_guest()
        self.select_random_coupon().find_element_by_class_name('plus-btn').click()

    def select_guest(self):
        guest_selector = self.select_random_coupon(
        ).find_element_by_class_name('no-guests-selector')

        select = Select(guest_selector)
        if not self.guest_number:
            self.guest_number = random.randint(
                0, len(select.options) - 1)

        select.select_by_index(self.guest_number)

        # confirmation

    def fill_personal_info(self):
        state = Select(self.wait.until(
            lambda browser: self.browser.find_element_by_id("state")))
        state.select_by_value('CA,QC')
        self.wait.until(lambda browser: self.browser.find_element_by_id(
            "firstname")).send_keys("Hervé")
        self.wait.until(lambda browser: self.browser.find_element_by_id(
            "lastname")).send_keys("Test")
        self.wait.until(lambda browser: self.browser.find_element_by_id(
            "email")).send_keys("leaves.woods92@gmail.com")
        self.wait.until(lambda browser: self.browser.find_element_by_id(
            "_address.address1")).send_keys("51  rue du Fossé des Tanneurs")

        self.wait.until(lambda browser: self.browser.find_element_by_id(
            "_address.city")).send_keys("montreal")
        self.wait.until(lambda browser: self.browser.find_element_by_id(
            "_address.postal_code")).send_keys("H4L2H3")
        self.wait.until(lambda browser: self.browser.find_element_by_id(
            "_contact.phone_number")).send_keys("5145555555")

    def fill_credit_card(self):
        # The cc form is wrapped in react-stripe element by using iframe for
        # each field, and also simply send keys would not work
        # use key stroke to simulate the most original input from client side
        self.browser.switch_to.frame(0)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)

        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)

        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)

        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='cardnumber']").send_keys(Keys.NUMPAD2)

        self.browser.switch_to.default_content()

        self.browser.switch_to.frame(1)
        self.browser.find_element_by_xpath(
            "//input[@name='exp-date']").send_keys(Keys.NUMPAD0)
        self.browser.find_element_by_xpath(
            "//input[@name='exp-date']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='exp-date']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='exp-date']").send_keys(Keys.NUMPAD2)
        self.browser.switch_to.default_content()

        self.browser.switch_to.frame(2)
        self.browser.find_element_by_xpath(
            "//input[@name='cvc']").send_keys(Keys.NUMPAD1)
        self.browser.find_element_by_xpath(
            "//input[@name='cvc']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='cvc']").send_keys(Keys.NUMPAD3)
        self.browser.switch_to.default_content()

        self.browser.switch_to.frame(3)
        self.browser.find_element_by_xpath(
            "//input[@name='postal']").send_keys(Keys.NUMPAD1)
        self.browser.find_element_by_xpath(
            "//input[@name='postal']").send_keys(Keys.NUMPAD2)
        self.browser.find_element_by_xpath(
            "//input[@name='postal']").send_keys(Keys.NUMPAD3)
        self.browser.find_element_by_xpath(
            "//input[@name='postal']").send_keys(Keys.NUMPAD4)
        self.browser.find_element_by_xpath(
            "//input[@name='postal']").send_keys(Keys.NUMPAD5)
        self.browser.switch_to.default_content()

    def click_buy(self):
        self.wait.until(
            lambda browser: self.browser.find_element_by_class_name("submit-btn"))
        self.browser.execute_script(
            "document.querySelector('.submit-btn').click()")

    def check_facture_dispay(self):
        self.wait.until_not(lambda browser: self.browser.find_element_by_class_name(
            "modal-title").text == '')

    def check_buy_success(self):
        try:
            self.check_facture_dispay()
        except TimeoutException:
            self.wait.until(EC.alert_is_present())

    # header
    def find_nav_step(self, step_name, active):
        step = 1
        if step_name == 'dining':
            step = 2
        elif step_name == 'confirmation':
            step = 3
        selector = f'div.page-header.row .categories ul > li:nth-child({step})'
        step_element = self.query_equal(selector, translations[step_name])
        selector = f'div.page-header.row .categories ul > li:nth-child({step}) span img'
        if active:
            selector = f'div.page-header.row .categories ul > li:nth-child({step}) span.current img'
        image = self.wait.until(
            lambda browser: self.browser.find_element_by_css_selector(selector))
        if image.size['width'] <= 0 or image.size['height'] <= 0:
            raise Exception(f'{step_name} step image not display correctly')
        else:
            return step_element

    def find_cart(self, item_count):
        selector = '.page-header .cart-wrapper .checkout svg.cart'
        cart = self.wait.until(
            lambda browser: self.browser.find_element_by_css_selector(selector))
        if item_count > 0:
            selector = '.page-header .cart-wrapper .checkout span.number-box'
            self.query_equal(selector, str(item_count))
        return cart

    def click_cart(self):
        # pass 0, click only should not care about the number
        self.find_cart(0).click()

    def find_language_selector(self):
        selector = '.language-selector select'
        return self.wait.until(lambda browser: self.browser.find_element_by_css_selector(selector))

    def switch_language(self, language):
        language_selector = self.find_language_selector()
        language_selector.click()
        option_number = 1
        if language == 'fr':
            option_number = 2
        selector = f'.language-selector select option:nth-child({option_number})'
        option = self.wait.until(
            lambda browser: self.browser.find_element_by_css_selector(selector))
        option.click()

    def load_local_storage(self, local_storage_string):
        storage_object = json.loads(local_storage_string)
        # for item in storage_object:
        #     # import pdb; pdb.set_trace()
        #     value = storage_object[item]
        #     self.browser.execute_script(f"window.localStorage.setItem({item}, {value})")
        # import pdb; pdb.set_trace()
        self.browser.execute_script(
            f'window.localStorage.setItem("pyetoday_venue", JSON.stringify({storage_object["pyetoday_venue"]}))')

    def tearDown(self):
        # filename = 'pye-frontend-screenshot-' + str(time.time()) + ".png"
        # self.browser.save_screenshot(filename)
        self.browser.quit()


if __name__ == '__main__':
    test_env = 'local'
    if (len(sys.argv) > 1):
        test_env = sys.argv[1]

    landing_url = 'http://localhost:8000/landing/tsd?ln=fr'
    if test_env == 'dev':
        landing_url = 'https://dev.pye.today/landing/tsd?ln=fr'
    elif test_env == 'urban':
        landing_url = 'https://urban.pye.today/landing/tsd?ln=fr'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1380,900")
    # chrome_options.add_argument("--headless")
    time_out = 20
    home_path = str(Path.home())
    en_tranlation_path = home_path + '/code/pye.today-front-end/src/translations/en.json'
    fr_tranlation_path = home_path + '/code/pye.today-front-end/src/translations/fr.json'
    translations = ''
    if 'ln=en' in landing_url:
        with open(en_tranlation_path) as f:
            translations = json.load(f)
    elif 'ln=fr' in landing_url:
        with open(fr_tranlation_path) as f:
            translations = json.load(f)
    else:
        raise Exception('should provide a lanuage param in url')

    del sys.argv[1:]
    unittest.main()
