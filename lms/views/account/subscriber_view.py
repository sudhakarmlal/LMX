from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from lms.models.subscriber_model import Subscriber
from lms.forms.account.subscriber_form import SubscriberForm
import lmx.settings
import random
from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        try:
            sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
            sub.confirmed = False
            sub.is_subscribed = True
            sub.save()
        except IntegrityError:
            return render(request, 'account/subscriber.html', {'form': SubscriberForm()})
        try:
            subject="Newsletter Confirmation"
            message='Thank you for signing up for my email newsletter! \
                Please complete the process by \
                <a href="{}?email={}&conf_num={}"> clicking here to \
                confirm your registration</a>.'.format(request.build_absolute_uri('/account/subscribe_confirm'),
                                                    sub.email,
                                                    sub.conf_num)
            #email_from="reddypsusila9@gmail.com"
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[sub.email]
            send_mail( subject, message, email_from, recipient_list )

            return render(request, 'account/subscriber.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
        except:
            return render(request, 'account/subscriber.html', {'form': SubscriberForm()})
    else:
        return render(request, 'account/subscriber.html', {'form': SubscriberForm()})

    
def subscribe_confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.is_subscribed = True
        sub.save()
        return render(request, 'account/subscriber.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'account/subscriber.html', {'email': sub.email, 'action': 'denied'})

def like_post(request):
    post =get_object_or_404(Post,id=request.POST.get("post_id"))
    post.likes.add(request.user)
    return

def subscribe_delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = False
        sub.is_subscribed = False
        sub.delete()
        #sub.save()
        return render(request, 'account/unsubscriber.html', {'action': 'User Successfully Unsubscribed'})
    else:
        return render(request, 'account/unsubscriber.html', {'email': sub.email, 'action': 'denied'})

def sub_delete(request):
    if request.method == 'POST':
        try:
            #print("The email is",request.POST['email'])
            sub = Subscriber.objects.get(email=request.POST['email'])
            #print("The sub value is", sub.is_subscribed)
            #if sub.confirmed== False:
                #return render(request, 'account/unsubscriber.html', {'email': sub.email, 'action': 'The User  did not confirm Subscription'})
            if  sub.is_subscribed == False:
                print("The user has already unsubscribed")
                return render(request, 'account/unsubscriber.html', {'email': sub.email, 'action': 'Unsubscribe'})
            else:
                sub.confirmed = False
                sub.is_subscribed = False
                sub.save()
                subject="Unsubscribe Newsletter"
                message='News Letter Unsubscription! \
                    Please complete the process by \
                    <a href="{}?email={}&conf_num={}"> clicking here to \
                    unsubscribe</a>.'.format(request.build_absolute_uri('/account/subscribe_delete'),
                                                    sub.email,
                                                    sub.conf_num)
            #email_from="reddypsusila9@gmail.com"
                email_from=settings.EMAIL_HOST_USER
                recipient_list=[sub.email]
                send_mail( subject, message, email_from, recipient_list )
                #print(subject,message)
                return render(request, 'account/unsubscriber.html', {'email': sub.email, 'action': 'Unsubscribe', 'form': SubscriberForm()})
        except IntegrityError:
            return render(request, 'account/unsubscriber.html', {'form': SubscriberForm()})
        except:
            #print("User already unsubscribed")
            return render(request, 'account/unsubscriber.html', {'action': 'User already unsubscribed'})
        return render(request, 'account/unsubscriber.html', {'email': sub.email, 'action': 'Unsubscribed'})
    else:
        return render(request, 'account/unsubscriber.html', {'form': SubscriberForm()})

    #return render(request, 'account/unsubscriber.html',{'form': SubscriberForm()},{'email': sub.email, 'action': 'Unsubscribed'})