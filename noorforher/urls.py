from django.urls import path
from . import views

app_name = "noorforher"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("work-with-me/", views.work_with_me, name="work_with_me"),

    path("register/", views.register, name="register"),

    path("tracker/", views.tracker_list, name="tracker_list"),
    path("tracker/add/", views.tracker_create, name="tracker_create"),
    path("tracker/<int:pk>/edit/", views.tracker_update, name="tracker_update"),
    path("logout/", views.logout_view, name="logout"),

    path("consent/", views.data_consent, name="data_consent"),
    path("terms-of-use/", views.terms_of_use, name="terms_of_use"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),

    path("consent/", views.data_consent, name="data_consent"),
    path("terms-of-use/", views.terms_of_use, name="terms_of_use"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
]
