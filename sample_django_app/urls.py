from django.urls import path
from .views import PlanViewSet, PackViewSet

urlpatterns = [
    path("plan/", PlanViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "plan/",
        PlanViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    path(
        "plan/<int:pk>/",
        PlanViewSet.as_view({"delete": "destroy", "patch": "partial_update"}),
    ),
    path(
        "plan/<int:pk>/subscribe/",
        PlanViewSet.as_view(
            {
                "get": "subscribe_user",
            }
        ),
    ),
    path(
        "plan/cancel/subscribe/",
        PlanViewSet.as_view(
            {
                "get": "cancel_subscription",
            }
        ),
    ),
    path(
        "plan/current/",
        PlanViewSet.as_view(
            {
                "get": "current_plan",
            }
        ),
    ),
    path("pack/", PackViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "pack/",
        PackViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    path(
        "pack/<int:pk>/buy/",
        PackViewSet.as_view(
            {
                "get": "buy_pack",
            }
        ),
    ),
    path(
        "pack/<int:pk>/",
        PackViewSet.as_view({"patch": "partial_update", "delete": "destroy"}),
    )
]
