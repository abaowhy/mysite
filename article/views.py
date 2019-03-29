from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ArticleColumn, ArticlePost
from .form import ArticlePostForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger



@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)

        return render(request, 'article/column/article_column.html', {'columns': columns})
    if request.method == 'POST':
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST['column']
    column_id = request.POST['column_id']
    columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
    if columns:
        return HttpResponse('2')
    else:
        try:
            line = ArticleColumn.objects.get(id=column_id)
            line.column = column_name
            line.save()
            return HttpResponse('1')
        except:
            return HttpResponse('3')


@login_required(login_url='/account/login/')
@csrf_exempt
def delete_article_column(request):
        column_id = request.POST['column_id']
        try:
            line = ArticleColumn.objects.filter(id=column_id)
            line.delete()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = ArticleColumn.objects.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, 'article/column/article_post.html', {'article_post_form': article_post_form, 'article_columns': article_columns})


@login_required(login_url='/account/login/')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    #articles = request.user.article.all()

    paginator = Paginator(articles_list, 2)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    return render(request, 'article/column/article_list.html', {'articles': articles, 'page': current_page})


@login_required(login_url='/account/login/')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, 'article/column/article_detail.html', {'article': article})


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def delete_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


@login_required(login_url='/account/login/')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        article_form = ArticlePostForm(initial={'title': article.title})
        return render(request, "article/column/redit_article.html",\
                      {"article": article, "article_columns": article_columns,\
                       "article_form": article_form})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)

        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except Exception as e:
            print(str(e))
            return HttpResponse('2')


