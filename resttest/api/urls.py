from django.urls import include, path
from resthome.views import ClassPerson, LoginAPI, RegisterAPI, index, person, PersonViewSets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'person', PersonViewSets, basename='person')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index, name='index'),
    path('person/', person, name='person'),
    path('classperson/', ClassPerson.as_view(), name='classperson'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),

]