from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.room_list, name="room_list"),
    path("new/", views.room_new, name="room_new"),
    path("<int:pk>/", views.room_detail, name="room_detail"),
    path("<int:room_pk>/messages/new/", views.message_new, name="message_new"),
    path("docs/law/tax/", views.TaxLawDocumentListView.as_view()),
]
