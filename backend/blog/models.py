from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    tags = TaggableManager(blank=True)
    # User테이블과 1대 n 관계로 foreign키를 잡아준다.
    # on_delete가 CASCADE이면 유저 테이블에서 한 레코드가 삭제되면 이 레코드랑 관련된 모든 Post의 레코드가 삭제된다.
    # owner 칸은 비어있을 수 있으므로 blank, null을 ture로 해준다. 비어있어도 되고 필드에 null로 저장하는 것을 허용
    # get_user_model() 을 통해 인증테이블을 불러와준다.
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)
    scrap = models.ManyToManyField(get_user_model(), related_name='scrapping')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.id,))

    def get_prev(self):
        return self.get_previous_by_modify_dt()

    def get_next(self):
        return self.get_next_by_modify_dt()

    def number_of_scrap(self):
        return self.scrap.count()

# class Scrap(models.Model):
#     user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     news_id = models.ForeignKey(Post, on_delete=models.CASCADE)