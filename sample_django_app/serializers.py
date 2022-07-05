from core.serializers import DynamicFieldsModelSerializer
from .models import Plan, Pack, PaymentHistory
from rest_framework import serializers
from core.helpers.payment_helpers import create_plan, create_pack, update_product


class PackSerializer(DynamicFieldsModelSerializer):
    def create(self, validated_data):
        instance = Pack.objects.create(**validated_data)
        return create_pack(instance)

    def update(self, instance, validated_data):
        product_name = validated_data.get("name")
        if product_name and product_name != instance.name:
            update_product(instance.product_stripe_id, {"name": product_name})
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Pack
        extra_kwargs = {
            "stripe_product_id": {"write_only": True},
        }
        exclude = (
            "created_at",
            "updated_at",
        )


class PlanSerializer(DynamicFieldsModelSerializer):
    free = serializers.BooleanField(write_only=True)

    def create(self, validated_data):
        free = validated_data.pop("free", False)
        instance = Plan.objects.create(**validated_data)
        if free:
            instance.save()
            return instance
        create_plan(instance)
        return instance

    def update(self, instance, validated_data):
        product_name = validated_data.get("name")
        if product_name != instance.name and instance.stripe_id:
            update_product(instance.product_stripe_id, {"name": product_name})
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Plan
        exclude = (
            "created_at",
            "updated_at",
        )


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        exclude = (
            "created_at",
            "updated_at",
        )
