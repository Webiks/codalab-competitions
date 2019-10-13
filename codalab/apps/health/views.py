import json
from collections import OrderedDict
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Prefetch, Avg, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from apps.web.models import CompetitionSubmission
from .models import HealthSettings, TaskMetadata, Worker, WorkerStateChange
from apps.jobs.models import Job


def get_health_metrics():
    """
    Function that get health metrics based on the amouunt of jobs.

    :return: jobs dictionary
    -------
    - **Jobs pending** - Jobs pending queryset.
    - **Jobs pending count** - Length of pending jobs.
    - **Jobs finished in the last two days** - Jobs processed in the last two days.
    - **Jobs lasting longer than 10 minutes** - Jobs that are running for more than 30 minutes.
    - **Jobs failed** - Jobs that failed
    - **Jobs failed count** - Amount of jobs failed.
    - **alert emails** Email to send alert.
    - **alert_threshold** Threshold number.
    """
    jobs_pending = Job.objects.filter(status=Job.PENDING)

    jobs_finished_in_last_2_days = Job.objects.filter(status=Job.FINISHED, created__gt=datetime.now() - timedelta(days=2))
    jobs_finished_in_last_2_days_count = len(jobs_finished_in_last_2_days)
    jobs_finished_in_last_2_days_total_time_in_seconds = 0
    jobs_finished_in_last_2_days_avg = 0.0

    for job in jobs_finished_in_last_2_days:
        jobs_finished_in_last_2_days_total_time_in_seconds += (job.updated - job.created).seconds

    if jobs_finished_in_last_2_days_total_time_in_seconds > 0:
        jobs_finished_in_last_2_days_avg = jobs_finished_in_last_2_days_total_time_in_seconds / jobs_finished_in_last_2_days_count

    jobs_lasting_longer_than_10_minutes = []

    for job in jobs_pending:
        if (job.updated - job.created) > timedelta(minutes=10):
            jobs_lasting_longer_than_10_minutes.append(job)

    jobs_failed = Job.objects.filter(status=Job.FAILED).order_by("-updated")[:10]

    health_settings = HealthSettings.objects.get_or_create(pk=1)[0]

    alert_emails = health_settings.emails if health_settings.emails else ""

    context = {
        "jobs_pending": jobs_pending,
        "jobs_pending_count": len(jobs_pending),
        "jobs_finished_in_last_2_days_avg": jobs_finished_in_last_2_days_avg,
        "jobs_lasting_longer_than_10_minutes": jobs_lasting_longer_than_10_minutes,
        "jobs_failed": jobs_failed,
        "jobs_failed_count": len(jobs_failed),
        "alert_emails": alert_emails,
        "alert_threshold": health_settings.threshold,
        "congestion_threshold": health_settings.congestion_threshold
    }

    # Health page update Dec 22, 2017

    # Today's jobs
    jobs_today = Job.objects.filter(created__year=datetime.today().year,
                                    created__day=datetime.today().day,
                                    created__month=datetime.today().month)
    jobs_today_failed = jobs_today.filter(status=Job.FAILED)
    jobs_today_finished = jobs_today.filter(status=Job.FINISHED)
    jobs_today_pending = jobs_today.filter(status=Job.PENDING)

    jobs_last_fifty = Job.objects.all().order_by('-created')[0:50]
    jobs_last_fifty_updated = Job.objects.all().order_by('-updated')[0:50]
    jobs_last_fifty_failed = Job.objects.filter(status=Job.FAILED).order_by('-updated')[0:50]

    jobs_pending_stuck = Job.objects.filter(status=Job.PENDING, created__lt=datetime.now() + timedelta(days=1)).order_by('-updated')[0:100]
    jobs_running_stuck = Job.objects.filter(status=Job.RUNNING, created__lt=datetime.now() + timedelta(days=1)).order_by('-updated')[0:100]

    context['jobs_today'] = jobs_today
    context['jobs_today_count'] = len(jobs_today)
    context['jobs_today_failed'] = jobs_today_failed
    context['jobs_today_failed_count'] = len(jobs_today_failed)
    context['jobs_today_finished'] = jobs_today_finished
    context['jobs_today_finished_count'] = len(jobs_today_finished)
    context['jobs_today_pending'] = jobs_today_pending
    context['jobs_today_pending_count'] = len(jobs_today_pending)

    context['jobs_last_fifty'] = jobs_last_fifty
    context['jobs_last_fifty_updated'] = jobs_last_fifty_updated
    context['jobs_last_fifty_failed'] = jobs_last_fifty_failed
    context['jobs_pending_stuck'] = jobs_pending_stuck
    context['jobs_pending_stuck_count'] = len(jobs_pending_stuck)
    context['jobs_running_stuck'] = jobs_running_stuck
    context['jobs_running_stuck_count'] = len(jobs_running_stuck)
    context['jobs_all_stuck_count'] = len(jobs_running_stuck) + len(jobs_pending_stuck)

    return context


@login_required
def health(request):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    return render(request, "health/health.html", get_health_metrics())


@login_required
def simple_health(request):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    qs = CompetitionSubmission.objects.all()
    qs = qs.order_by('-submitted_at')
    qs = qs.select_related('phase__competition')
    qs = qs.select_related('phase__competition__queue')
    qs = qs.select_related('participant__user')
    qs = qs.prefetch_related('phase', 'status', 'participant')
    return render(request, "health/simple_health.html", {
        "submissions": qs[:250],
    })


@login_required
def email_settings(request):
    if not request.user.is_staff or request.method != "POST":
        return HttpResponse(status=404)
    health_settings = HealthSettings.objects.get_or_create(pk=1)[0]
    health_settings.emails = request.POST.get("emails")
    health_settings.threshold = request.POST.get("alert_threshold")
    health_settings.congestion_threshold = request.POST.get("congestion_threshold")
    health_settings.save()
    return HttpResponse()


def check_thresholds(request):
    """
    Function that checks if the amount of pending jobs is greater than threshold number.
    It will send an email if the number exceeded.
    """
    metrics = get_health_metrics()
    health_settings = HealthSettings.objects.get_or_create(pk=1)[0]
    email_string = health_settings.emails
    if email_string:
        emails = [s.strip() for s in email_string.split(",")]

        if metrics["jobs_pending_count"] > health_settings.threshold:
            send_mail(
                "Codalab Warning: Jobs pending > %s!" % health_settings.threshold,
                "There are > %s jobs pending for processing right now" % health_settings.threshold,
                settings.DEFAULT_FROM_EMAIL,
                emails
            )

        if metrics["jobs_lasting_longer_than_10_minutes"] and len(metrics["jobs_lasting_longer_than_10_minutes"]) > 10:
            send_mail("Codalab Warning: Many jobs taking > 10 minutes!", "There are many jobs taking longer than 10 minutes to process", settings.DEFAULT_FROM_EMAIL, emails)

    return HttpResponse()


def _task_metadata_stats(start, end, worker_context):
    # If start and end are the "current time" then get current state of workers
    if now() < end:
        for worker in Worker.objects.all():
            worker_context[worker.id] = worker.is_active

    # Get any changes for worker state during this time period
    worker_state_changes = WorkerStateChange.objects.filter(timestamp__range=(start, end)).distinct('worker').order_by('worker', '-timestamp')
    for state_change in worker_state_changes:
        # latest change should stick here
        worker_context[state_change.worker_id] = state_change.up

    return {
        # Started within this interval
        "arrived": TaskMetadata.objects.filter(queued__range=(start, end)).count(),

        # Finished within this interval
        "serviced": TaskMetadata.objects.filter(start__range=(start, end), end__range=(start, end)).count(),

        # Jobs waiting to be picked up by a worker
        "queued": TaskMetadata.objects.filter(worker__isnull=True, queued__range=(start, end)).count(),

        # Average time of jobs finished during this hour
        "average_execution_time": TaskMetadata.objects.filter(end__range=(start, end)).aggregate(
            average_execution_time=Avg(F('end') - F('start'))
        )['average_execution_time'],

        # Average time waiting to get picked up by a worker
        "average_queued_time": TaskMetadata.objects.filter(queued__range=(start, end), start__isnull=False).aggregate(
            average_queued_time=Avg(F('start') - F('queued'))
        )['average_queued_time'],

        # Workers active (`up`)
        "workers_active": sum([is_active for id, is_active in worker_context.items()]),

        # Workers that actually did a job
        "workers_doing_jobs": Worker.objects.filter(tasks__start__range=(start, end)).distinct('pk').count()
    }


@login_required
def worker_list(request):
    if not request.user.is_staff:
        return HttpResponse(status=404)

    workers = Worker.objects.all().prefetch_related(
        # Get all tasks that haven't ended
        Prefetch('tasks', queryset=TaskMetadata.objects.filter(end=None, failed_to_complete=False), to_attr='current_tasks')
    )

    stats = OrderedDict()
    worker_context = {w.id: w.is_active for w in Worker.objects.all()}
    hour_on_the_dot = now().replace(minute=0, second=0, microsecond=0)
    hours_to_look_back = 10

    stats["5day-1day"] = _task_metadata_stats(
        now() - timedelta(days=5),
        now() - timedelta(days=1),
        worker_context
    )
    last_day_end_timestamp = hour_on_the_dot - timedelta(hours=hours_to_look_back - 1)
    stats["1day-{}".format(last_day_end_timestamp.strftime('%H:%M:%S'))] = _task_metadata_stats(
        now() - timedelta(days=1),
        last_day_end_timestamp,
        worker_context
    )

    for offset in reversed(range(hours_to_look_back)):
        start = hour_on_the_dot - timedelta(hours=offset)
        end = hour_on_the_dot.replace(minute=59, second=59, microsecond=999) - timedelta(hours=offset)

        range_string = "{} - {}".format(start.strftime('%H:%M:%S'), end.strftime('%H:%M:%S'))
        stats[range_string] = _task_metadata_stats(start, end, worker_context)

    return render(request, "health/worker_list.html", {
        "workers": workers,
        "stats": stats
    })


@login_required
def worker_detail(request, worker_pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)

    qs = Worker.objects.prefetch_related(
        Prefetch('tasks', queryset=TaskMetadata.objects.order_by('-start')),
        'tasks__submission',
    )
    worker = get_object_or_404(qs, pk=worker_pk)

    return render(request, "health/worker_detail.html", {
        "worker": worker,
        "task_history": worker.tasks.all()[:100],
    })
