from django.urls import path

from wordtracker import views

app_name = "wordtracker"
urlpatterns = [
    path("log_work/", views.WorkSessionCreateView.as_view(), name="log_work"),
    path("stats/", views.view_stats, name="view_stats"),
    path("session/", views.session_timer, name="session_timer"),
    path("session/<int:ws_id>/", views.session_timer, name="session_timer"),
    path("", views.DashboardView.as_view(), name="dashboard"),
]
