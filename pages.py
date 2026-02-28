from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:

    # ---------- LOCATORS ----------
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")

    request_taxi_btn = (By.CLASS_NAME, "smart-button")

    comfort_tariff = (By.XPATH, "//div[text()='Comfort']")
    comfort_selected = (
        By.XPATH,
        "//div[text()='Comfort' and contains(@class,'active')]",
    )

    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    phone_code_input = (By.ID, "code")
    phone_confirmed = (By.CLASS_NAME, "np-text")

    payment_button = (By.CLASS_NAME, "pp-button")
    add_card_btn = (By.CLASS_NAME, "pp-plus")
    card_number_input = (By.ID, "number")
    card_code_input = (By.NAME, "code")
    card_added_label = (By.CLASS_NAME, "pp-value")

    driver_message = (By.ID, "comment")

    blanket_slider = (
        By.XPATH,
        "//div[text()='Manta y pañuelos']/following::span[contains(@class,'slider')][1]",
    )
    blanket_active = (
        By.XPATH,
        "//div[text()='Manta y pañuelos']/ancestor::div[contains(@class,'active')]",
    )

    icecream_plus = (By.CLASS_NAME, "counter-plus")
    icecream_value = (By.CLASS_NAME, "counter-value")

    confirm_order_btn = (By.CLASS_NAME, "smart-button")
    order_modal = (By.CLASS_NAME, "order-header-title")

    # ---------- INIT ----------
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------- ROUTE ----------
    def set_route(self, from_address, to_address):
        from_input = self.wait.until(
            EC.visibility_of_element_located(self.from_field)
        )
        from_input.clear()
        from_input.send_keys(from_address)

        to_input = self.wait.until(
            EC.visibility_of_element_located(self.to_field)
        )
        to_input.clear()
        to_input.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_attribute("value")

    # ---------- TARIFF ----------
    def click_request_taxi(self):
        self.wait.until(
            EC.element_to_be_clickable(self.request_taxi_btn)
        ).click()

    def select_comfort(self):
        self.wait.until(
            EC.element_to_be_clickable(self.comfort_tariff)
        ).click()

    def is_comfort_selected(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.comfort_selected)
        ).is_displayed()

    # ---------- PHONE ----------
    def open_phone_modal(self):
        self.wait.until(
            EC.element_to_be_clickable(self.phone_button)
        ).click()

    def fill_phone_number(self, number):
        self.wait.until(
            EC.visibility_of_element_located(self.phone_input)
        ).send_keys(number)

    def enter_phone_code(self, code):
        self.wait.until(
            EC.visibility_of_element_located(self.phone_code_input)
        ).send_keys(code)

    def is_phone_added(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.phone_confirmed)
        ).is_displayed()

    # ---------- CARD ----------
    def open_payment_modal(self):
        self.wait.until(
            EC.element_to_be_clickable(self.payment_button)
        ).click()

    def click_add_card(self):
        self.wait.until(
            EC.element_to_be_clickable(self.add_card_btn)
        ).click()

    def fill_card_info(self, number, code):
        self.wait.until(
            EC.visibility_of_element_located(self.card_number_input)
        ).send_keys(number)

        self.wait.until(
            EC.visibility_of_element_located(self.card_code_input)
        ).send_keys(code)

    def is_card_added(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.card_added_label)
        ).is_displayed()

    # ---------- MESSAGE ----------
    def set_driver_message(self, message):
        field = self.wait.until(
            EC.visibility_of_element_located(self.driver_message)
        )
        field.clear()
        field.send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(
            *self.driver_message
        ).get_attribute("value")

    # ---------- EXTRAS ----------
    def enable_blanket(self):
        self.wait.until(
            EC.element_to_be_clickable(self.blanket_slider)
        ).click()

    def is_blanket_enabled(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.blanket_active)
        ).is_displayed()

    def add_icecream(self, amount):
        for _ in range(amount):
            self.wait.until(
                EC.element_to_be_clickable(self.icecream_plus)
            ).click()

    def get_icecream_count(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.icecream_value)
        ).text

    # ---------- ORDER ----------
    def confirm_taxi(self):
        self.wait.until(
            EC.element_to_be_clickable(self.confirm_order_btn)
        ).click()

    def wait_for_order_modal(self):
        return WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located(self.order_modal)
        ).is_displayed()