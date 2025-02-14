from django.contrib.auth import login, logout, update_session_auth_hash, get_user
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Count
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseCreateView, BaseUpdateView, BaseDeleteView
from django.views.generic.list import BaseListView
#from taggit.models import Tag
from blog.models import Topics

from blog.models import Post
from accounts.forms import MyUserCreationForm
from accounts.views import MyLoginRequiredMixin
from accounts.views import OwnerOnlyMixin
from api.views_util import obj_to_post, prev_next_post, make_tag_cloud


class ApiPostLV(BaseListView):
    # model = Post
    def get_queryset(self):
        tagname = self.request.GET.get('tagname')
        if tagname:
            qs = Post.objects.filter(tags__name=tagname)
        else:
            qs = Post.objects.all()
        return qs

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        postList = [obj_to_post(obj) for obj in qs]
        return JsonResponse(data=postList, safe=False, status=200)

class ApiPostDV(BaseDetailView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        post = obj_to_post(obj)
        post['prev'], post['next'] = prev_next_post(obj)
        return JsonResponse(data=post, safe=True, status=200)


class ApiTagCloudLV(BaseListView):
    # model = Tag
    #queryset = Tag.objects.annotate(count=Count('post'))
    queryset = Topics.objects.annotate(count=Count('post'))

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        tagList = make_tag_cloud(qs)
        return JsonResponse(data=tagList, safe=False, status=200)

class ApiLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        userDict = {
            'id': user.id,
            'username': user.username,
        }
        return JsonResponse(data=userDict, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)


class ApiRegisterView(BaseCreateView):
    form_class = MyUserCreationForm

    def form_valid(self, form):
        self.object = form.save()
        userDict = {
            'id': self.object.id,
            'username': self.object.username,
        }
        return JsonResponse(data=userDict, safe=True, status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class ApiLogoutView(LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)

        return JsonResponse(data={}, safe=True, status=200)

class ApiPwdchgView(PasswordChangeView):
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return JsonResponse(data={}, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class ApimeView(View):
    def get(self, request, *args, **kwargs):
        user = get_user(request)

        if user.is_authenticated:
            userDict = {
                'id': user.id,
                'username': user.username,
            }
        else:
            userDict ={
                'username': 'Anonymous',
            }

        return JsonResponse(data=userDict, safe=True, status=200)

class ApiPostCV(MyLoginRequiredMixin, BaseCreateView):
    model = Post
    fields = '__all__'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        post = obj_to_post(self.object)
        return JsonResponse(data=post, safe=True, status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class ApiPostUV(OwnerOnlyMixin, BaseUpdateView):
    model = Post
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        post = obj_to_post(self.object)
        return JsonResponse(data=post, safe=True, status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class ApiPostDelV(OwnerOnlyMixin, BaseDeleteView):
    model = Post

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse(data={}, safe=True, status=204)

class ApiPostScrapLV(MyLoginRequiredMixin, BaseListView):
    def get_queryset(self):
        username = self.request.user.username
        qs = Post.objects.filter(scrap__username=username)
        return qs

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        postList = [obj_to_post(obj) for obj in qs]
        return JsonResponse(data=postList, safe=False, status=200)

class ApiPostScrapDView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(data={'errmsg': 'you should login first!'}, safe=True, status=401)
        else:
            if 'post_id' in kwargs:
                post_id = kwargs['post_id']
                print(post_id)
                post = Post.objects.get(pk=post_id)
                print(post)
                user = request.user
                if user in post.scrap.all():
                    post.scrap.remove(user)
                    return JsonResponse(data={'successmsg': 'unscrapped!'}, safe=True, status=200)
                else:
                    return JsonResponse(data={'errmsg': 'Already unscrapped.'}, safe=True, status=401)


class ApiPostScrapAddView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(data={'errmsg':'you should login first!'}, safe=True, status=401)
        else:
            if 'post_id' in kwargs:
                post_id = kwargs['post_id']
                print(post_id)
                post = Post.objects.get(pk=post_id)
                print(post)
                user = request.user
                if user in post.scrap.all():
                    return JsonResponse(data={'errmsg':'Already scrapped.'}, safe=True, status=401)
                else:
                    post.scrap.add(user)
                    return JsonResponse(data={'successmsg':'scrapped!'}, safe=True, status=200)

