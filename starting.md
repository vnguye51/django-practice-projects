## 1. Initializing the project

Use the command 

    django-admin startproject <name>

## 2. Creating an app

Use the command 

    python manage.py startapp <appname>

## 3. Creating views

In the views folder 

Inside  <appname>/views.py and replace it with the your views Ex:

    from django.http import HttpResponse


    def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")

    def detail(request, question_id):
        return HttpResponse("You're looking at question %s." % question_id)

    def results(request, question_id):
        response = "You're looking at the results of question %s."
        return HttpResponse(response % question_id)

    def vote(request, question_id):
        return HttpResponse("You're voting on question %s." % question_id)

Now inside <name>/urls.py we need to point the URLconf to the paths we just created add the following code

    from django.contrib import admin
    from django.urls import include, path

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

Quoted from djangoproject.com 

"The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

path(route, view, **kwargs, **name)

route: is a string that contains a URL pattern. When processing a request, Django starts at the first pattern in urlpatterns and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches.

view: When Django finds a matching pattern, it calls the specified view function with an HttpRequest object as the first argument and any “captured” values from the route as keyword arguments. We’ll give an example of this in a bit.

## 4. Setting up a database and other configs

sqlite works out of the box with python, for other backends we need to connect it to python.

MySQL: "pip install mysqlclient"
On windows a wheel needs to be installed and so download the correct version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python
and then "pip install <absolute filepath>"
Visual Studio C++ might also be needed "https://visualstudio.microsoft.com/vs/"

To connect a database to the project inside settings.py add in the database parameters. In my case it is

        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'python_polls',
            'USER': 'root',
            'PASSWORD': '7182011',
            'HOST': '127.0.0.1',
            'PORT': '3306'
        }


Remember to change the timezone parameter to "America/Los_Angeles"


## 5. Creating models
Inside "<appname>/models.py"

Example models:

    class Question(models.Model):
        def __str__(self):
            return self.question_text
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')


    class Choice(models.Model):
        def __str__(self):
            return self.choice_text
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

The first field argument is the name as in "date published" otherwised the property name will be used instead as in question_text

Now run 

    python manage.py migrate

This looks at INSTALLED_APPS and creates the tables necessary for them

## 6. Activating models

Now we need to tell the project where the app is installed so inside "<name>/settings.py"

add the path to INSTALLED_APPS so that it looks like:

    INSTALLED_APPS = [
        '<appname>.apps.PollsConfig',
        ...
    ]

Now run 

    python manage.py makemigrations

makemigrations tells Django that changes were made to the apps or models

If you want run "manage.py sqlmigrate <appname> 0001" to see the SQL code that python generated

* Now run "python manage.py migrate" to create the updated models in the database

## Django API Stuff

* If you want to access the python shell with django use "python manage.py shell"
* From here along with normal python things you can manually change database values using "from polls.models import Choice, Question"
* Nothing is changed in the actual database until save() is called

Example:

    In [1]: from polls.models import Choice, Question

    In [2]: Question.objects.all()
    Out[2]: <QuerySet []>

    In [3]: from django.utils import timezone

    In [4]: q = Question(question_text = "What's new?", pub_date=timezone.now())

    In [5]: q.save()

    In [6]: q.id
    Out[6]: 1

    In [7]: q.question_text
    Out[7]: "What's new?"

    In [8]: q.pub_date
    Out[8]: datetime.datetime(2018, 12, 3, 11, 30, 50, 542492, tzinfo=<UTC>)

    In [9]: q.question_text
    Out[9]: "What's new?"

    In [10]: q.save()

    Question.objects.all()
    Question.objects.filter(id=1)
    Question.objects.filter(question_text__startswith='What')

## Creating an admin user

run python manage.py createsuperuser and follow its instructions

To add models to the admin interface inside <appname>/admin.py add the following

    from .models import <Model>

    admin.site.register(<Model>)

## Writing Tests


* in <appname>/tests.py create a subclass of TestCase and give it methods that will be used as tests

    from django.test import TestCase

    import datetime

    from django.test import TestCase
    from django.utils import timezone

    from .models import Question


    class QuestionModelTests(TestCase):

        def test_was_published_recently_with_future_question(self):
            """
            was_published_recently() returns False for questions whose pub_date
            is in the future.
            """
            time = timezone.now() + datetime.timedelta(days=30)
            future_question = Question(pub_date=time)
            self.assertIs(future_question.was_published_recently(), False)

        def test_was_published_recently_with_old_question(self):
            """
            was_published_recently() returns False for questions whose pub_date
            is older than 1 day.
            """
            time = timezone.now() - datetime.timedelta(days=1,seconds=1)
            old_question = Question(pub_date=time)
            self.assertIs(old_question.was_published_recently(),False)