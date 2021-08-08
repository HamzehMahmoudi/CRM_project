from django.http.response import JsonResponse
from sales.tasks import send_email_task
from django.shortcuts import render, redirect
from .models import FollowUp
from django.contrib.auth import decorators
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .tasks import send_email_task
from organization import models
from django.contrib import messages
from sales import forms

# Create your views here.


@decorators.login_required
@csrf_exempt
def email(request):  # send email to company
    qid = request.GET.get('qid')
    send_email_task.delay(request.user.pk, qid)
    return redirect('quotelist')


@decorators.login_required
def show_followup(request):
    orgid = request.GET.get("orgid")
    organ = models.Organization.objects.get(pk=orgid)
    qs = FollowUp.objects.filter(
        organization=organ, creator=request.user)
    followups = list(qs.values('creator__username',
                     'written_on__date', 'written_on__time', 'report'))
    return JsonResponse({"result": followups})


@ decorators.login_required
@ require_POST
@ csrf_exempt
def create_followup(request):
    organization = models.Organization.objects.get(
        pk=request.POST.get("organization"))
    form = forms.FollowUpForm(data=request.POST)
    if form.is_valid():
        form.save(commit=False).creator = request.user
        form.save(commit=False).organization = organization
        form.save()
        return JsonResponse(
            data={
                "success": True,
                "message": "follow up created "
            },
            status=201,
        )
    else:
        return JsonResponse(
            data={
                "success": False,
            },
            status=400,
        )
