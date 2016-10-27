from django.shortcuts import render, redirect, HttpResponse
from .models import Users, Quotes, Join
from django.contrib import messages

# Create your views here.
def index(request):
    # Users= Users.registerManager.all().delete()
    # Users2= Users.loginManager.all().delete()
    # Trip= Trips.tripManager.all().delete()
    # Join= Join.objects.all().delete()
    return render(request, 'belt2/index.html')

def register(request):
    result = Users.registerManager.register(request.POST['name'], request.POST['username'], request.POST['email'], request.POST['password'], request.POST['password_confirmation'])
    if result[0]:
        request.session['user_id']=result[2]
        request.session['name']=result[1].name
        print result[1].name
        return redirect('/dashboard')
    else:
        for x in xrange(len(result[1])):
            messages.error(request, result[1][x])
        return redirect('/')

def login(request):
    print request.POST
    result = Users.loginManager.login(request.POST['email_login'], request.POST['password_login'])
    name = Users.loginManager.filter(email=request.POST['email_login'])
    if len(name) >0:
        name = name[0].name
        request.session['name']=name
    #     print name
    if result[0]:
        request.session['user_id']=result[2]
        print result[2]
        return redirect('/dashboard')
    else:
        for x in xrange(len(result[1])):
            messages.error(request, result[1][x])
        return redirect('/')

def logout(request, id):
    request.session.pop('user_id')
    request.session.pop('email_login')
    request.session.clear()
    return redirect('/')

def dashboard(request):
    quote = Quotes.quoteManager.filter(user_id=request.session.get('user_id'))
    other_quotes = Quotes.quoteManager.exclude(user_id=request.session.get('user_id'))
    join = Join.objects.filter(user_id=request.session['user_id'])
    print quote
    for x in join:
        other_quotes = other_quotes.exclude(id=x.quote.id)
    context = {
    'quote':quote,
    'other_quotes':other_quotes,
    'join' : join
    }
    return render(request, 'belt2/dashboard.html', context)

def addquote(request):
    if request.method == 'GET':
        print request.session.get('user_id')
        return render(request, 'belt2/addquote.html')
    elif request.method == 'POST':
        # print "New Quote"
        quote = Quotes.quoteManager.addquote(creator=request.POST['creator'], message=request.POST['message'], user_id= request.session.get('user_id'))
        if quote[0]:
            quote = Quotes.quoteManager.create(creator=request.POST['creator'], message=request.POST['message'], user_id= request.session.get('user_id'))
            join= Join.objects.create(quote_id=quote.id, user_id=request.session['user_id'])
            quote.save()
            return redirect('/dashboard')
        else:
            for x in xrange(len(quote[1])):
                messages.error(request, quote[1][x])
                return redirect('/addquote')

def user(request, quote_id):
    join = Join.objects.filter(quote_id=quote_id)
    context={
    'join':join,
    'quote':Quotes.quoteManager.filter(id=quote_id)
    }
    return render(request, 'belt2/quotes.html', context)

# so you cant add a quote more than once
def join(request, quote_id):
    measure = Join.objects.filter(quote_id=quote_id).filter(user_id=request.session['user_id'])
    if len(measure)==0:
        join = Join.objects.create(user_id=request.session['user_id'], quote_id=quote_id)
    return redirect('/dashboard')
