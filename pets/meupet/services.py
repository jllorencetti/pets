from django.utils.timezone import timedelta

def get_unsolved_cases_perdiod_range(period_end):
    period_start = period_end - timedelta(days=90)
    return [period_start, period_end]