from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login         
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AnxietyTriggerForm
from .models import AnxietyTrigger
from django.contrib.auth import logout 
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
import requests



def home(request):
    insights = None
    affirmation = None
    trend = None  # up / down / flat

    if request.user.is_authenticated:
        qs = AnxietyTrigger.objects.filter(user=request.user)

        # ---------- INSIGHTS ----------
        if qs.exists():
            today = timezone.now().date()

            # Last 7 days
            last_7_days = today - timedelta(days=7)
            this_week = qs.filter(date__gte=last_7_days)
            avg_this_week = this_week.aggregate(Avg("intensity"))["intensity__avg"]

            # Previous 7 days
            prev_7_start = last_7_days - timedelta(days=7)
            prev_week = qs.filter(date__gte=prev_7_start, date__lt=last_7_days)
            avg_prev_week = prev_week.aggregate(Avg("intensity"))["intensity__avg"]

            # Overall stats
            avg_intensity = qs.aggregate(Avg("intensity"))["intensity__avg"]
            high_intensity_count = qs.filter(intensity__gte=7).count()
            entries_last_7 = this_week.count()

            top_triggers = (
                qs.values("situation")
                .annotate(count=Count("id"))
                .order_by("-count")[:3]
            )

            # Trend logic: up, down, flat
            if avg_this_week is not None and avg_prev_week is not None:
                if avg_this_week > avg_prev_week + 0.5:
                    trend = "up"
                elif avg_this_week < avg_prev_week - 0.5:
                    trend = "down"
                else:
                    trend = "flat"

            insights = {
                "avg_intensity": round(avg_intensity, 1) if avg_intensity is not None else None,
                "high_intensity_count": high_intensity_count,
                "entries_last_7": entries_last_7,
                "top_triggers": top_triggers,
                "avg_this_week": round(avg_this_week, 1) if avg_this_week is not None else None,
                "avg_prev_week": round(avg_prev_week, 1) if avg_prev_week is not None else None,
            }

        # ---------- AFFIRMATION ----------
        try:
            resp = requests.get("https://www.affirmations.dev/", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                affirmation = data.get("affirmation")
        except Exception:
            affirmation = None

    context = {
        "insights": insights,
        "affirmation": affirmation,
        "trend": trend,
    }
    return render(request, "home.html", context)



def about(request):
    return render(request, "about.html")


def work_with_me(request):
    return render(request, "work_with_me.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in
            return redirect("noorforher:data_consent")  # 👈 go to consent page
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})



def tracker_list(request):
    triggers = AnxietyTrigger.objects.filter(user=request.user)
    return render(request, "tracker_list.html", {"triggers": triggers})


@login_required
def tracker_create(request):
    if request.method == "POST":
        form = AnxietyTriggerForm(request.POST)
        if form.is_valid():
            trigger = form.save(commit=False)
            trigger.user = request.user
            trigger.save()
            return redirect("noorforher:tracker_list")
    else:
        form = AnxietyTriggerForm()
    return render(request, "tracker_form.html", {"form": form})


@login_required
def tracker_update(request, pk):
    trigger = get_object_or_404(AnxietyTrigger, pk=pk, user=request.user)
    if request.method == "POST":
        form = AnxietyTriggerForm(request.POST, instance=trigger)
        if form.is_valid():
            form.save()
            return redirect("noorforher:tracker_list")
    else:
        form = AnxietyTriggerForm(instance=trigger)
    return render(request, "tracker_form.html", {"form": form, "update": True})

def logout_view(request):
    logout(request)  # logs the user out
    return redirect("noorforher:home")  # send them to home page

@login_required
def data_consent(request):
    if request.method == "POST":
        # check everything is ticked
        if (
            request.POST.get("agree_terms")
            and request.POST.get("agree_privacy")
            and request.POST.get("agree_health")
        ):
            # later you could store a flag on a Profile model here
            return redirect("noorforher:home")
        else:
            error = "Please agree to all items to continue."
            return render(request, "data_consent.html", {"error": error})

    return render(request, "data_consent.html")


def terms_of_use(request):
    return render(request, "terms_of_use.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")
