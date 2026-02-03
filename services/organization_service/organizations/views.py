import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

from .models import Organization, OrganizationMember, OrganizationInvite
from .serializers import (
    OrganizationSerializer,
    OrganizationMemberSerializer,
    ChangeMemberRoleSerializer,
)
from .utils.helper_functions import is_owner, is_admin_or_owner, get_membership


# -----------------------------
# Auth Service URL (Traefik Route)
# -----------------------------
AUTH_SERVICE_URL = "http://auth-service/api/auth/users/"   # <-- FIXED


# -----------------------------
# Create + List Organizations
# -----------------------------
class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Organizations where user is a member
        orgs = Organization.objects.filter(
            members__user_id=request.user.id
        ).distinct()

        serializer = OrganizationSerializer(orgs, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Get user from request
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Pass both user_id and username to serializer context
        serializer = OrganizationSerializer(
            data=request.data,
            context={
                "user_id": user.id,
                "username": user.username,
            },
        )

        if serializer.is_valid():
            org = serializer.save()

            return Response(
                OrganizationSerializer(org).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# Single Organization Details
# -----------------------------
class OrganizationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            org = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return Response(
                {"error": "Organization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrganizationSerializer(org)
        return Response(serializer.data)


# -----------------------------
# List Members of an Organization
# -----------------------------
class OrganizationMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        members = OrganizationMember.objects.filter(org_id=pk)
        serializer = OrganizationMemberSerializer(members, many=True)
        return Response(serializer.data)
    
class OrganizationMemberManageView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, org_id, member_id):
        if not is_admin_or_owner(org_id, request.user.id):
            return Response({"error": "Only owner or Admin can change roles"}, status=403)

        role = request.data.get("role")

        if role not in [
            OrganizationMember.ROLE_ADMIN,
            OrganizationMember.ROLE_MEMBER
        ]:
            return Response({"error": "Invalid role"}, status=400)

        try:
            member = OrganizationMember.objects.get(
                id=member_id,
                org_id=org_id
            )
        except OrganizationMember.DoesNotExist:
            return Response({"error": "Member not found"}, status=404)

        if member.role == OrganizationMember.ROLE_OWNER:
            return Response(
                {"error": "Cannot change owner role"},
                status=400
            )

        member.role = role
        member.save(update_fields=["role"])

        return Response({"message": "Role updated successfully"})


    def delete(self, request, org_id, member_id):
        requester = get_membership(org_id, request.user.id)

        if not requester:
            return Response({"error": "Forbidden"}, status=403)

        try:
            target = OrganizationMember.objects.get(
                id=member_id,
                org_id=org_id
            )
        except OrganizationMember.DoesNotExist:
            return Response({"error": "Member not found"}, status=404)

        # ❌ Cannot remove OWNER
        if target.role == OrganizationMember.ROLE_OWNER:
            return Response(
                {"error": "Cannot remove organization owner"},
                status=400
            )

        # ADMIN cannot remove ADMIN
        if requester.role == OrganizationMember.ROLE_ADMIN and \
           target.role == OrganizationMember.ROLE_ADMIN:
            return Response({"error": "Forbidden"}, status=403)

        # OWNER removing someone → OK
        # ADMIN removing MEMBER → OK
        target.delete()

        return Response({"message": "Member removed successfully"})



# -----------------------------
# Invite User (Cross-Service Call)
# -----------------------------
class InviteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not is_admin_or_owner(pk, request.user.id):
            return Response({"error": "Forbidden"}, status=403)

        email = request.data.get("email")
        if not email:
            return Response({"error": "email required"}, status=400)

        invite, created = OrganizationInvite.objects.get_or_create(
            org_id=pk,
            email=email,
            defaults={
                "invited_by_id": request.user.id,
            }
        )

        if not created:
            return Response({"error": "Invite already sent"}, status=400)

        return Response({
            "message": "Invite created",
            "token": invite.token  # later emailed
        })

class AcceptInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        # Use getattr to avoid attribute errors
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            invite = OrganizationInvite.objects.get(
                token=token,
                is_accepted=False,
                is_expired=False
            )
        except OrganizationInvite.DoesNotExist:
            return Response({"error": "Invalid or expired invite"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the organization member safely
        OrganizationMember.objects.get_or_create(
            org=invite.org,
            user_id=user.id,
            username=user.username,
            defaults={"role": OrganizationMember.ROLE_MEMBER}
        )

        invite.is_accepted = True
        invite.save(update_fields=["is_accepted"])

        return Response({"message": "Invite accepted"}, status=status.HTTP_200_OK)

    


class TransferOwnershipView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, org_id):
        if not is_owner(org_id, request.user.id):
            return Response(
                {"error": "Only owner can transfer ownership"},
                status=status.HTTP_403_FORBIDDEN
            )

        new_owner_id = request.data.get("new_owner_id")
        if not new_owner_id:
            return Response({"error": "new_owner_id required"}, status=400)

        try:
            new_owner = OrganizationMember.objects.get(
                org_id=org_id,
                user_id=new_owner_id
            )
        except OrganizationMember.DoesNotExist:
            return Response(
                {"error": "User must be a member of the organization"},
                status=400
            )

        if new_owner.role == OrganizationMember.ROLE_OWNER:
            return Response({"error": "User is already owner"}, status=400)

        # downgrade current owner
        OrganizationMember.objects.filter(
            org_id=org_id,
            user_id=request.user.id,
            role=OrganizationMember.ROLE_OWNER
        ).update(role=OrganizationMember.ROLE_ADMIN)

        # promote new owner
        new_owner.role = OrganizationMember.ROLE_OWNER
        new_owner.save(update_fields=["role"])

        # update organization owner_id
        Organization.objects.filter(id=org_id).update(
            owner_id=new_owner_id
        )

        return Response({"message": "Ownership transferred successfully"})

class LeaveOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        try:
            membership = OrganizationMember.objects.get(
                org_id=org_id,
                user_id=request.user.id
            )
        except OrganizationMember.DoesNotExist:
            return Response(
                {"error": "You are not a member of this organization"},
                status=400
            )

        if membership.role == OrganizationMember.ROLE_OWNER:
            return Response(
                {"error": "Owner must transfer ownership before leaving"},
                status=400
            )

        membership.delete()

        return Response({"message": "You have left the organization"})
    
class OrganizationMemberDetailByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, org_id, user_id):
        # requester must be a member of the org
        if not get_membership(org_id, request.user.id):
            return Response({"error": "Forbidden"}, status=403)

        try:
            member = OrganizationMember.objects.get(
                org_id=org_id,
                user_id=user_id
            )
        except OrganizationMember.DoesNotExist:
            return Response(
                {"error": "Member not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrganizationMemberSerializer(member)
        return Response(serializer.data)


