from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:item_id>/', views.item_json, name='item'),
    path('details/<int:item_id>/', views.item_details, name='item_details'),
    path('add/', views.add_item_view, name='add_item'),
    path('manager/<str:sortBy>/',views.manager_view, name="manager_view"),
    path('supervisor/add',views.create_department, name='create_department'),
    path('supervisor/',views.supervisor_view, name='supervisor_view')
]