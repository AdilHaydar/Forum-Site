from django.shortcuts import render,redirect,Http404,get_object_or_404,HttpResponseRedirect,reverse
from Forum.models import Forum, SubForum, Moderator
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Topic, Comment
from user.models import User
from .forms import CommentForm, TopicForm
from bs4 import BeautifulSoup
# Create your views here.


def show(request,name,slug):
	page = request.GET.get('page',1)
	topic = Topic.objects.get(slug = slug)
	
	topic.views_plus()
	comments = Comment.objects.filter(topic = topic)
	paginator = Paginator(comments, 10)
	comment_form = CommentForm()

	try:
		comments = paginator.page(page)
	except PageNotAnInteger:
		comments = paginator.page(1)
	except EmptyPage:
		comments = paginator.page(paginator.num_pages)

	return render(request, "show.html", {'topic':topic,'comments':comments,'comment_form':comment_form,'name':name})

@login_required(login_url = "user:login")
def create_post(request,forum):
	topic_form = TopicForm(request.POST or None)
	if topic_form.is_valid():
		created_topic = topic_form.save(commit = False)
		created_topic.owner = request.user
		created_topic.forum = SubForum.objects.get(name = forum)
		created_topic.save()

		messages.success(request,'Comment Successfully Send.')
		return HttpResponseRedirect(reverse('Topic:show',kwargs={'name':forum,'slug':created_topic.slug})) 
	return render(request,'create_topic.html',{'form':topic_form})


@login_required(login_url = "user:login")
def create_comment(request,name,slug):
	if not request.user.is_authenticated:
		raise Http404
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			created_comment = comment_form.save(commit = False)

			created_comment.owner = request.user
			created_comment.topic = Topic.objects.get(slug = slug)
			created_comment.save()

			messages.success(request,'Comment Successfully Send.')
		messages.warning(request,"Comment can't send.")
		return HttpResponseRedirect(reverse('Topic:show',kwargs={'name':name,'slug':slug}))

def lock(request,slug): 
	post = get_object_or_404(Topic, slug=slug)
	forum = post.forum
	mod = Moderator.objects.filter(forum = forum)
	if request.user.is_staff:
		if request.user in mod or request.user.userpermission != 'Mod':
			post.lock_topic = not post.lock_topic
			post.lock()
			return HttpResponseRedirect(reverse('Topic:show',kwargs={'name':forum,'slug':slug}))
		return redirect("index")
	return redirect("index")

def move(request, slug):
	post = get_object_or_404(Topic, slug=slug)
	post_forum = post.forum
	mod = Moderator.objects.filter(forum = post_forum)
	if request.user.is_staff:
		if request.user in mod or request.user.userpermission != 'Mod':
			forums = Forum.objects.all()

			if request.method == "POST":

				subforum = request.POST.get('forums')
				forum = SubForum.objects.get(id = subforum)
				post.forum = forum
				post.move(post_forum)
				return redirect('index')

		return render(request,"move_topic.html",{'post':post,'forums':forums})
	return redirect("index")
	