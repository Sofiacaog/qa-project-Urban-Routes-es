import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    comfort_selected = (By.XPATH, "//div[text()='Comfort' and contains(@class,'active')]")
    def is_comfort_selected(self):
        return WebDriverWait(self.driver, 10).until(
             expected_conditions.visibility_of_element_located(self.comfort_selected)
         ).is_displayed()

    # Campo mensaje conductor
    driver_message_input = (By.ID, "comment")

    def set_driver_message(self, message):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.driver_message_input)
        ).send_keys(message)

    blanket_slider = (By.XPATH, "//div[text()='Manta y pañuelos']/following::span[contains(@class,'slider')][1]")
    def enable_blanket(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.blanket_slider)
        ).click()

    icecream_plus = (By.CLASS_NAME, "counter-plus")
    icecream_value = (By.CLASS_NAME, "counter-value")

    def add_icecream(self, amount):
        for _ in range(amount):
            WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable(self.icecream_plus)
            ).click()

    def get_icecream_count(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.icecream_value)
        ).text

    confirm_taxi_button = (By.CLASS_NAME, "smart-button")
    def confirm_taxi(self):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.confirm_taxi_button)
        ).click()

    driver_info_modal = (By.CLASS_NAME, "order-header-title")
    def wait_for_driver_info(self):
        return WebDriverWait(self.driver, 40).until(
            expected_conditions.visibility_of_element_located(self.driver_info_modal)
        ).is_displayed()

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.select_comfort()
        assert routes_page.is_comfort_selected()  # validación simple (ejemplo: que Comfort esté seleccionado)

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.select_comfort()
        routes_page.open_phone_modal()
        routes_page.fill_phone_number(data.phone_number)
        # obtener código automático
        code = retrieve_phone_code(self.driver)
        routes_page.enter_phone_code(code)
        assert routes_page.is_phone_added()

    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.select_comfort()
        # teléfono primero (requisito del sistema)
        routes_page.open_phone_modal()
        routes_page.fill_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        routes_page.enter_phone_code(code)
        # agregar tarjeta
        routes_page.open_payment_modal()
        routes_page.click_add_card()
        routes_page.fill_card_info(
            data.card_number,
            data.card_code
        )
        routes_page.card_code_input.send_keys(Keys.TAB)
        routes_page.close_payment_modal()
        # validación
        assert routes_page.is_card_added()

    def test_add_driver_message(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.select_comfort()
        routes_page.set_driver_message(data.message_for_driver)

    def test_enable_blanket(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.select_comfort()
        routes_page.enable_blanket()

    def test_add_icecream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.select_comfort()
        routes_page.add_icecream(2)
        assert routes_page.get_icecream_count() == "2"

    def test_complete_taxi_order(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.select_comfort()
        routes_page.set_driver_message(data.message_for_driver)
        routes_page.enable_blanket()
        routes_page.add_icecream(2)
        routes_page.confirm_taxi()
        assert routes_page.wait_for_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
