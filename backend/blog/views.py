# from django.views.generic import ListView, DetailView
#
# from blog.models import Post
#
#
# class PostLV(ListView):
#     model = Post
#     # template_name = 'blog/post_list.html'
#     # blog/urls.py에 있는 name='' 과 템플릿의 이름이 같기 때문에 생략해도 된다.
#
#
# class PostDV(DetailView):
#     model = Post
#     # 템플릿의 이름과 urls.py의 name이 같으면 탬플릿 네임은 생략해도 된다.
from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404
from blog.models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse


class PostListTV(TemplateView):
    # TemplateView를 상속 받는다면, template_name은 무조건 넣어줘야한다.
    template_name = 'blog/post_list.html'


class PostDetailTV(TemplateView):
    template_name = 'blog/post_detail.html'


def ScrapView(request, pk):
    news = get_object_or_404(Post, id=request.POST.get('post_id'))
    if news.scrap.filter(id=request.user.id).exists():
        news.scrap.remove(request.user)
    else:
        news.scrap.add(request.user)
    return HttpResponseRedirect(reverse('blog:post_list', args=[str(pk)]))
