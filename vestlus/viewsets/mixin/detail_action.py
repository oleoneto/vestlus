from rest_framework.decorators import action
from rest_framework.response import Response


class DetailActionMixin:
    def detail_action(self, objects, klass_serializer):
        page = self.paginate_queryset(objects)
        if page is not None:
            serializer = klass_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = klass_serializer(objects, many=True)
        return Response(serializer.data)
