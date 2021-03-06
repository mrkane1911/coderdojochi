# -*- coding: utf-8 -*-

import os
import arrow

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from email.MIMEImage import MIMEImage

from coderdojochi.models import Mentor, Donation

from coderdojochi.views import sendSystemEmail

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received


@receiver(pre_save, sender=Mentor)
def avatar_updated_handler(sender, instance, **kwargs):

    try:
        original_mentor = Mentor.objects.get(id=instance.id)
    except ObjectDoesNotExist:
        return

    if not instance.avatar:
        return

    if original_mentor.avatar != instance.avatar:

        instance.avatar_approved = False

        context = {
            'first_name': instance.user.first_name,
            'last_name':instance.user.last_name,
            'image': 'avatar',
            'approve_url': instance.get_approve_avatar_url(),
            'reject_url': instance.get_reject_avatar_url(),
        }

        subject = u"{} {} | Mentor Avatar Changed".format(instance.user.first_name, instance.user.last_name)
        html_content = render_to_string("mentor-avatar-changed.html", context)
        text_content = render_to_string("mentor-avatar-changed.txt", context)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL]
        )

        msg.attach_alternative(html_content, "text/html")

        msg.mixed_subtype = 'related'

        img = MIMEImage(instance.avatar.read())
        img.add_header('Content-Id', 'avatar')
        img.add_header("Content-Disposition", "inline", filename="avatar")

        msg.attach(img)

        msg.send()


def donate_callback(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        donation = get_object_or_404(Donation, id=ipn_obj.invoice)
        donation.verified = True

        if not donation.receipt_sent:
            sendSystemEmail(
                False,
                'Thank you!',
                'coderdojochi-donation-receipt',
                {
                    'first_name': donation.first_name,
                    'last_name': donation.last_name,
                    'email': donation.email,
                    'amount': u'${}'.format(donation.amount),
                    'transaction_date': arrow.get(donation.created_at).format('MMMM D, YYYY h:ss a'),
                    'transaction_id': donation.id
                },
                donation.email,
                [v for k,v in settings.ADMINS]
            )

            donation.receipt_sent = True

        donation.save()


valid_ipn_received.connect(donate_callback)

