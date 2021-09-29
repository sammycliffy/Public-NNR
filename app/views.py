from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash

# def index(request):
#      return render(request, 'app/index.html',)


class SignUp_View(View):
    form_class = SignUpForm
    initial = {'key': 'value'}
    template_name = 'app/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form_valid = form.is_valid()
        if form_valid:
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.is_active = True
            user.save()
            login(request, user)

            return redirect('dashboard')
        return render(request, self.template_name, {'form': form, })


class SourceForm_View(View):
    form_class = RadioActiveSourcesForm
    initial = {'key': 'value'}
    template_name = 'app/add_source.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form_valid = form.is_valid()
        if form_valid:
            fs = form.save(commit=False)
            fs.user = request.user
            fs.save()
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form, })


@login_required
def dashboard(request):
    sources = RadioActiveSourcesModel.objects.filter(user=request.user)
    paginator = Paginator(sources, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'page_obj': page_obj,
    }
    return render(request, 'app/dashboard.html', data)


@login_required
def delete(request, pk=None):
    delete = RadioActiveSourcesModel.objects.filter(pk=pk).delete()
    if (delete):
        return redirect('dashboard')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, _(
                'Your profile was successfully updated!'))
            return redirect('dashboard')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = SignUpForm(instance=request.user)
    return render(request, 'app/update_profile.html', {
        'user_form': user_form,
    })


@login_required
def contact(request):
    if request.method == 'POST':
        message = request.POST.get('message', None)
        print(message)
        Message.objects.create(
            user=request.user,
            message=message
        )
        sendEmail = send_mail(
            'Sent email from {} - {}'.format(request.user.contactPerson,
                                             request.user.contactPhone),
            'Here is the feedback. {}'.format(message),
            request.user.email,
            ['support@gigazone.com.ng'],
            fail_silently=False,
        )
        if(sendEmail):
            messages.success(request, 'sent successfully.')

    return render(request, 'app/contact.html')
