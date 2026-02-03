from django.urls import path
from .views import (
    OrganizationCreateView,
    OrganizationDetailView,
    OrganizationMembersView,
    InviteUserView,
    OrganizationMemberManageView,
    AcceptInviteView,
    TransferOwnershipView,
    LeaveOrganizationView,
    OrganizationMemberDetailByUserView,
)

urlpatterns = [
    path("", OrganizationCreateView.as_view(), name="org-list-create"),
    path("<uuid:pk>/", OrganizationDetailView.as_view(), name="org-detail"),
    path("<uuid:pk>/members/", OrganizationMembersView.as_view(), name="org-members"),
    path("<uuid:org_id>/members/<uuid:member_id>/",OrganizationMemberManageView.as_view(),name="org-member-manage",),
    path("<uuid:pk>/invite/", InviteUserView.as_view(), name="org-invite"),
    path("invites/<uuid:token>/accept/",AcceptInviteView.as_view(),name="invite-accept"),
    path("<uuid:org_id>/transfer-ownership/",TransferOwnershipView.as_view(),name="org-transfer-ownership"),
    path("<uuid:org_id>/leave/",LeaveOrganizationView.as_view(),name="org-leave"),
    path("<uuid:org_id>/members/user/<uuid:user_id>/",OrganizationMemberDetailByUserView.as_view(),name="org-member-by-user"),
]

