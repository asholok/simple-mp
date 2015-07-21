from tastypie import resources, fields
from tastypie.authorization import Authorization
from profiles.models import Profile, Course, CourseType
from django.contrib.auth.models import User

class CourseTypeResource(resources.ModelResource):
    class Meta:
        queryset = CourseType.objects.all()

        fields = ['id', 'name']
        allowed_methods = ['get']
        resource_name = 'course-type'

""" ***************** Private ************************************************ """

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
        allowed_methods = ['get', 'put', 'patch']
        always_return_data = True
        authorization = Authorization()
        filtering = {'private-user': resources.ALL_WITH_RELATIONS}

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class PrivateCourseResource(resources.ModelResource):
    ovner = fields.ForeignKey(PrivateProfileResource, 'private-profile')
    course_type = fields.ForeignKey(CourseTypeResource, 'course-type')

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'private-course'
        fields = ['course_name', 'course_type', 'course_desciption', 'ovner']
        allowed_methods = ['get', 'put', 'patch']
        always_return_data = True
        authorization = Authorization()
        filtering = {
            'private-user': resources.ALL_WITH_RELATIONS,
            'course-type': resources.ALL_WITH_RELATIONS
        }

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

""" ***************** End Private ********************************************* """

""" ***************** Public ************************************************** """

class PublicUserResource(resources.ModelResource):
    class Meta:
        queryset = User.objects.all()

        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
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

class PublicCourseResource(resources.ModelResource):
    ovner = fields.ForeignKey(PublicProfileResource, 'profile')

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        fields = ['course_name', 'course_type', 'course_desciption', 'ovner']
        allowed_methods = ['get']
        always_return_data = True
        filtering = {'ovner': resources.ALL_WITH_RELATIONS}


""" ***************** End Public *********************************************** """

""" ***************** Create *************************************************** """
    
class CreateProfileResource(resources.ModelResource):

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'create-profile'
        fields = ['user', 'zip_code', 'country', 'city', 'user_desciption']
        allowed_methods = ['get', 'post']
        always_return_data = True
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        user = User.objects.create_user(
                username=bundle.data.get('username'), 
                email=bundle.data.get('email'), 
                password=bundle.data.get('password')
            )
        bundle.data['user'] = user
        return super(PrivateProfileResource, self).obj_create(bundle, request, **kwargs)

class CreateCourseResource(resources.ModelResource):

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'create-profile'
        fields = ['course_name', 'course_type', 'course_desciption', 'ovner']
        excludes = ['ovner']
        allowed_methods = ['get', 'post']
        always_return_data = True
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['ovner'] = request.user
        bundle.data['course_type'] = CourseType.objects.get(bundle.data['course_type'])
        
        return super(PrivateProfileResource, self).obj_create(bundle, request, **kwargs)