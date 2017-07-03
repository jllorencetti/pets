from django.db import models

from common import utils


class CityQuerySet(models.QuerySet):
    def get_city(self, name):
        clean_name = utils.clear_text(name).lower()
        return self.filter(search_name=clean_name)
