from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import PressureFrame


def _user_role(user):
    profile = getattr(user, "profile", None)
    return getattr(profile, "role", None)


def clinician_required(view_func):
    """
    Allow access only to clinicians and superusers.
    """

    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if request.user.is_superuser or _user_role(request.user) == "clinician":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")

    return _wrapped


def home_redirect(request):
    """
    Redirect root URL to the login page.
    """
    return redirect("login")


@login_required
def dashboard(request):
    """
    Authenticated dashboard view that renders the main UI with recent data.

    Clinicians and admins see all scans; other users see their own scans only.
    """
    role = _user_role(request.user)
    qs = PressureFrame.objects.select_related("user").order_by("-timestamp")
    if not request.user.is_superuser and role != "clinician":
        qs = qs.filter(user=request.user)

    frames = list(qs[:5])
    total_scans = qs.count()
    positive_cases = qs.filter(alert_flag=True).count()

    context = {
        "role": role,
        "frames": frames,
        "total_scans": total_scans,
        "positive_cases": positive_cases,
        "normal_results": max(total_scans - positive_cases, 0),
    }
    return render(request, "sensor_app/dashboard.html", context)


@login_required
def scan_list(request):
    """
    List scans for the current user.
    Clinicians/admins see all; others see their own.
    """
    role = _user_role(request.user)
    qs = PressureFrame.objects.select_related("user").order_by("-timestamp")
    if not request.user.is_superuser and role != "clinician":
        qs = qs.filter(user=request.user)

    return render(request, "sensor_app/scan_list.html", {"frames": qs})


@login_required
def scan_detail(request, pk):
    """
    Detail view for a single scan, enforcing ownership for non-clinicians.
    """
    frame = get_object_or_404(PressureFrame.objects.select_related("user"), pk=pk)
    role = _user_role(request.user)

    if not (
        request.user.is_superuser
        or role == "clinician"
        or frame.user_id == request.user.id
    ):
        raise Http404()

    return render(request, "sensor_app/scan_detail.html", {"frame": frame})


@clinician_required
def scan_create(request):
    """
    Simple clinician-only form to record a new PressureFrame.
    """
    error = None

    if request.method == "POST":
        try:
            # Minimal, assignment-level validation
            user = request.user
            peak_pressure = int(request.POST.get("peak_pressure", "0"))
            contact_area = float(request.POST.get("contact_area", "0") or 0)
            alert_flag = request.POST.get("alert_flag") == "on"

            PressureFrame.objects.create(
                user=user,
                timestamp=timezone.now(),
                matrix=[[peak_pressure]],
                peak_pressure=peak_pressure,
                contact_area=contact_area,
                alert_flag=alert_flag,
            )
            return redirect("scan_list")
        except (TypeError, ValueError):
            error = "Please provide valid numeric values."

    return render(request, "sensor_app/scan_create.html", {"error": error})

