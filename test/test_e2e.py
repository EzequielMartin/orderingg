import unittest
import os
import time
import threading

from selenium import webdriver

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

from werkzeug.serving import make_server

class Ordering(unittest.TestCase):
    # Creamos la base de datos de test
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.baseURL = 'http://localhost:5000'

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.t = threading.Thread(target=self.app.run)
        self.t.start()

        time.sleep(1)

        self.driver = webdriver.Chrome()
    '''
    def test_title(self):
        driver = self.driver
        driver.get(self.baseURL)
        add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        add_product_button.click()
        modal = driver.find_element_by_id('modal')
        assert modal.is_displayed(), "El modal no esta visible"
    '''
    def test_InfoModalEditar(self):
        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Tenedor', price= 50)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)
        time.sleep(5)

        edit_product_button = driver.find_element_by_xpath('/html/body/main/div[2]/div/table/tbody/tr[1]/td[6]/button[1]')
        edit_product_button.click()

        producto = driver.find_element_by_xpath('//*[@id="select-prod"]')
        cantidad = driver.find_element_by_xpath('//*[@id="quantity"]')
        value_prod = producto.get_attribute("value")
        value_cant = cantidad.get_attribute("value")
        boton_cerrar_modal = driver.find_element_by_xpath('//*[@id="modal"]/div[2]/footer/button[3]')
        time.sleep(5)
        boton_cerrar_modal.click()
        self.assertTrue(value_prod != "", "No tiene informacion")
        self.assertTrue(value_cant != "", "No tiene informacion")

    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()

