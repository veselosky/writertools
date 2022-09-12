from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", _("Work in progress")
    COMPLETED = "COMPLETED", _("Completed")
    ON_HOLD = "ON_HOLD", _("On hold")
    RETIRED = "RETIRED", _("Retired")


class StandardActivityChoices(models.TextChoices):
    """Choosable activities. This is NOT enforced in the model, just provided to the form.

    In future, the user may be able to customize the available activities.
    """

    DRAFTING = "drafting", _("drafting")
    EDITING = "editing", _("editing")
    OUTLINING = "outlining", _("outlining")
    RESEARCHING = "researching", _("researching")
    OTHER = "other", _("other")


class Project(models.Model):
    """
    Projects are a method of organizing work sessions. Their meaning is up to the user.

    Only projects with the IN_PROGRESS status will be offered for auto-complete in the
    session entry page. This will not prevent the user from logging sessions to other
    projects, but it gives them a way to clean up old stuff and keep the list tidy.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.PROTECT
    )
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"))
    status = models.CharField(
        _("status"),
        max_length=50,
        choices=ProjectStatus.choices,
        default=ProjectStatus.IN_PROGRESS,
        help_text=_(
            "Note: Only Works In Progress will be chooseable in new work sessions."
        ),
    )
    desciption = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.name


class WorkSession(models.Model):
    """
    A Work Session represents a (semi-)contiguous block of time spent working on a
    project.

    To allow for simple entry, and upload of Scrivener Writing History, only the
    startdate field is technically required (other than user). When loading Scrivener
    Writing History, enddate should be set to the value of startdate.

    Start and end times are stored in separate time fields, not as datetimes, to allow
    for easy time of day analysis. Duration is stored and reported separately to allow
    a Work Session to be paused briefly for breaks. This allows you to record
    interesting patterns like "worked for 45 minutes between 9 and 10".

    Although the primary intention of the app is to track word counts while drafting,
    users can set the `activity` field to anything they like. This allows one to track
    time spent on research, editing, etc.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.PROTECT
    )
    startdate = models.DateField(_("start date"), db_index=True)
    enddate = models.DateField(_("end date"), blank=True, null=True)
    starttime = models.TimeField(_("start time"), blank=True, null=True, db_index=True)
    endtime = models.TimeField(_("end time"), blank=True, null=True)
    duration = models.DurationField(_("duration"), blank=True, null=True)
    wordcount = models.IntegerField(_("word count"), blank=True, null=True)
    project = models.ForeignKey(
        "wordtracker.Project",
        verbose_name=_("project"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
        help_text=_("Don't worry, you can add a project later or change this value."),
    )
    activity = models.CharField(
        _("activity"), max_length=255, blank=True, db_index=True
    )

    class Meta:
        verbose_name = _("work session")
        verbose_name_plural = _("work sessions")

    def __str__(self):
        return f"{self.startdate.isoformat()} ({self.user.username})"
