from rest_framework import permissions


class AutoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            print('options')
            return False
        #print('Inside Vysfin Permission')
        # print(request.user.id)
        # print(request.method)
        # print('Kindly handle permission module')
        return True