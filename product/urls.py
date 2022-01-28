from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('products/create/', views.snippet_list),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)