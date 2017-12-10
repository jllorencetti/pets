from .models import Pet


def pets_count(request):
    return {
        'pets_count': Pet.objects.count(),
    }
