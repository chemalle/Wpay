from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# Create your views here.


def home(request):
    return render(request, 'ecd/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('ecd/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your #wpay account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'ecd/acc_active_sent.html')
            #return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'ecd/thankyou.html')
    else:
        return HttpResponse('Activation link is invalid!')



from django.core.mail.message import EmailMessage
#from django.contrib.auth.models import User
from .forms import EmailPostForm


@login_required
def email(request):
    if request.method == 'POST':
            form = EmailPostForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                email = EmailMessage()
                email.subject = "Sua Escrituracao Contabil Digital ano 2017 chegou"
                email.body = 'O contratante esta ciente que deve agregar os demais dados de 2017 relacionados ao periodo fora de nosso escopo descrito no Distrato lido e devidamente pago em 2017 e que nao é de nossa responsabilidade fazer qualquer adequacao fora do que estiver expressamente descrito em Lei e no proprio distrato.'
                email.to = [cd['to']]
                email.attach_file("ecd/documents/SpedContabil-00991143000102_35229417301_2_20170101_20171231_G.txt") # Attach a file directly

                email.send()
                return render_to_response('ecd/thankyou2.html')

    else:
        form = EmailPostForm(request.POST)


    return render(request, 'ecd/share.html', context = {'form': form})



@login_required
def demonstrativos(request):
        if request.method == 'POST':
                form = EmailPostForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    email = EmailMessage()
                    email.subject = "Backup dos demonstrativos validados e Legislacao"
                    email.body = 'Seguem demonstrativos para compor a revisao do arquivo devidamente validado'
                    email.to = [cd['to']]
                    email.attach_file("ecd/documents/backup.zip") # Attach a file directly

                    email.send()
                    return render_to_response('ecd/thankyou2.html')

        else:
            form = EmailPostForm(request.POST)


        return render(request, 'ecd/share2.html', context = {'form': form})




@login_required
def distrato(request):
        if request.method == 'POST':
                form = EmailPostForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    email = EmailMessage()
                    email.subject = "Distrato seguindo normas CFC e CRC e alinhado com o disposto em nosso contrato original"
                    email.body = 'Copia do distrato enviado em 10-11-2017'
                    email.to = [cd['to']]
                    email.attach_file("ecd/documents/DISTRATO WPAY.doc") # Attach a file directly

                    email.send()
                    return render_to_response('ecd/thankyou2.html')

        else:
            form = EmailPostForm(request.POST)


        return render(request, 'ecd/share3.html', context = {'form': form})
