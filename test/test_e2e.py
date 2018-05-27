import unittest
import os
import time
import threading

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 

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
    
    def test_delete(self):

        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Tenedor', price= 50)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)
        
        delete_product_button = driver.find_element_by_xpath('/html/body/main/div[2]/div/table/tbody/tr[1]/td[6]/button[2]')
        delete_product_button.click()
        self.assertRaises(NoSuchElementException, driver.find_element_by_xpath, "xpath")

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
    
    def test_cant_negativo(self):
        orden = Order(id= 1)
        db.session.add(orden)
        producto = Product(name= 'Cuchara', price= 20)
        db.session.add(producto)
        db.session.commit()
        driver = self.driver
        driver.get(self.baseURL)
        boton_agregar_producto = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        boton_agregar_producto.click()
        seleccionar_producto = driver.find_element_by_id('select-prod')
        seleccionar_producto.click()
        opcion_seleccionada = driver.find_element_by_xpath('//*[@id="select-prod"]/option[2]')
        opcion_seleccionada.click()
        cantidad_ingresada = driver.find_element_by_xpath('//*[@id="quantity"]')
        cantidad_ingresada.send_keys(Keys.DELETE)
        cant = -20 #Lo uso para probar cantidades negativas y positivas
        cantidad_ingresada.send_keys(str(cant))
        time.sleep(10)
        boton_guardar = driver.find_element_by_xpath('//*[@id="save-button"]')
        boton_guardar.click()
        time.sleep(20) 
        cantidad_en_tabla = driver.find_element_by_xpath('//*[@id="orders"]/table/tbody/tr/td[4]')
        self.assertGreater(int(cantidad_en_tabla.text),0,"Agrego una cantidad negativa")
    
    def test_infoNombreProducto(self):
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

        elem_nombre = driver.find_element_by_xpath('/html/body/main/div[2]/div/table/tbody/tr/td[2]')
        nombre = elem_nombre.text
        time.sleep(5)
        
        self.assertTrue(nombre != '',"El nombre esta vacio")

    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()

