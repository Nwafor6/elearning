from rest_framework import permissions








class IsAuthorOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):

		# Read-only ermission are allowe for any request
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.email == request.user
