# permissions.py
from organizations.models import OrganizationMember

def get_membership(org_id, user_id):
    return OrganizationMember.objects.filter(
        org_id=org_id,
        user_id=user_id
    ).first()


def is_owner(org_id, user_id):
    return OrganizationMember.objects.filter(
        org_id=org_id,
        user_id=user_id,
        role=OrganizationMember.ROLE_OWNER
    ).exists()


def is_admin_or_owner(org_id, user_id):
    return OrganizationMember.objects.filter(
        org_id=org_id,
        user_id=user_id,
        role__in=[
            OrganizationMember.ROLE_OWNER,
            OrganizationMember.ROLE_ADMIN
        ]
    ).exists()
