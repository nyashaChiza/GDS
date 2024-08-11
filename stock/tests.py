from django.test import TestCase
from django.urls import reverse
from accounts.models import Site, Company
from stock.models import Stock
from .views import StockListView, StockCreateView

class StockModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="test")
        self.site = Site.objects.create(name='test', company=self.company)
        self.Stock = Stock.objects.create(
            name='Stock A',
            quantity=10,
            site=self.site,
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
    def setUp(self):
        self.company = Company.objects.create(name="test")
        self.site = Site.objects.create(name='test', company=self.company)
        self.Stock = Stock.objects.create(
            name='Stock A',
            quantity=10,
            site=self.site,
            price=2.50,
            supplier='Supplier A'
        )
    def test_Stock_list_view(self):
        url = reverse('Stock_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
class StockCreateViewTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="test")
        self.site = Site.objects.create(name='test', company=self.company)
        self.stock = Stock.objects.create(
            name='Stock A',
            quantity=10,
            site=self.site,
            price=2.50,
            supplier='Supplier A'
        )
    def test_Stock_create_view(self):
        url = reverse('Stock_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_Stock_create_form_submission(self):
        url = reverse('Stock_create')
        
        data = {
            'site': self.site,
            'name': 'Stock B',
            'quantity': 5,
            'price': 3.00,
            'supplier': 'Supplier B'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.stock.name, 'Stock A')
        self.assertEqual(self.stock.quantity, 10)
        self.assertEqual(self.stock.price, 2.50)
        self.assertEqual(self.stock.supplier, 'Supplier A')
