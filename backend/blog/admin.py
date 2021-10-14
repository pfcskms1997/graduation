from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt', 'tag_list')

    # 두 태이블에 n대n이면 prefetch_related() 1대n이면 selected_related()를 사용
    def get_queryset(self, request):
        # 태그 테이블에서 가지고 올때, prefetch_related메서드를 사용하는데, 디비에 대한 쿼리 횟수를 줄이기 위해 포스트 레코드를 가지고 올때 태그 레코드도 가지고 오라는 의미
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj): #여기서 태크 테이블에 있는 레코드를 가지고 와서 , 로 이어붙이고 있다.
        return u", ".join(o.name for o in obj.tags.all())