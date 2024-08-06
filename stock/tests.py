from django.test import TestCase
from django.urls import reverse
from .models import Gas
from .views import GasListView, GasCreateView

class GasModelTest(TestCase):
    def setUp(self):
        self.gas = Gas.objects.create(
            name='Gas A',
            quantity=10,
            price=2.50,
            supplier='Supplier A'
        )

    def test_gas_model(self):
        self.assertEqual(self.gas.name, 'Gas A')
        self.assertEqual(self.gas.quantity, 10)
        self.assertEqual(self.gas.price, 2.50)
        self.assertEqual(self.gas.supplier, 'Supplier A')
        self.assertIsNotNone(self.gas.created)
        self.assertIsNotNone(self.gas.updated)

class GasListViewTest(TestCase):
    def test_gas_list_view(self):
        url = reverse('gas_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
class GasCreateViewTest(TestCase):
    def test_gas_create_view(self):
        url = reverse('gas_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_gas_create_form_submission(self):
        url = reverse('gas_create')
        data = {
            'name': 'Gas B',
            'quantity': 5,
            'price': 3.00,
            'supplier': 'Supplier B'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Gas.objects.count(), 1)
        gas = Gas.objects.first()
        self.assertEqual(gas.name, 'Gas B')
        self.assertEqual(gas.quantity, 5)
        self.assertEqual(gas.price, 3.00)
        self.assertEqual(gas.supplier, 'Supplier B')
