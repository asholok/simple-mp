from tastypie import resources, fields
from tastypie.authorization import Authorization
from profiles.models import Profile, Course
from django.contrib.auth.models import User

class PrivateUserResource(resources.ModelResource):
    class Meta:
        queryset = User.objects.all()

        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        resource_name = 'private-user'
        filtering = {'id': ('exact',)}
        authorization = Authorization()

class PrivateProfileResource(resources.ModelResource):
    user = fields.ForeignKey(PrivateUserResource, 'private-user')

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'private-profile'
        fields = ['user', 'zip_code', 'country', 'city', 'user_desciption']
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        authorization = Authorization()
        filtering = {'private-user': resources.ALL_WITH_RELATIONS}

    def obj_create(self, bundle, request=None, **kwargs):
        user = User.objects.create_user(
                username=bundle.data.get('username'), 
                email=bundle.data.get('email'), 
                password=bundle.data.get('password')
            )
        bundle.data['user'] = user
        return super(PrivateProfileResource, self).obj_create(bundle, request, **kwargs)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class PrivateCourseResource(resources.ModelResource):
    ovner = fields.ForeignKey(PrivateProfileResource, 'profile')

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        fields = ['course_name', 'course_type', 'course_desciption', 'ovner']
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        authorization = Authorization()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class PublicUserResource(resources.ModelResource):
    class Meta:
        queryset = User.objects.all()

        excludes = [ 'email', 'password', 'is_active', 'is_staff', 'is_superuser']
        resource_name = 'user'
        allowed_methods = ['get']
        filtering = {'id': ('exact',)}

class PublicProfileResource(resources.ModelResource):
    user = fields.ForeignKey(PublicUserResource, 'user')

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        fields = ['user', 'zip_code', 'country', 'city', 'user_desciption']
        allowed_methods = ['get']
        always_return_data = True
        authorization = Authorization()
        filtering = {'user': resources.ALL_WITH_RELATIONS}



