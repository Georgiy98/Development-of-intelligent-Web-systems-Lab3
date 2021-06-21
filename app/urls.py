from django.urls import path
import app.views as view

urlpatterns = [
    path('page/new/', view.handle_view_create, name="page_create"),
    path('page/<int:pk>/', view.handle_view_record, name="page_form"),
    path('page/', view.handle_view_list, name="page_list"),
]
