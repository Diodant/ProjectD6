from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsDelete, NewsCreate, NewsUpdate

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
    path('search/', NewsSearch.as_view()),
    path('add/', NewsCreate.as_view(), name='create'),
    path('edit/<int:pk>', NewsUpdate.as_view(), name='update'),
    path('delete/<int:pk>', NewsDelete.as_view(), name='delete'),
]