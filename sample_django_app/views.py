from rest_framework import viewsets
from .models import Plan, Pack
from .serializers import (
    PlanSerializer,
    PackSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from core.helpers.payment_helpers import (
    cancel_subscription,
    create_plan_session,
    get_current_period_end,
    create_pack_session,
)
from core.permissions import IsSuperAdmin


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)
    default_permissions_classes = (IsAuthenticated,)
    permissions = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "create": (IsAuthenticated, IsSuperAdmin),
        "destroy": (IsAuthenticated, IsSuperAdmin),
        "partial_update": (IsAuthenticated, IsSuperAdmin),
    }
    queryset = Plan.objects.filter(deleted=False)

    def get_permissions(self):
        if self.permissions:
            self.permission_classes = self.permissions.get(
                self.action, self.default_permissions_classes
            )
            return super().get_permissions()

    def subscribe_user(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            if not instance.stripe_id:
                cancel_subscription(self.request.user)
                self.request.user.plan = instance
                self.request.user.save()
                return Response({"sessionId": instance.stripe_id}, status=status.HTTP_200_OK)
            session_id = create_plan_session(self.request.user, instance.stripe_id)
            return Response({"sessionId": session_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"plan": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def cancel_subscription(self, request, *args, **kwargs):
        try:
            cancel_subscription(self.request.user)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"plan": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def current_plan(self, request, *args, **kwargs):
        user = self.request.user
        if user.plan and user.payment_subscription_stripe_id:
            serializer = self.get_serializer(user.plan)
            data = {
                "id": serializer.data["id"],
                "name": serializer.data["name"],
                "description": serializer.data["description"],
                "duration": serializer.data["duration"],
                "price": serializer.data["price"],
                "number_credits": user.count_of_credits,
                "date_to_pay": get_current_period_end(
                    user.payment_subscription_stripe_id
                ),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)


class PackViewSet(viewsets.ModelViewSet):
    serializer_class = PackSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Pack.objects.filter(deleted=False)
    default_permissions_classes = (IsAuthenticated,)
    permissions = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "create": (IsAuthenticated, IsSuperAdmin),
        "partial_update": (IsAuthenticated, IsSuperAdmin),
        "destroy": (IsAuthenticated, IsSuperAdmin),
    }

    def get_permissions(self):
        if self.permissions:
            self.permission_classes = self.permissions.get(
                self.action, self.default_permissions_classes
            )
            return super().get_permissions()

    def buy_pack(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            session_id = create_pack_session(self.request.user, instance.price_stripe_id)
            return Response({"sessionId": session_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"pack": str(e)}, status=status.HTTP_400_BAD_REQUEST)
