import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(data.address_from, data.address_to)
        self.page.click_request_taxi()
        self.page.select_comfort()

    # 1️⃣ Dirección
    def test_set_route(self):
        assert self.page.get_from() == data.address_from
        assert self.page.get_to() == data.address_to

    # 2️⃣ Comfort
    def test_select_comfort(self):
        assert self.page.is_comfort_selected()

    # 3️⃣ Teléfono
    def test_add_phone(self):
        self.page.open_phone_modal()
        self.page.fill_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        self.page.enter_phone_code(code)
        assert True

    # 4️⃣ Tarjeta
    def test_add_card(self):
        self.page.click_add_card()
        self.page.fill_card_info(data.card_number, data.card_code)
        assert True

    # 5️⃣ Confirmación tarjeta
    def test_card_code_confirmation(self):
        self.page.click_add_card()
        self.page.fill_card_info(data.card_number, data.card_code)
        assert True

    # 6️⃣ Mensaje conductor
    def test_driver_message(self):
        self.page.set_driver_message(data.message_for_driver)
        assert True

    # 7️⃣ Manta
    def test_enable_blanket(self):
        self.page.enable_blanket()
        assert True

    # 8️⃣ Helados
    def test_add_icecream(self):
        self.page.add_icecream(2)
        assert self.page.get_icecream_count() == "2"

    # 9️⃣ Modal búsqueda taxi
    def test_complete_order(self):
        self.page.add_icecream(2)
        self.page.confirm_taxi()
        assert self.page.wait_for_order_modal()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()