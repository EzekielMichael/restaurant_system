from django.urls import path
from . import views
from django.conf.urls import handler404

handler404 = 'Pages.views.custom_404_view'
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('order_history/', views.order_history, name="order_history"),
    path('create_order/', views.create_order, name="create_order"),
    path('change_password/', views.change_password, name='change_password'),

    path('view_orders/', views.view_orders, name='view_orders'),
    path('update_order_item_status/<int:order_item_id>/', views.update_order_item_status, name='update_order_item_status'),

    path('item_list/', views.item_list, name="item_list"),
    path('item_upload/', views.ItemsUpload, name="item_upload"),
    path('items/update/<int:item_id>/', views.update_item, name='update_item'),
    path('items/delete/<int:item_id>/', views.delete_item, name='delete_item'),
]