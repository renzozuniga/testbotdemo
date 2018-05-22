from django.conf.urls import include, url
from .views import TestBotView

urlpatterns = [
				url(r'^647a1c507fbdee1dba3d68fbd8654b8127d5099531454a8055/?$', TestBotView.as_view())
			]