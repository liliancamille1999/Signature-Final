from django.urls import path, include
from rest_framework import routers

from myx509.views import signer, DocumentList,DocList, verifList, PersonneList, \
    CaList, EntrepriseList, verifDetail  # PersonneList, DocList, CaList,EntrepriseList

router = routers.DefaultRouter()
router.register('personne', PersonneList)
router.register('cert', CaList)
router.register('entreprise', EntrepriseList)
router.register('document', DocumentList)

urlpatterns = [
    path('signer', signer, name="signer"),
    path('api-auth/', include('rest_framework.urls')),
    path('test/', include(router.urls)),
    path('test/verif/',verifList.as_view()),
    path('test/verif/<int:pk>/', verifDetail.as_view()),
    path('test/document/',DocList.as_view()),
]