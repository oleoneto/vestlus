# chat:serializers:mixins
from rest_flex_fields import FlexFieldsModelSerializer
from leh.authentication.serializers.user import UserSerializer


class ExpandUserMixin(FlexFieldsModelSerializer):
    class Meta:
        expandable_fields = {
            'user': (UserSerializer, {'source': 'user'})
        }
