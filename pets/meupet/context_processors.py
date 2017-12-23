from .models import Kind, Pet


def pets_count(request):
    return {
        'pets_count': Pet.objects.count(),
    }


def kinds_count(request):
    return {
        'kind_lost': Kind.objects.lost_kinds(),
        'kind_adoption': Kind.objects.adoption_kinds(),
    }
