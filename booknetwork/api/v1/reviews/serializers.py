from rest_framework import serializers

from api.v1.reviews.models import Review


class ReeviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
