# vestlus:serializers:mixins
from rest_framework import serializers


class ExcludePolymorphicMixin(serializers.ModelSerializer):
    """Exclude polymorphic content type from serializer"""

    class Meta:
        exclude = ('polymorphic_ctype',)


class ExcludeTimestampMixin(serializers.ModelSerializer):
    """Make uuid, created_at, and updated_at fields read-only"""

    class Meta:
        exclude = (
            'created_at',
            'updated_at',
        )


class ExcludeTimestampAndPolymorphicMixin(serializers.ModelSerializer):
    """Exclude polymorphic content type from serializer"""

    class Meta(ExcludeTimestampMixin.Meta):
        exclude = ExcludeTimestampMixin.Meta.exclude + ('polymorphic_ctype',)
