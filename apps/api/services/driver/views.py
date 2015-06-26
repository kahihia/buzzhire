from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from ...job.views import JobRequestForFreelancerViewSet
from ...freelancer.permissions import FreelancerOnlyPermission
from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from .serializers import (DriverForClientSerializer,
                          PrivateDriverSerializer, VehicleTypeSerializer,
                    FlexibleVehicleTypeSerializer, DriverJobRequestForFreelancerSerializer,
                    DriverVehicleTypeSerializer)
from apps.services.driver.models import (VehicleType, FlexibleVehicleType, Driver,
                      DriverJobRequest, DriverVehicleType)
from .permissions import DriverOnlyPermission
from ...views import RetrieveAndUpdateViewset


class DriverForClientViewSet(FreelancerForClientViewSet):
    """All drivers that the currently logged in client can see.
    
    The generic fields are documented on the freelancer endpoint.
    
    ## Specific fields
    
    - `vehicles` List of vehicles that the driver has.
      See documentation on the 'Driver vehicles' endpoint for details.
    - `phone_type` What kind of phone they have.  Choices are:
        - `"AN"` - Android
        - `"IP"` - iPhone
        - `"WI"` - Windows
        - `"OT"` - Other smartphone
        - `"NS"` - Non smartphone       
    """
    serializer_class = DriverForClientSerializer

    def get_queryset(self):
        return Driver.published_objects.all()


class OwnDriverViewSet(OwnFreelancerViewSet):
    """Returns the driver's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    ## Specific fields
    - `phone_type` What kind of phone they have.  Choices are:
        - `"AN"` - Android
        - `"IP"` - iPhone
        - `"WI"` - Windows
        - `"OT"` - Other smartphone
        - `"NS"` - Non smartphone      
    """
    pass


class DriverJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All driver job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    - `flexible_vehicle_type`: The flexible vehicle type that would
      be appropriate for the job, or null if any vehicle would be appropriate.
    - `own_vehicle`: Whether the driver needs to supply their own vehicle.
    - `delivery_box_applicable`: Whether the minimum delivery box requirement
      is relevant. 
    - `minimum_delivery_box`: The minimum size of delivery box required (only
      relevant if `delivery_box_applicable` is `true`).  Integer.  Choices are:
        - `0` - None
        - `2` - Standard
        - `4` - Pizza
    - `phone_requirement` The kind of phone the freelancer needs to do the job.
      Choices are:
        - `"NR"` - No smart phone needed.
        - `"AY"` - Any smart phone.
        - `"AN"` - Android.
        - `"IP"` - iPhone.
        - `"WI"` - Windows.
    """
    serializer_class = DriverJobRequestForFreelancerSerializer

    def get_queryset(self):
        return DriverJobRequest.objects.all()


class VehicleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """All the vehicle types for the site.  Read only.
        
    ## Fields
    
    - `id` Unique id for the vehicle type.  Integer.
    - `name` Human-readable name of the vehicle type.
    - `delivery_box_applicable`: Whether it is applicable to this vehicle
      type to ask about a delivery box.
    """
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleType.objects.all()


class FlexibleVehicleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """All flexible vehicle types for the site.  Read only.
    
    These are vehicle types that can include more than one vehicle type,
    e.g. Motorcycle / Scooter.  They are used on job requests, where the
    vehicle requirements are less strict.

    ## Fields
    
    See the vehicle types endpoint for documentation.
    """
    serializer_class = FlexibleVehicleTypeSerializer

    def get_queryset(self):
        return FlexibleVehicleType.objects.all()


class DriverVehicleForDriverViewSet(viewsets.ModelViewSet):
    """All the vehicles belonging to the currently logged in driver
    (aka 'driver vehicles').
    
    ## Fields
    
    - `id` Unique id for the driver vehicle.  Read only.
    - `vehicle_type` The type of vehicle.  Read only.
    - `vehicle_type_name` The human readable name of the vehicle type.  Read only.
    - `own_vehicle` Whether the driver can provide the vehicle on a job.
    - `delivery_box` If applicable, the size of delivery box.  Integer. Choices:
        - `0` - None.
        - `2` - Standard.
        - `4` - Pizza.
    """
    serializer_class = DriverVehicleTypeSerializer

    permission_classes = (DriverOnlyPermission,)

    def get_queryset(self):
        return self.request.user.driver.drivervehicletype_set.all()
