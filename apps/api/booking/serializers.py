from django.forms import widgets
from rest_framework import serializers
from apps.booking.models import Booking, Invitation
from ..job import serializers as job_serializers
from ..freelancer.serializers import SpecificFreelancerIdentityField


class BookingOrInvitationSerializer(serializers.ModelSerializer):
    "Serializer for Bookings or Invitations, for freelancers."
    job_request = serializers.HyperlinkedRelatedField(read_only=True,
                            view_name='job_requests_for_freelancer-detail',
                            source='jobrequest')

    job_request_full = \
            job_serializers.PolymorphicJobRequestForFreelancerSerializer(
                                                        source='jobrequest',
                                                        read_only=True)

    class Meta:
        fields = ('id', 'reference_number',
                  'job_request', 'date_created',
                  'job_request_full')

class BookingSerializer(BookingOrInvitationSerializer):
    class Meta(BookingOrInvitationSerializer.Meta):
        model = Booking



class InvitationSerializer(BookingOrInvitationSerializer):
    class Meta(BookingOrInvitationSerializer.Meta):
        model = Invitation


class BookingForClientSerializer(serializers.ModelSerializer):
    "Serializer for a booking attached to a job request viewed by a client."

    freelancer = serializers.HyperlinkedRelatedField(
                                    view_name='freelancers_for_client-detail',
                                    read_only=True)


    class Meta:
        model = Booking
        fields = ('id', 'reference_number', 'freelancer', 'date_created')


class BookingsJobRequestForClientSerializer(
                                job_serializers.JobRequestForClientSerializer):
    """Serializer for job requests for client, including bookings."""

    bookings = BookingForClientSerializer(many=True, read_only=True)

    class Meta(job_serializers.JobRequestForClientSerializer.Meta):
        fields = job_serializers.JobRequestForClientSerializer.Meta.fields + (
                        'bookings',)
