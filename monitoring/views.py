from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics

import csv
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

from django.utils.dateparse import parse_date
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import Alert, FogHealth
from .serializers import AlertSerializer, FogHealthSerializer


from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .tasks import save_alert_task, save_fog_health_task


# =====================================================
# REST API
# =====================================================

class AlertCreateAPIView(generics.ListCreateAPIView):
    queryset = Alert.objects.all().order_by("-created_at")
    serializer_class = AlertSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        save_alert_task.delay(serializer.validated_data)

        return Response(
            {"message": "Alert queued successfully"},
            status=status.HTTP_202_ACCEPTED,
        )


class FogHealthCreateAPIView(generics.CreateAPIView):
    queryset = FogHealth.objects.all()
    serializer_class = FogHealthSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        save_fog_health_task.delay(serializer.validated_data)

        return Response(
            {"message": "Fog Health queued successfully"},
            status=status.HTTP_202_ACCEPTED,
        )


# =====================================================
# Dashboard
# =====================================================

def dashboard(request):

    alerts = Alert.objects.all().order_by("-created_at")

    latest_health = FogHealth.objects.order_by("-created_at").first()

    context = {
        "alerts": alerts,

        "total_alerts": alerts.count(),
        "critical_alerts": alerts.filter(status="CRITICAL").count(),
        "high_alerts": alerts.filter(status="HIGH").count(),
        "medium_alerts": alerts.filter(status="MEDIUM").count(),

        "latest_health": latest_health,
    }

    return render(request, "dashboard/dashboard.html", context)


# =====================================================
# Export CSV
# =====================================================

def export_csv(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="ride_alerts.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Ride",
        "Sensor",
        "Value",
        "Status",
        "Message",
        "Time",
    ])

    alerts = Alert.objects.all().order_by("-created_at")

    for alert in alerts:
        writer.writerow([
            alert.ride_name,
            alert.sensor_name,
            alert.value,
            alert.status,
            alert.message,
            alert.created_at.strftime("%d-%m-%Y %H:%M:%S"),
        ])

    return response


# =====================================================
# Export PDF
# =====================================================

def export_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    data = [
        ["Ride", "Sensor", "Value", "Status", "Message", "Time"]
    ]

    alerts = Alert.objects.all().order_by("-created_at")

    for alert in alerts:
        data.append([
            alert.ride_name,
            alert.sensor_name,
            str(alert.value),
            alert.status,
            alert.message,
            alert.created_at.strftime("%d-%m-%Y %H:%M:%S"),
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    doc.build([table])

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ride_alerts.pdf"'
    response.write(pdf)

    return response


# =====================================================
# Reports
# =====================================================

def reports(request):

    alerts = Alert.objects.all().order_by("-created_at")

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if from_date:
        alerts = alerts.filter(created_at__date__gte=parse_date(from_date))

    if to_date:
        alerts = alerts.filter(created_at__date__lte=parse_date(to_date))

    # ---------------------------------
    # Alerts Trend
    # ---------------------------------

    alerts_per_day = (
        alerts
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    line_labels = []
    line_data = []

    for item in alerts_per_day:
        if item["day"]:
            line_labels.append(item["day"].strftime("%d %b"))
            line_data.append(item["total"])

    # ---------------------------------
    # Severity Distribution
    # ---------------------------------

    severity_labels = [
        "Critical",
        "High",
        "Medium"
    ]

    severity_data = [
        alerts.filter(status="CRITICAL").count(),
        alerts.filter(status="HIGH").count(),
        alerts.filter(status="MEDIUM").count(),
    ]

    # ---------------------------------
    # Alerts By Ride
    # ---------------------------------

    ride_counts = (
        alerts
        .values("ride_name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    ride_labels = []
    ride_data = []

    for item in ride_counts:
        ride_labels.append(item["ride_name"])
        ride_data.append(item["total"])

    # ---------------------------------
    # Analytics
    # ---------------------------------

    total_rides = alerts.values("ride_name").distinct().count()

    total_sensors = alerts.values("sensor_name").distinct().count()

    today = timezone.now().date()

    critical_today = alerts.filter(
        status="CRITICAL",
        created_at__date=today
    ).count()

    most_affected = (
        alerts.values("ride_name")
        .annotate(total=Count("id"))
        .order_by("-total")
        .first()
    )

    most_affected_ride = (
        most_affected["ride_name"]
        if most_affected
        else "N/A"
    )

    recent_critical = (
        alerts.filter(status="CRITICAL")
        .order_by("-created_at")[:5]
    )

    sensor_stats = (
        alerts.values("sensor_name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    top_rides = (
        alerts.values("ride_name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    latest_health = FogHealth.objects.order_by("-created_at").first()

    context = {

        "alerts": alerts,

        "top_rides": top_rides,

        "total_alerts": alerts.count(),
        "critical_alerts": alerts.filter(status="CRITICAL").count(),
        "high_alerts": alerts.filter(status="HIGH").count(),
        "medium_alerts": alerts.filter(status="MEDIUM").count(),

        "from_date": from_date,
        "to_date": to_date,

        "line_labels": line_labels,
        "line_data": line_data,

        "severity_labels": severity_labels,
        "severity_data": severity_data,

        "ride_labels": ride_labels,
        "ride_data": ride_data,

        "total_rides": total_rides,
        "total_sensors": total_sensors,
        "critical_today": critical_today,
        "most_affected_ride": most_affected_ride,
        "recent_critical": recent_critical,
        "sensor_stats": sensor_stats,

        "latest_health": latest_health,
    }

    return render(request, "reports/reports.html", context)