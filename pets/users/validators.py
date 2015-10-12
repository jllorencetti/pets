from django.core.exceptions import ValidationError


def validate_facebook_url(value):
    msg = 'Por favor, insira uma URL válida do seu perfil no Facebook.'
    if 'www.facebook.com/' not in value and 'www.fb.com' not in value:
        raise ValidationError(msg)
