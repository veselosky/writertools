from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView

from .models import Board, Sequence, Card


class QuickCreateBoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name", "owner"]
        widgets = {"name": forms.TextInput({"placeholder": _("name")})}


class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    template_name = "plotboard/board_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = QuickCreateBoardForm()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = "plotboard/board_detail.html"


class BoardCreateView(CreateView):
    model = Board
    fields = ["name", "description", "per_row", "owner"]
    template_name = "plotboard/board_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Force the owner to be the user submitting the request.
        # Django sets data to an immutable QueryDict, so we need to copy it.
        data = kwargs["data"].dict()
        data["owner"] = self.request.user
        kwargs["data"] = data
        print(f"KWARGS = {kwargs}")
        return kwargs
