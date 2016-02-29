from django.utils.timezone import timedelta, now


def get_date_3_months_ago(target_date=now()):
    return target_date - timedelta(days=90)