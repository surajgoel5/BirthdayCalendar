from django.urls import path,include
from . import views


urlpatterns = [
path('', views.index),
path('<int:dd>/<int:mm>/<int:yy>', views.flipcal,name="flipcal"),
path('allbdays/', views.allbdays,name="allbdays"),
path('export/', views.exportallbdays,name="export"),
path('import/', views.importallbdays,name="import")
]
