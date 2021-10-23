from datasets.views import DatasetViewset
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from ml.views import AlgorithmDataViewset, ClusteringViewset
from rest_framework import permissions
from rest_framework_nested import routers

schema_view = get_schema_view(
    openapi.Info(
        title="Machine Learning API",
        default_version="v1",
        description="""
        #### How to start?
        1. Create your account through **_POST /auth/users_**.
        2. Activate your account by clicking link sent to your e-mail.
        3. Create your access token through **_POST /auth/jwt/create_**.
        4. Authorize yourself by clicking green button below. In value field paste your token as **_JWT \{token\}_**.
        5. Now you are ready to go!
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mathew28011@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.SimpleRouter()

router.register("datasets", DatasetViewset)
router.register("clusterings", ClusteringViewset)

algorithm_data_router = routers.NestedSimpleRouter(router, r"clusterings", lookup="clustering")
algorithm_data_router.register(r"algorithms", AlgorithmDataViewset, basename="clustering-algorithm_data")

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    ]
    + router.urls
    + algorithm_data_router.urls
)
