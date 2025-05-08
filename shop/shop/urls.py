from django.conf import settings
from django.contrib import admin
from django.urls import path
from catalog import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.add_product, name='add_product'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:category_id>/products/', views.category_products, name='category_products'),
    path('categories/add/', views.add_category, name='add_category'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/<int:tag_id>/products/', views.tag_products, name='tag_products'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)