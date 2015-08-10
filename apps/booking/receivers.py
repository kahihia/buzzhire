from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Booking
from apps.job.models import JobRequest
from .signals import (invitation_created, invitation_applied,
                      booking_created, invitation_declined)
from django_fsm.signals import post_transition
from apps.notification.models import Notification
from . import tasks


@receiver(post_transition)
def invite_matching_freelancers(sender, instance, name,
                                source, target, **kwargs):
    """Invites all freelancers who match the job request,
    when a new job request is opened."""
    if name == 'open' and issubclass(sender, JobRequest):
        tasks.invite_matching_freelancers(instance)


@receiver(invitation_applied)
def notify_freelancer_on_apply(sender, invitation, **kwargs):
    "Notifies the freelancer when they apply for a job."
    subject = 'You have now applied for %s' % \
                invitation.jobrequest.reference_number
    content = render_to_string(
        'booking/email/includes/freelancer_invitation_applied.html',
        {'object': invitation.jobrequest})
    send_mail(invitation.freelancer.user.email,
              subject,
              'email/base',
              {'title': 'We have received your application',
               'content': content},
              from_email=settings.BOOKINGS_FROM_EMAIL)

@receiver(booking_created)
def notify_freelancer_on_booking(sender, booking, **kwargs):
    "Notifies the freelancer when a booking is created."
    subject = 'Confirmation of booking for %s' % \
                booking.jobrequest.reference_number
    content = render_to_string(
        'booking/email/includes/freelancer_booking_confirmation.html',
        {'object': booking.jobrequest})
    send_mail(booking.freelancer.user.email,
              subject,
              'email/base',
              {'title': 'Confirmation of booking',
               'content': content},
              from_email=settings.BOOKINGS_FROM_EMAIL)


@receiver(invitation_declined)
def notify_freelancer_on_decline(sender, invitation, **kwargs):
    "Notifies the freelancer when their job application is declined."
    subject = 'Unsuccessful application for job for %s' % \
                invitation.jobrequest.reference_number
    content = render_to_string(
        'booking/email/includes/freelancer_invitation_declined.html',
        {'object': invitation.jobrequest})
    send_mail(invitation.freelancer.user.email,
              subject,
              'email/base',
              {'title': 'Your application was unsuccessful',
               'content': content},
              from_email=settings.BOOKINGS_FROM_EMAIL)


@receiver(invitation_applied)
def notify_admin_when_invitation_applied(sender, invitation, **kwargs):
    """Notifies the admin when a job request is applied for.
    """
    job_request = invitation.jobrequest

    if job_request.has_enough_applications:
        subject = 'Job request %s now has enough applications' % \
                job_request.reference_number

        content = render_to_string(
            'booking/email/includes/admin_enough_applications.html',
            {'object': job_request}
        )
    else:
        # Just the regular notification
        subject = 'New application for job request %s' % \
                job_request.reference_number

        content = render_to_string(
            'booking/email/includes/admin_invitation_applied.html',
            {'object': job_request,
             'freelancer': invitation.freelancer}
        )

    send_mail(settings.BOOKINGS_EMAIL,
                  subject,
                  'email/base',
                  {'title': subject,
                   'content': content})


@receiver(invitation_created)
def notify_freelancer_on_invitation(sender, invitation, **kwargs):
    "Notifies the freelancer when they are invited to book a job."
    title = 'A new job was just posted'
    content = render_to_string(
        'booking/email/includes/freelancer_invitation.html',
        {
            'object': invitation,
            'job_request': invitation.jobrequest
         }
    )
    send_mail(invitation.freelancer.user.email,
              title,
              'email/base',
              {'title': title,
               'content': content},
              from_email=settings.BOOKINGS_FROM_EMAIL)

    # Create notification
    Notification.objects.create(
            message='A new job was just posted.',
            category='freelancer_invitation',
            related_object=invitation.jobrequest,
            user=invitation.freelancer.user)

# @receiver(booking_created)
# def notify_client_on_booking(sender, booking, **kwargs):
#     "Notifies the client when a booking is created."
#     subject = 'Confirmation of booking %s' % booking.reference_number
#     content = render_to_string(
#         'booking/email/includes/client_booking_confirmation.html',
#         {
#             'object': booking,
#             'driverjobrequest': booking.jobrequest
#          }
#     )
#     send_mail(booking.jobrequest.client.user.email,
#               subject,
#               'email/base',
#               {'title': 'Your booking has been confirmed',
#                'content': content},
#               from_email=settings.BOOKINGS_EMAIL)

# @receiver(post_save, sender=Booking)
# def notify_client_on_booking(sender, instance, created, **kwargs):
#     "Notifies the client when a booking is created."
#     if created:
#         subject = 'Your driver has now been confirmed'
#         content = render_to_string(
#             'booking/email/includes/client_booking_confirmation.html',
#             {'object': instance})
#
#         send_mail(instance.jobrequest.client.user.email,
#                   subject,
#                   'email/base',
#                   {'title': subject,
#                    'content': content},
#                   from_email=settings.BOOKINGS_EMAIL)
