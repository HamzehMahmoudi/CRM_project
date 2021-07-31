from django.http.response import JsonResponse
from sales.tasks import send_email_task
from django.shortcuts import render, redirect
from .models import FollowUp
from django.contrib.auth import decorators
from django.views.decorators.csrf import csrf_exempt
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
def add_follow_up(request, orgid):
    organ = models.Organization.objects.get(pk=orgid)
    if request.method == 'POST':
        form = forms.FollowUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.organization = organ
            instance.creator = request.user
            instance.save()
            return redirect('orgdetail', pk=orgid)
    else:
        form = forms.FollowUpForm()
        return render(request, 'sales/add_followup.html', {"form": form})


@decorators.login_required
def show_followup(request):
    orgid = request.GET.get("orgid")
    organ = models.Organization.objects.get(pk=orgid)
    followups = FollowUp.objects.filter(
        organization=organ, creator=request.user)
    return JsonResponse({"result": list(followups.values())})
