from rest_framework import serializers
from ..models import Membership
from .mixins import ExcludeTimestampMixin


class MembershipSerializer(serializers.ModelSerializer):

    class Meta(ExcludeTimestampMixin.Meta):
        model = Membership

        read_only_fields = (
            'invited_by',
            'channel',
            'uuid',
            'created_at',
            'updated_at'
        )
