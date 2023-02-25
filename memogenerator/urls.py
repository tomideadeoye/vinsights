from django.urls import path
from memogenerator import views

urlpatterns = [
    path('dataconsumer', views.DataConsumer.as_view()),

]
