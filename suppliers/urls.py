from rest_framework.routers import SimpleRouter

from suppliers.apps import SuppliersConfig

from .views import SuppliersViewSet

app_name = SuppliersConfig.name
router = SimpleRouter()
router.register('', SuppliersViewSet)
urlpatterns = [] + router.urls
