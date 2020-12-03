from django.shortcuts import render,redirect,Http404,get_object_or_404,HttpResponseRedirect,reverse
from .models import Forum, SubForum
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from Topic.models import Topic, Comment
from user.models import User
from Topic.forms import CommentForm, TopicForm
from user.forms import LoginForm

# Create your views here.

def index(request):
	total_topic = 0
	total_comment = 0

	forums = Forum.objects.all()
	subForums = SubForum.objects.all()

	for forum in subForums:
		total_topic += forum.topic_count
		total_comment += forum.comment_count

	last_ten_topic = Topic.objects.all().order_by('-id')[:10]
	last_ten_comment = Comment.objects.all().order_by('-id')[:10]
	last_ten_user = User.objects.all().order_by('-timestamp')[:10]
	most_posted_users = User.objects.all().order_by('-topic_count')[:10]
	total_user = User.objects.all().count()
	login_form = LoginForm()

	context = {
			'forums': forums,
			'subForums': subForums,
			'last_ten_user': last_ten_user,
			'last_ten_comment': last_ten_comment,
			'last_ten_topic': last_ten_topic,
			'login_form' : login_form,
			'most_posted_users' : most_posted_users,
			'total_topic' : total_topic,
			'total_comment' : total_comment,
			'total_user' : total_user,

		}

	return render(request,'forum.html', context)


def list(request,name):
	page = request.GET.get('page',1)
	subForum = SubForum.objects.get(name = name)
	topics = Topic.objects.filter(forum = subForum)
	paginator = Paginator(topics, 20)

	try:
		topics = paginator.page(page)
	except PageNotAnInteger:
		topics = paginator.page(1)
	except EmptyPage:
		topics = paginator.page(paginator.num_pages)

	return render(request,"topic_list.html",{'subForum':subForum, 'topics':topics})


	