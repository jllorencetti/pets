def add_facebook_link(strategy, details, user=None, backend=None, is_new=None, *args, **kwargs):
    if is_new and backend.name == 'facebook':
        user.facebook = 'http://www.facebook.com/{}'.format(kwargs['uid'])
        user.save()
