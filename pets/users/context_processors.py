from .models import OwnerProfile


def users_count(request):
    return {
        'users_count': OwnerProfile.objects.count()
    }
