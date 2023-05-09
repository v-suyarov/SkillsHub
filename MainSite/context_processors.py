from django.conf import settings
from MainSite.models import CustomUser


def custom_user(request):
    return {'user': CustomUser.objects.get(id=request.user.id)} if request.user.is_authenticated else {}
