from django.test import TestCase
from django.urls import reverse
from .models import Stock
from .views import StockListView, StockCreateView

class StockModelTest(TestCase):
    def setUp(self):
        self.Stock = Stock.objects.create(
            name='Stock A',
            quantity=10,
            price=2.50,
            supplier='Supplier A'
        )

    def test_Stock_model(self):
        self.assertEqual(self.Stock.name, 'Stock A')
        self.assertEqual(self.Stock.quantity, 10)
        self.assertEqual(self.Stock.price, 2.50)
        self.assertEqual(self.Stock.supplier, 'Supplier A')
        self.assertIsNotNone(self.Stock.created)
        self.assertIsNotNone(self.Stock.updated)

class StockListViewTest(TestCase):
    def test_Stock_list_view(self):
        url = reverse('Stock_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
class StockCreateViewTest(TestCase):
    def test_Stock_create_view(self):
        url = reverse('Stock_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_Stock_create_form_submission(self):
        url = reverse('Stock_create')
        data = {
            'name': 'Stock B',
            'quantity': 5,
            'price': 3.00,
            'supplier': 'Supplier B'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)
        Stock = Stock.objects.first()
        self.assertEqual(Stock.name, 'Stock B')
        self.assertEqual(Stock.quantity, 5)
        self.assertEqual(Stock.price, 3.00)
        self.assertEqual(Stock.supplier, 'Supplier B')
