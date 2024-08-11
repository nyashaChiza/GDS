from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.create_user, name='user_signup'),
    path('company/create/', views.create_company, name='create_company'),
    path('site/create/', views.create_site, name='create_site'),
    path('site/staff/create/<int:pk>', views.create_staff, name='create_staff_user'),
    path('site/details/<uuid:uuid>', views.SiteDetailView.as_view(), name='site_detail'),
    path('site/update/<uuid:uuid>', views.update_site, name='site_update'),
    path('sites/', views.SiteListView.as_view(), name='site_list'),
    path('search/', views.SiteSearchView.as_view(), name='site_search'),
    path('filter/', views.SiteStatusFilterView.as_view(), name='site_filter'),
   ]