
from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name='home'),
    path('delete/<str:id>', views.delete_data,name='deldata'),
    path('update/<str:id>',views.update,name='update')
]
