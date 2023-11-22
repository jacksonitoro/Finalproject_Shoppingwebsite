from django.urls import path
from . import views

app_name='davinshop'

urlpatterns = [
    path('', views.allProdCat, name='allProdCat'),
    path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),
    path('<slug:c_slug>/<product_slug>/', views.ProdCatDetails, name='ProdCatDetail'),
]