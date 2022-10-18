"""ics_innovation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ics_innovation import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.upload_page, name="home"),
    path("extracted_data/", views.get_extracted_data, name="review_page"),
    path("get_modal_details/", views.get_modal_details),
    path("latest_req/", views.get_latest_req),
    path("form/", views.get_form),
    path("get_document/", views.get_document_preview_file),
    path("preview/", views.get_preview),
    path("train_model/", views.train_model),
    path("model_status/", views.model_status),
    path("status_check/", views.status_check),
    path("submit_files/", views.upload_files_for_training_model),

    



]

urlpatterns = format_suffix_patterns(urlpatterns) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
