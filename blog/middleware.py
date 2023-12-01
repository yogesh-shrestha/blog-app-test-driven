from .models import Stats


class StatsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def os_stats(self, os_info):
        stats_object = Stats.objects.get(pk=1)

        if 'Windows' in os_info:
            stats_object.os_data['windows'] += 1
        elif 'Mac' in os_info:
            stats_object.os_data['mac'] += 1
        elif 'iPhone' in os_info:
            stats_object.os_data['iphone'] += 1
        elif 'Android' in os_info:
            stats_object.os_data['android'] += 1
        else:
            stats_object.os_data['others'] += 1

        stats_object.save()

        

    def __call__(self, request):

        if 'admin' not in request.path:
            self.os_stats(request.META.get('HTTP_USER_AGENT'))

        response = self.get_response(request)

        return response