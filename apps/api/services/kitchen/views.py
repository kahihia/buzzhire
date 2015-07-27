from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import (JobRequestForFreelancerViewSet,
                          ServiceSpecificJobRequestForClientViewSet)
from apps.services.kitchen.models import KitchenFreelancer, KitchenJobRequest
from .serializers import (KitchenFreelancerForClientSerializer,
                          PrivateKitchenFreelancerSerializer,
                          KitchenJobRequestForFreelancerSerializer,
                          KitchenJobRequestForClientSerializer)


class KitchenFreelancerForClientViewSet(FreelancerForClientViewSet):
    """All published kitchen staff - publicly available information.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to kitchen staff:
        
    - `role`: The role of the freelancer.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = KitchenFreelancerForClientSerializer
    model_class = KitchenFreelancer


class OwnKitchenFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the kitchen staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to kitchen staff:
    
    - `role`: The role of the freelancer.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = PrivateKitchenFreelancerSerializer


class KitchenJobRequestForClientViewSet(ServiceSpecificJobRequestForClientViewSet):
    """Kitchen staff job requests for the currently logged in client.
    
    ## Fields
    
    The generic fields are documented on the job request
    endpoint for the client.
    
    These are the fields specific to kitchen staff job requests:
    
    - `role`: The role of the freelancer.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter 
    """
    serializer_class = KitchenJobRequestForClientSerializer
    model_class = KitchenJobRequest

class KitchenJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All kitchen staff job requests.  Publicly viewable information.
    
    ## Fields
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to kitchen staff job requests:
    
    - `role`: The role needed.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = KitchenJobRequestForFreelancerSerializer
    model_class = KitchenJobRequest