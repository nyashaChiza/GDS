from transactions.models import Transaction
from stock.models import Gas
from accounts.models import Site, User
from datetime import datetime

class DashboardData:
    def __init__(self, user:User, date: datetime):
        self.date = date
        self.user = user
        
    def get_site_data(self):
        return self.user.site

    def get_sales_data(self):
        
        return {"current_month_total_sales": 678, "total_sales": 1000, "last_month_total_sales": 679, "week_total_sales": 67.45 , "total_sales_today":14.7}
    
    def get_stock_data(self):
        
        return {"current_month_total_sales_quantity": 340.3,"week_total_sales_quantity":29.4, "total_sales_quantity": 340.3,"last_month_total_sales_quantity": 340.3, "current_available_gas_quantity":Gas.objects.first().quantity, "total_gas_quantity_sold":1220, "total_requisitions":68 }
    
    def get_sales_plot_data(self):
        
        return {"monthly_average":345, "weekly_average":89.3, "daily_average":23.4, "plot_data":[]}
    
    def get_stock_sales_table_data(self):
        
        return Transaction.objects.filter().all()