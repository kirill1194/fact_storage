from .views import FactListViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'facts', FactListViewset, base_name="fact")

app_name = 'facts'

urlpatterns = router.urls