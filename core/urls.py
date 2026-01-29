from django.urls import path
from core.views import ChatApiView

urlpatterns = [
    path('chat/', ChatApiView.as_view()),
]
