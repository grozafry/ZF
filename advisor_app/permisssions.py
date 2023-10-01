from rest_framework import permissions

class IsAdvisor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "Advisor":
            return True
        return False
