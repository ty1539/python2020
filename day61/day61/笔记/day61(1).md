展示数据的4个方法

对单标的新增和编辑

两个url  +  一个视图（modelform）  + 一个模板



评论框样式

http://www.jq22.com/demo/jQueryWbPl201705260102/

文章详情 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Blog Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">

    {% load static %}
    <!-- Custom styles for this template -->
    <link href="{% static 'css/blog.css' %}" rel="stylesheet">
    <link href="{% static 'css/comment/comment.css' %}" rel="stylesheet">
    <link href="{% static 'css/comment/style.css' %}" rel="stylesheet">


</head>

<body>

{% include 'nav.html' %}

<div class="container">

    <div class="blog-header">
        <h1>{{ article_obj.title }}</h1>
        <p class="lead blog-description">{{ article_obj.detail.content|safe }}</p>


        <div class="commentAll">

            <div class="reviewArea clearfix">
                <div class="flex-text-wrap">
                    <pre class="pre"><span></span><br></pre>
                    <textarea class="content comment-input" placeholder="Please enter a comment…"
                    ></textarea></div>
                <a href="javascript:;" id='comment' class="plBtn">评论</a>
            </div>


            <div class="comment-show">

                {% for comment in article_obj.comment_set.all %}
                    <div class="comment-show-con clearfix">
                        <div class="comment-show-con-img pull-left">
                            <img src="{{ comment.author.avatar.url }}" alt="">
                        </div>
                        <div class="comment-show-con-list pull-left clearfix">
                            <div class="pl-text clearfix">
                                <a href="#" class="comment-size-name">{{ comment.author.username }} : </a>
                                <span class="my-pl-con">&nbsp;{{ comment.content }}</span>
                            </div>
                            <div class="date-dz">
                                <span class="date-dz-left pull-left comment-time">{{ comment.time }}</span>
                                <div class="date-dz-right pull-right comment-pl-block">
                                    <a href="javascript:;" class="removeBlock">删除</a>
                                </div>
                            </div>
                            <div class="hf-list-con"></div>
                        </div>
                    </div>
                {% endfor %}




            </div>

        </div>

    </div>


</div><!-- /.container -->

<footer class="blog-footer">
    <p>Blog template built for <a href="http://getbootstrap.com">Bootstrap</a> by <a
            href="https://twitter.com/mdo">@mdo</a>.</p>
    <p>
        <a href="#">Back to top</a>
    </p>
</footer>


<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
<script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>


<script>

    $('#comment').click(function () {
        var content = $('.comment-input').val();
        var article_id = {{ article_obj.pk }};
        var author_id = {{ request.user_obj.pk }};
        var author_name = '{{ request.user_obj.username }}';
        var author_avatar = '{{ request.user_obj.avatar.url }}';
        $.ajax({
            url:'/comment/',
            data:{
                content:content,
                article_id:article_id,
                author_id:author_id,
            },
            success: (res) => {
                if (res.status){
                    // 评论插入到数据库成功了
                    $('.comment-show').append(`<div class="comment-show-con clearfix">
                    <div class="comment-show-con-img pull-left">
                        <img src="${author_avatar}" alt="">
                    </div>
                    <div class="comment-show-con-list pull-left clearfix">
                        <div class="pl-text clearfix">
                            <a href="#" class="comment-size-name">${author_name} : </a>
                            <span class="my-pl-con">${content}</span>
                        </div>
                        <div class="date-dz">
                            <span class="date-dz-left pull-left comment-time">${res.time}</span>
                            <div class="date-dz-right pull-right comment-pl-block">
                                <a href="javascript:;" class="removeBlock">删除</a>
                            </div>
                        </div>
                        <div class="hf-list-con"></div>
                    </div>
                </div>`)

                    $('.comment-input').val('')
                    alert('评论成功')
                }
            }

        })
    })
</script>


</body>
</html>
```

评论路由

```python
url(r'^comment/$', views.comment, name='comment'),
```

视图

```python
from django.http.response import JsonResponse

from django.utils import timezone


def comment(request):
    obj = models.Comment.objects.create(**request.GET.dict())

    return JsonResponse({'status': True, 'time': timezone.localtime(obj.time).strftime('%Y-%m-%d %H:%M:%S')})
```

