from django.views.generic import ListView, DetailView
from .models import Post
from .forms import PostForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone


class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_on = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})
