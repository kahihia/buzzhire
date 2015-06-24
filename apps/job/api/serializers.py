from django.forms import widgets
from rest_framework import serializers
from apps.api.serializers import MoneyField
from ..models import JobRequest


class JobRequestSerializer(serializers.ModelSerializer):
    client = serializers.HyperlinkedRelatedField(read_only=True,
                                            view_name='clients-detail')

    address = serializers.SerializerMethodField('_address')
    def _address(self, obj):
        return {
            'address1': obj.address1,
            'address2': obj.address2,
            'city': obj.get_city_display(),
            'postcode': str(obj.postcode),
        }

    client_pay_per_hour = MoneyField()
    freelancer_pay_per_hour = MoneyField()

    class Meta:
        model = JobRequest
        fields = ('id', 'reference_number', 'service',
                  'client', 'status',
                  'tips_included', 'date', 'start_time', 'duration',
                  'number_of_freelancers', 'address',
                  'phone_requirement', 'client_pay_per_hour',
                  'freelancer_pay_per_hour', 'years_experience', 'comments'
                  )
