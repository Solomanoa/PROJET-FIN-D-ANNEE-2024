from django.urls import path
from .views import get_evaluations, get_evaluation, create_evaluation, update_evaluation, delete_evaluation

urlpatterns = [
    path('evaluations/', get_evaluations, name='get_evaluations'),
    path('evaluations/<int:id>/', get_evaluation, name='get_evaluation'),
    path('evaluations/create/', create_evaluation, name='create_evaluation'),
    path('evaluations/update/<int:id>/', update_evaluation, name='update_evaluation'),
    path('evaluations/delete/<int:id>/', delete_evaluation, name='delete_evaluation'),
]
