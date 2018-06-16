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
    '''
    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"

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
        o = Order(id=1)
        db.session.add(o)

        p = Product(id=1, name='Plato', price=15)
        db.session.add(p)

        orderproduct = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
        db.session.add(orderproduct)
        db.session.commit()
        data = {
            'quantity': 10
        }
        self.client.put('order/1/product/1', data=json.dumps(data), content_type='application/json')
        arg = 1,1
        prod = OrderProduct.query.get(arg)
        self.assertTrue(prod.quantity == 10, "Fallo el PUT")

    def test_orderprice(self):
        o = Order(id=1)
        db.session.add(o)

        p = Product(id=1, name='Plato', price=15)
        db.session.add(p)

        orderproduct = OrderProduct(order_id=1, product_id=1, quantity=10, product=p)
        db.session.add(orderproduct)
        db.session.commit()

        orden = Order.query.get(1)
        totalprice = orden.orderPrice
        self.assertEqual(150, totalprice, "El precio total no se calcula bien")

    def test_delete(self):
        o = Order(id=1)
        db.session.add(o)

        p = Product(id=1, name='Tenedor', price=50)
        db.session.add(p)

        orderproduct = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
        db.session.add(orderproduct)
        db.session.commit()

        resp = self.client.delete('order/1/product/1')
        q = db.session.query(OrderProduct.product_id).filter_by(order_id=1)  # Busco todos los ids de productos de la orden de id = 1

        self.assert200(resp, "Fallo el DELETE")
        self.assertNotIn(p.id, q, "Fallo el DELETE")  # Agrego un assert que checkea que el producto p de id = 1 ya no esta en la base de datos.

    # Rehago el test de nombre vacio agregando directamente el producto a la db.

    def test_name_vacio(self):
        p = Product(id= 1,name = '', price= 15)
        db.session.add(p)
        db.session.commit()

        productos = Product.query.all()

        assert len(productos) == 0, "Se agrego un producto con nombre vacio" #El test no pasa ya que un bug en el backend permite que se agreguen productos con nombre vacio

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
 
        orderProducto = OrderProduct(order_id= 1, product_id= 3, quantity= -1, product= producto)
        db.session.add(orderProducto)
        db.session.commit()

        arg = 1,3
        orderProd = OrderProduct.query.get(arg)
        cantidad = orderProd.quantity
        assert cantidad > 0, "Fallo el GET" #El test falla porque un bug en el backend permite agregar un producto con cantidad negativa 

    def test_get_product(self):
        p = Product(id=1, name='Vaso', price=50)
        db.session.add(p)
        db.session.commit()

        productos = self.client.get('/product')

        self.assert200(productos, "Fallo el GET")
        assert productos.json[0] == {'id': 1, 'name': 'Vaso', 'price': 50.0}, "Fallo el GET" #Me fijo que el json que me devuelve el get tenga los datos esperados, que tenga id 1, nombre vaso y precio 50

    #El Ejercicio 1C de los opcionales es el mismo que el 2A de los obligatorios, ya esta realizado en este mismo archivo
    
    def test_get_order(self):
        o = Order(id=1)
        db.session.add(o)
        db.session.commit()

        orden = self.client.get('/order/1')

        self.assert200(orden, "Fallo el GET")
        assert orden.json == {'id': 1, 'orderPrice': 0, 'products': []}, "Fallo el GET"  # Me fijo que el json que me devuelve tenga los datos esperados, en mi caso es una orden de id 1 vacia ( sin productos y por consiguiente con precio total de la orden 0 )


if __name__ == '__main__':
    unittest.main()

