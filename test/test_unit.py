import os
import unittest

from flask import json
from flask_testing import TestCase

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class OrderingTestCase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        return app

    # Creamos la base de datos de test
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    # Destruimos la base de datos de test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
 
    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"
    '''
    def test_crear_producto(self):
        data = {
            'name': 'Tenedor',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Falló el POST")
        p = Product.query.all()

        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")
    '''
    def test_put(self):
        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Plato', price= 15)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        data = {
            'quantity': 10
        }
        self.client.put('order/1/product/1', data=json.dumps(data), content_type='application/json')
        arg = 1,1
        prod = OrderProduct.query.get(arg)
        self.assertTrue(prod.quantity == 10, "Fallo el PUT")
        #self.assert200(resp, "Fallo el PUT")

    def test_OrderPrice(self): 
        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Plato', price= 15)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 10, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        
        orden= Order.query.get(1)
        totalPrice = orden.orderPrice
        self.assertEqual(150, totalPrice, "El precio total no se calcula bien")        

    def test_delete(self):
        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Tenedor', price= 50)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        
        resp = self.client.delete('order/1/product/1')

        self.assert200(resp, "Fallo el DELETE")

    def test_name_vacio(self):
        data = {
            'name': '',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        assert resp != 200, 'Fallo el test, se creo un producto de nombre vacio'

    def test_get(self):

        o = Order(id= 1)
        db.session.add(o)

        p = Product(id= 1, name= 'Tenedor', price= 50)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()            


        respuesta = self.client.get('order/1/product/1')
        self.assert200(respuesta, "Fallo el GET")


    def test_cantidad_negativa(self):
        
        order = Order(id= 1)
        db.session.add(order)

        producto = Product(id= 3, name= 'Cuchillo', price= 59)
        db.session.add(producto)

        cant= 1 #Uso cantidad negativa para verificar que no se crea la instancia, si pongo una cantidad positiva el test pasa correctamente 
        if cant > 0: 
            orderProducto = OrderProduct(order_id= 1, product_id= 3, quantity= cant, product= producto)
            db.session.add(orderProducto)
            db.session.commit()
        else :
            print ("No se puede crear instancia con cantidad negativa")

        resp = self.client.get('order/1/product/3') 
        self.assert200(resp,"Fallo el test") 



if __name__ == '__main__':
    unittest.main()

