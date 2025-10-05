from rest_framework import viewsets

from api.v1.reviews.models import Review
from api.v1.reviews.serializers import ReeviewSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReeviewSerializers
