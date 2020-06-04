from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, NotFound, NotAcceptable
from rest_framework import viewsets
from rest_framework import permissions
from .router import router
from ..models import Channel
from ..models import Membership
from ..serializers import MembershipSerializer
from .mixin.detail_action import DetailActionMixin
from .mixin.non_detail_action import NonDetailActionMixin


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.none()
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Membership.objects.get_for_user(
            user=self.request.user
        )

    # def initial(self, request, *args, **kwargs):
    #     user = request.user
    #     get_object_or_404(Channel.objects.get_for_user(user=user), pk=kwargs['channels_pk'])
    #     self.queryset = Membership.objects.get_for_channel_and_user(
    #         channel=kwargs['channels_pk'],
    #         user=user
    #     )
    #     return super().initial(request, args, kwargs)

    def perform_create(self, serializer):

        user = self.request.user

        try:
            channel = Channel.objects.get(
                id=self.kwargs['channels_pk']
            )
        except Channel.DoesNotExist:
            raise NotFound()

        # Only members can add people to channels
        if not channel.members.filter(user=user).exists():
            if channel.is_private:
                raise PermissionDenied("Only members can invite new members to private channels.")

        # Ensure memberships are not duplicated
        invitee = serializer.validated_data['user']
        if channel.members.filter(user_id=invitee).exists():
            raise NotAcceptable("User is already a member.")

        serializer.save(
            channel_id=channel.id,
            invited_by_id=user.id
        )

    def perform_update(self, serializer):

        serializer = MembershipSerializer()

        user = self.request.user

        try:
            channel = Channel.objects.get(
                id=self.kwargs['channels_pk']
            )
        except Channel.DoesNotExist:
            raise NotFound()

        # Only members can update members
        if not channel.members.filter(user=user).exists():
            raise PermissionDenied()

        # User id cannot be updated
        if 'user' in serializer.validated_data:
            raise NotAcceptable()

        # Owner will always be admin. Only admins can make admins
        if 'is_admin' in serializer.validated_data:
            membership_id = self.kwargs['pk']

            updated_user_id = Membership.objects.get(id=membership_id).user_id
            wants_to_update_owner = channel.owner.id == updated_user_id
            requester_is_admin = channel.members.get(user=user).is_admin

            if not requester_is_admin:
                raise PermissionDenied()

            if wants_to_update_owner:
                raise PermissionDenied("Channel owner is always admin.")

        serializer.save()


router.register('memberships', MembershipViewSet)
