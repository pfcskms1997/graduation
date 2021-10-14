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
from django.views.generic import TemplateView


class PostListTV(TemplateView):
    # TemplateView를 상속 받는다면, template_name은 무조건 넣어줘야한다.
    template_name = 'blog/post_list.html'


class PostDetailTV(TemplateView):
    template_name = 'blog/post_detail.html'
