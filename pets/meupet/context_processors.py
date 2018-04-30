from .models import Kind, Pet, StatusGroup


def pets_count(request):
    return {
        'pets_count': Pet.objects.count(),
    }


def sidemenu(request):
    groups = list(StatusGroup.objects.order_by('name').all())

    menu_data = []

    for group in groups:
        menu_data.append({
            'name': group.name,
            'slug': group.slug,
            'menu_items': Kind.objects.count_pets((group.statuses.all())),
        })

    return {
        'sidemenu': menu_data
    }
