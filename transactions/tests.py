from django.test import TestCase
from django.utils import timezone
from .models import Transaction
from stock.models import Gas

class TransactionModelTest(TestCase):
    def setUp(self):
        self.gas = Gas.objects.create(name='Gas A', quantity=100,price=1.50)
        self.transaction = Transaction.objects.create(
            customer='John Doe',
            quantity=10,
            product=self.gas
        )

    def test_total_cost(self):
        expected_total_cost = self.transaction.quantity * self.transaction.product.price
        self.assertEqual(self.transaction.total_cost(), expected_total_cost)

    def test_stock_reduction_on_create(self):
        initial_quantity = self.gas.quantity
        new_transaction = Transaction.objects.create(
            customer='Jane Smith',
            quantity=20,
            product=self.gas
        )
        updated_quantity = self.gas.quantity
        self.assertEqual(updated_quantity, initial_quantity - new_transaction.quantity)

    def test_stock_reduction_on_update(self):
        initial_quantity = self.gas.quantity
        updated_quantity = 15
        self.transaction.quantity = updated_quantity
        self.transaction.save()
        self.gas.refresh_from_db()
        self.assertEqual(self.gas.quantity, initial_quantity - (updated_quantity - self.transaction.quantity))