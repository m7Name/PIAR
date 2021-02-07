from django.contrib import admin
from django.conf import settings

from django.urls import path, include
from work.views import (
    home_screen_view,
    dashboard_view,
    working_pick_order,
    check_view,
    photo_view,    
)

admin.site.site_header = 'Piar test'                    # default: "Django Administration"
admin.site.index_title = 'Test zone'                 # default: "Site administration"
admin.site.site_title = 'HTML title from adminsitration' # default: "Django site admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_view, name="dashboard"),
    #path('gala/', dashboard_view, name="dashboard"),
    path('gallery/', photo_view, name="gallery"),
    path('check/', check_view, name="check"),
    path('', home_screen_view, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('order/<working_order>', working_pick_order, name='working_order'),        
]
