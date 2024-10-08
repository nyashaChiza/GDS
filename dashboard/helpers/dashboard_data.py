from transactions.models import Transaction
from stock.models import Stock
from django.conf import settings
from accounts.models import Site, User
from requisition.models import Requisition
from datetime import datetime, timedelta
from django.db.models import Sum, F

class DashboardData:
    def __init__(self, user: User):
        self.user = user
        self.site = self.get_site_data()

    def get_site_data(self):
        """Returns the site associated with the user based on their role."""
        if self.user.role == "Operator":
            return self.user.operation_site
        elif self.user.role == "Manager":
            return self.user.managed_site
        return None

    def get_sales_data(self):
        """Returns a dictionary with sales data."""
        return {
            "current_month_total_sales": self.calculate_current_month_sales(),
            "total_sales": self.calculate_total_sales(),
            "last_month_total_sales": self.calculate_last_month_sales(),
            "week_total_sales": self.calculate_week_sales(),
            "total_sales_today": self.calculate_today_sales()
        }

    def calculate_current_month_sales(self):
        """Calculate total sales for the current month."""
        start_of_month = datetime.now().replace(day=1)
        # Calculate the total sales for the last month by summing quantity * unit_cost
        try:
            return Transaction.objects.filter(
                site=self.site,
                created__gte=start_of_month,
            ).aggregate(
                total_sales=Sum(F('quantity') * F('unit_cost'))
            )['total_sales'] * self.site.stock.first().price or 0.00
        except Exception as e:
            settings.LOGGER.error(e)
            return 0.00
        
    def calculate_total_sales(self):
        """Calculate total sales for today."""
        try:
            return Transaction.objects.filter(site=self.site).aggregate(
                total_sales=Sum(F('quantity') * F('unit_cost'))
            )['total_sales'] * self.site.stock.first().price or 0.00
        except Exception as e:
            settings.LOGGER.error(e)
            return 0.00
    def calculate_last_month_sales(self):
        """Calculate total sales for the last month."""
        start_of_last_month = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)
        end_of_last_month = datetime.now().replace(day=1) - timedelta(days=1)

        # Calculate the total sales for the last month by summing quantity * unit_cost
        return Transaction.objects.filter(
            site=self.site,
            created__gte=start_of_last_month,
            created__lte=end_of_last_month
        ).aggregate(
            total_sales=Sum(F('quantity') * F('unit_cost'))
        )['total_sales'] or 0.00

    def calculate_week_sales(self):
        """Calculate total sales for the current week."""
        start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())

        # Calculate the total sales for the current week by summing quantity * unit_cost
        try:
            return Transaction.objects.filter(
                site=self.site,
                created__gte=start_of_week
            ).aggregate(
                total_sales=Sum(F('quantity') * F('unit_cost'))
            )['total_sales'] * self.site.stock.first().price or 0.00
        except Exception as e:
            settings.LOGGER.error(e)
            return 0.00
        
    def calculate_today_sales(self):
        """Calculate total sales for today."""
        today = datetime.now().date()
        try:
            return Transaction.objects.filter(site=self.site, created__date=today).aggregate(
                total_sales=Sum(F('quantity') * F('unit_cost'))
            )['total_sales'] * self.site.stock.first().price or 0.00
        except Exception as e:
            settings.LOGGER.error(e)
            return 0.00

    def get_stock_data(self):
        """Returns a dictionary with stock data."""
        return {
            "current_month_total_sales_quantity": self.calculate_current_month_sales_quantity(),
            "week_total_sales_quantity": self.calculate_week_sales_quantity(),
            "total_sales_quantity": self.calculate_total_sales_quantity(),
            "last_month_total_sales_quantity": self.calculate_last_month_sales_quantity(),
            "current_available_stock_quantity": self.calculate_current_available_stock_quantity(),
            "total_stock_quantity_sold": self.calculate_total_stock_quantity_sold(),
            "total_requisitions": self.calculate_total_requisitions()
        }

    def calculate_current_month_sales_quantity(self):
        """Calculate total quantity of items sold in the current month."""
        start_of_month = datetime.now().replace(day=1)
        return Transaction.objects.filter(site=self.site, created__gte=start_of_month).aggregate(Sum('quantity'))['quantity__sum'] or 0

    def calculate_week_sales_quantity(self):
        """Calculate total quantity of items sold in the current week."""
        start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
        return Transaction.objects.filter(site=self.site, created__gte=start_of_week).aggregate(Sum('quantity'))['quantity__sum'] or 0
    def calculate_total_sales_quantity(self):
        """Calculate total quantity of items sold for the site."""
        return Transaction.objects.filter(site=self.site).aggregate(Sum('quantity'))['quantity__sum'] or 0

    def calculate_last_month_sales_quantity(self):
        """Calculate total quantity of items sold in the last month."""
        start_of_last_month = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)
        end_of_last_month = datetime.now().replace(day=1) - timedelta(days=1)
        return Transaction.objects.filter(site=self.site, created__gte=start_of_last_month, created__lte=end_of_last_month).aggregate(Sum('quantity'))['quantity__sum'] or 0

    def calculate_current_available_stock_quantity(self):
        """Calculate current available stock quantity."""
        return Stock.objects.filter(site=self.site).aggregate(Sum('quantity'))['quantity__sum'] or 0

    def calculate_total_stock_quantity_sold(self):
        """Calculate total quantity of stock sold."""
        return self.calculate_total_sales_quantity()

    def calculate_total_requisitions(self):
        """Calculate total number of requisitions."""
        # Assuming `requisitions` is a related field in `Transaction` or a similar model
        return Requisition.objects.filter(site=self.site).count()

    def get_sales_plot_data(self):
        """Returns a dictionary with data for plotting sales."""
        return {
            "monthly_average": self.calculate_monthly_average(),
            "weekly_average": self.calculate_weekly_average(),
            "daily_average": self.calculate_daily_average(),
            "plot_data": self.calculate_plot_data()
        }

    def calculate_monthly_average(self):
        """Calculate the average monthly sales."""
        return self.calculate_total_sales() / 12  # Simplified; adjust as needed

    def calculate_weekly_average(self):
        """Calculate the average weekly sales."""
        return self.calculate_total_sales() / 52  # Simplified; adjust as needed

    def calculate_daily_average(self):
        """Calculate the average daily sales."""
        return self.calculate_total_sales() / 365  # Simplified; adjust as needed

    def calculate_plot_data(self):
        """Generate plot data."""
        # Implement the actual logic to generate plot data based on your requirements
        return []

    def get_stock_sales_table_data(self):
        """Returns a queryset of all transactions for the user's site."""
        if self.site:
            return Transaction.objects.filter(site=self.site).order_by('-created')[:6]
        return Transaction.objects.none()  # Return an empty queryset if no site is assigned


    def get_all_sites_monthly_sales(self):
        return {}
    
    
    def get_all_sites_remaining_stock(self):
        data = []
        sites = self.user.company.sites.all()
    
        for site in sites:
            remaining_stock = Stock.objects.filter(site=site).aggregate(Sum('quantity'))['quantity__sum'] or 0
            data.append({'site':site, 'remaining_stock':f"{remaining_stock}/{site.capacity}", 'remaining_stock_percentage':round(remaining_stock/site.capacity*100)})
        return data
    
    
    def get_all_sites_sales_bar_graph_totals(self):
        return {}
    
    def get_all_site_sales_line_graph_monthly_totals(self):
        return {}
    def get_company_data(self):
        total_sales = 0
        sites = self.user.company.sites.all()
        for site in sites:
            total_sales += Transaction.objects.filter(site=site).aggregate(
                total_sales=Sum(F('quantity') * F('unit_cost'))
            )['total_sales'] * site.stock.first().price or 0
        
        return {
            'company': self.user.company,
            'capacity': sum(site.capacity for site in self.user.company.sites.all()),
            'total_sales': total_sales,
            'monthly_average':total_sales / 12,
            'weekly_average':total_sales / 52,
            'daily_average':total_sales / 365,
        }


    def get_company_site_stats(self):
        sites = self.user.company.sites.all()
        data = []
        total_quantity = 0
        for site in sites:
                total_quantity += Transaction.objects.filter(site=site).aggregate(
                    total_quantity=Sum(F('quantity') * F('unit_cost'))
                )['total_quantity'] 
                data.append({'site':site, 'total_requisitions':site.requisitions.all().count(),'total_sales':total_quantity* site.stock.first().price or 0, 'total_quantity':total_quantity })
        return data