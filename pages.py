from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:

    # -------- LOCATORS --------
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    request_taxi_btn = (By.CLASS_NAME, "button-round")

    comfort_tariff = (By.XPATH, "//div[text()='Comfort']")
    comfort_selected = (
        By.XPATH,
        "//div[text()='Comfort' and contains(@class,'active')]",
    )

    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    phone_code_input = (By.ID, "code")

    add_card_btn = (By.CLASS_NAME, "pp-plus")
    card_number_input = (By.ID, "number")
    card_code_input = (By.NAME, "code")

    driver_message = (By.ID, "comment")

    blanket_slider = (
        By.XPATH,
        "//div[text()='Manta y pañuelos']/following::span[contains(@class,'slider')][1]",
    )

    icecream_plus = (By.CLASS_NAME, "counter-plus")
    icecream_value = (By.CLASS_NAME, "counter-value")

    confirm_order_btn = (By.CLASS_NAME, "smart-button")
    order_modal = (By.CLASS_NAME, "order-header-title")

    # -------- INIT --------
    def __init__(self, driver):
        self.driver = driver

    # -------- ROUTE --------
    def set_route(self, from_address, to_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_attribute("value")

    # -------- TARIFF --------
    def click_request_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.request_taxi_btn)
        ).click()

    def select_comfort(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comfort_tariff)
        ).click()

    def is_comfort_selected(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.comfort_selected)
        ).is_displayed()

    # -------- PHONE --------
    def open_phone_modal(self):
        self.driver.find_element(*self.phone_button).click()

    def fill_phone_number(self, number):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.phone_input)
        ).send_keys(number)

    def enter_phone_code(self, code):
        self.driver.find_element(*self.phone_code_input).send_keys(code)

    # -------- CARD --------
    def click_add_card(self):
        self.driver.find_element(*self.add_card_btn).click()

    def fill_card_info(self, number, code):
        self.driver.find_element(*self.card_number_input).send_keys(number)
        self.driver.find_element(*self.card_code_input).send_keys(code)

    # -------- MESSAGE --------
    def set_driver_message(self, message):
        self.driver.find_element(*self.driver_message).send_keys(message)

    # -------- EXTRAS --------
    def enable_blanket(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.blanket_slider)
        ).click()

    def add_icecream(self, amount):
        for _ in range(amount):
            self.driver.find_element(*self.icecream_plus).click()

    def get_icecream_count(self):
        return self.driver.find_element(*self.icecream_value).text

    # -------- ORDER --------
    def confirm_taxi(self):
        self.driver.find_element(*self.confirm_order_btn).click()

    def wait_for_order_modal(self):
        return WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located(self.order_modal)
        ).is_displayed()