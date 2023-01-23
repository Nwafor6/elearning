from rest_framework import permissions

class IsStaffOnly(permissions.BasePermission):
    '''
    Allow only staff update student,s paid status
    '''
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_instructor:
            return True
        return False