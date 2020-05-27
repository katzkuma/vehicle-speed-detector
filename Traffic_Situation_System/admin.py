from django.contrib import admin
from django.contrib.auth.models import User
from website.models import Camera, TrafficRecord, URLPathByBrand
from website.admin import CameraAdmin
from django.template.response import TemplateResponse
from vehicle_detector.views import vehicle_detector


class TSDAdminSite(admin.AdminSite):
    index_template = 'admin/index.html'


    def index(self, request, extra_context=None):
        """
        Override it from AdminSite
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = super().get_app_list(request)
        detector_stopped = vehicle_detector.stopped

        context = {
            **self.each_context(request),
            'title': super().index_title,
            'app_list': app_list,
            **(extra_context or {}),
            'detector_stopped': detector_stopped
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/index.html', context)

tsd_admin_site = TSDAdminSite()
tsd_admin_site.register(Camera, CameraAdmin)
tsd_admin_site.register(TrafficRecord)
tsd_admin_site.register(URLPathByBrand)
tsd_admin_site.register(User)

# change title on admin pages
tsd_admin_site.site_header = 'Administration for Traffic Situation System'