from rest_framework.routers import SimpleRouter
from .views import SuppliersViewSet
from suppliers.apps import SuppliersConfig

app_name = SuppliersConfig.name
router = SimpleRouter()
router.register('', SuppliersViewSet)
urlpatterns = [] + router.urls
