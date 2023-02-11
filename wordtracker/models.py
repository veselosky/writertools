from datetime import datetime, timedelta

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
            "Note: Only Works In Progress will be selectable in new work sessions."
        ),
    )
    desciption = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.name


class WorkSessionQuerySet(models.QuerySet):
    def user_summary_date_range(self, user, start: str, end: str):
        """Return summary statistics for the given date range and user. Note that
        the end date is exclusive, and the filter is based on the WorkSession
        statdate (because enddate is an optional field).

        {
            "sessions": 7,
            "wordcount": 4900,
            "duration": 25200
        }
        """
        stats = self.filter(
            user=user, startdate__gte=start, startdate__lt=end
        ).aggregate(
            sessions=models.Count("startdate"),
            wordcount=models.Sum("wordcount"),
            duration=models.Sum("duration"),
        )
        if stats["duration"]:
            stats["duration"] = int(stats["duration"].total_seconds())
        return stats

    def user_summary(self, user):
        """Return a data structure summarizing statistics for the user.

        The data include number of sessions, total wordcount, and total duration (in
        seconds). These data are provided for the following time periods: past 7 days,
        past 30 days, all time (all three periods *exclude* the current day).

            {
                'sevenday_sessions': 3,
                'sevenday_wordcount': 3144,
                'sevenday_duration': 6600,
                'thirtyday_sessions': 3,
                'thirtyday_wordcount': 3144,
                'thirtyday_duration': 6600,
                'all_sessions': 3,
                'all_wordcount': 3144,
                'all_duration': 6600
            }
        """
        # TODO: Cache user summary until end of calendar day
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=7)
        seven_days = models.Q(startdate__lt=today, startdate__gte=seven_days_ago)
        thirty_days_ago = today - timedelta(days=30)
        thirty_days = models.Q(startdate__lt=today, startdate__gte=thirty_days_ago)
        all = models.Q(startdate__lt=today)

        stats = self.filter(user=user).aggregate(
            sevenday_sessions=models.Count(
                "startdate",
                filter=seven_days,
            ),
            sevenday_wordcount=models.Sum(
                "wordcount",
                filter=seven_days,
            ),
            sevenday_duration=models.Sum(
                "duration",
                filter=seven_days,
            ),
            thirtyday_sessions=models.Count(
                "startdate",
                filter=thirty_days,
            ),
            thirtyday_wordcount=models.Sum(
                "wordcount",
                filter=thirty_days,
            ),
            thirtyday_duration=models.Sum(
                "duration",
                filter=thirty_days,
            ),
            all_sessions=models.Count("startdate", filter=all),
            all_wordcount=models.Sum("wordcount", filter=all),
            all_duration=models.Sum("duration", filter=all),
        )
        if stats["all_duration"]:
            stats["all_duration"] = int(stats["all_duration"].total_seconds())
        if stats["sevenday_duration"]:
            stats["sevenday_duration"] = int(stats["sevenday_duration"].total_seconds())
        if stats["thirtyday_duration"]:
            stats["thirtyday_duration"] = int(
                stats["thirtyday_duration"].total_seconds()
            )
        return stats


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

    class Meta:
        get_latest_by = ("startdate", "starttime")
        indexes = [models.Index(fields=("startdate", "starttime"), name="start_dt")]
        ordering = ("-startdate", "-starttime")

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

    objects = WorkSessionQuerySet.as_manager()

    class Meta:
        verbose_name = _("work session")
        verbose_name_plural = _("work sessions")

    def __str__(self):
        return f"{self.startdate.isoformat()} ({self.user.username})"
