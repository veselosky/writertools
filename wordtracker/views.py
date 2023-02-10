import logging
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from .forms import LogWorkForm
from .models import Project, ProjectStatus, WorkSession

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "wordtracker/index.html"


class WorkSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkSession
    template_name = "wordtracker/log_work.html"
    form_class = LogWorkForm
    success_url = reverse_lazy("wordtracker:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        init = super().get_initial() or {}
        now = datetime.now()
        init["startdate"] = now.date()
        init["enddate"] = now.date()
        init["starttime"] = now.time().isoformat(timespec="minutes")
        init["endtime"] = now.time().isoformat(timespec="minutes")
        return init

    def form_valid(self, form):
        # Ensure the user who posted it is linked to it
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def session_timer(request, ws_id=None):
    """
    Displays the session timer page.

    The app sends a POST to this view to create a WorkSession. The view redirects to
    the URL of the session, now in progress. This allows users to refresh the session
    timer page without losing the context of their in-progress WorkSession.

    At the end of the session, the user will post the session data to `log_work` to be
    saved and permanently close out the WorkSession.
    """
    if request.method == "POST" and not ws_id:
        now = timezone.now()
        ws = WorkSession.objects.create(
            startdate=now.date(),
            starttime=now.time(),
            user=request.user,
        )
        return HttpResponseRedirect(
            reverse("wordtracker:session_timer", kwargs={"ws_id": ws.id})
        )
    elif not ws_id:
        # Send GET requests back to the start page to start a session
        return HttpResponseRedirect(reverse("wordtracker:dashboard"))

    ws = get_object_or_404(WorkSession.objects.filter(user=request.user), id=ws_id)
    return render(
        request, "wordtracker/session_timer.html", context={"worksession": ws}
    )


class WorkSessionListView(ListView):
    model = WorkSession
    template_name = "wordtracker/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_summary"] = WorkSession.objects.user_summary(self.request.user)
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@login_required
def view_stats(request):
    return render(request, "wordtracker/stats.html")
