from rest_framework.routers import DefaultRouter
from users.views import StudentViewSet
from .views import DirectionViewsSet, FacultyViewsSet, GroupViewsSet

router = DefaultRouter()
router.register('directions', DirectionViewsSet, basename='direction')
router.register('faculties', FacultyViewsSet)
router.register('groups', GroupViewsSet, basename='group')
router.register('students', StudentViewSet)

urlpatterns = router.urls






















