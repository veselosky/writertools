from django.urls import path

from plotboard import views

app_name = "plotboard"
urlpatterns = [
    path("<int:pk>/", views.BoardDetailView.as_view(), name="board_detail"),
    path("create/", views.BoardCreateView.as_view(), name="board_create"),
    path("", views.BoardListView.as_view(), name="board_list"),
]
