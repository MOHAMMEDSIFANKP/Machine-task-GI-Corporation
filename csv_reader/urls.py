from django.urls import path
from . import views
urlpatterns = [
    path('', view = views.CsvUploadAPIView.as_view(), name = 'csv-uploader'),
    
]