from django.db import models


class Configuration(models.Model):
    fb_share_token = models.TextField(max_length=250)
    fb_share_app_id = models.TextField(max_length=20)
    fb_share_app_secret = models.TextField(max_length=35)
    fb_share_link = models.TextField(max_length=50)
