from django.contrib.admin.apps import AdminConfig

class TSDAdminConfig(AdminConfig):
    default_site = 'Traffic_Situation_System.admin.TSDAdminSite'