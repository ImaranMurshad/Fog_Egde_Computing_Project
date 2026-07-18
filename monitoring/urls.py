from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    path("api/alerts/", views.AlertCreateAPIView.as_view(), name="alert_api"),

    path("export/csv/", views.export_csv, name="export_csv"),
    
    path("export/pdf/", views.export_pdf, name="export_pdf"),
    
    path("reports/", views.reports, name="reports"),
    
    
    #path("api/alerts/", views.AlertCreateAPIView.as_view(), name="alert-api"),
    path("api/fog-health/", views.FogHealthCreateAPIView.as_view(), name="fog-health-api"),

]