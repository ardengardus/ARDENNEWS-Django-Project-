from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import News, Comment
from .forms import NewsForm, CommentForm

def index(request):
    latest_news = News.objects.all()[:3]
    return render(request, 'index.html', {'latest_news': latest_news})

def contacts(request):
    return render(request, 'contacts.html')

def news_list(request):
    news_queryset = News.objects.all()
    sort_by = request.GET.get('sort', '-pub_date')
    
    search_query = request.GET.get('search', '')
    if search_query:
        news_queryset = news_queryset.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if sort_by == 'pub_date_asc':
        news_queryset = news_queryset.order_by('pub_date')
    else:
        news_queryset = news_queryset.order_by('-pub_date')
    
    paginator = Paginator(news_queryset, 5)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    return render(request, 'news_list.html', {
        'news': news,
        'search_query': search_query,
        'current_sort': sort_by
    })

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    comments = news_item.comments.filter(is_active=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('news:news_detail', pk=news_item.pk)
    else:
        form = CommentForm()
    
    return render(request, 'news_detail.html', {
        'news': news_item,
        'comments': comments,
        'form': form
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость создана!')
            return redirect('news:news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'news_create.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость обновлена!')
            return redirect('news:news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news_edit.html', {'form': form, 'news': news})

@login_required
@user_passes_test(lambda u: u.is_staff)
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость удалена!')
        return redirect('news:news_list')
    return render(request, 'news_confirm_delete.html', {'news': news})