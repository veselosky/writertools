from datetime import datetime, timedelta
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project, ProjectStatus, StandardActivityChoices, WorkSession


time_message = _(
    "Note: If start time and end time are the same or blank, "
    "we take that to mean 'no specific time'. If you don't remember or don't care, "
    "just leave this field at the default."
)


class LogWorkForm(forms.ModelForm):
    """Accepts WorkSession details to create or update a session record."""

    class Meta:
        model = WorkSession
        fields = (
            "project",
            "activity",
            "wordcount",
            "duration",
            "startdate",
            "starttime",
            "enddate",
            "endtime",
        )

    activity = forms.ChoiceField(
        label=_("activity").title(),
        choices=StandardActivityChoices.choices,
        required=True,
        initial=StandardActivityChoices.DRAFTING,
    )
    wordcount = forms.IntegerField(
        label=_("word count").title(),
        required=False,
        max_value=999999,
        min_value=-99999,
    )
    duration = forms.IntegerField(
        label=_("duration").title(),
        required=False,
        min_value=0,
        max_value=999,
        help_text=_(
            "How long did you work (in minutes)? If you leave this blank, "
            "we'll calculate it from the start and end times (if available)."
        ),
    )
    startdate = forms.DateField(
        label=_("start date").title(),
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
    )
    starttime = forms.TimeField(
        label=_("start time").title(),
        required=False,
        widget=forms.TimeInput(attrs={"type": "time"}),
        help_text=_("What time did your session start? ") + time_message,
    )
    enddate = forms.DateField(
        label=_("end date").title(),
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    endtime = forms.TimeField(
        label=_("end time").title(),
        required=False,
        widget=forms.TimeInput(attrs={"type": "time"}),
        help_text=_("What time did your session end? ") + time_message,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = self.user.project_set.filter(
            status=ProjectStatus.IN_PROGRESS
        )

    def clean_duration(self):
        minutes = self.cleaned_data["duration"]
        if minutes:
            return str(timedelta(minutes=minutes))
        return None

    def clean(self):
        data = super().clean()
        # TODO: Attempt to calculate duration from start and end
        if not data["duration"]:
            startdate = data["startdate"]
            starttime = data["starttime"]
            enddate = data["enddate"]
            endtime = data["endtime"]
            if startdate and starttime and enddate and endtime and starttime != endtime:
                start = datetime.fromisoformat(f"{startdate}T{starttime}")
                end = datetime.fromisoformat(f"{enddate}T{endtime}")
                data["duration"] = str(end - start)
        return data
