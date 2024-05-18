from accounts.models import UserProfile
from vendor.models import Vendor


def get_current_customer(request):
    try:
        customer = UserProfile.objects.get(user=request.user)
    except:
        customer = None
    return dict({'current_customer': customer})
