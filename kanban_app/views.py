from django.shortcuts import render, redirect
from .models import user, board, columns, card
from django.contrib import messages
import bcrypt

# Create your views here.

def landing(request):
    print('session user id:', request.session['user_id'], 'session board id:', request.session['board_id'])
    if 'user_id' not in request.session:
        return redirect('/info')
    else:
        return redirect('/complete')

def signup(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "GET":
        return redirect('/info')

    errors = user.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/info')

    password = request.POST['pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    

    new_user = user.objects.create(
        first_name = request.POST['fname'],
        last_name = request.POST['lname'],
        username = request.POST['uname'],
        email = request.POST['email'],
        password = pw_hash
    )
    request.session['user_id'] = new_user.id

    print('password:', password, new_user.first_name, new_user.email)

    new_board = board.objects.create(
        title = "New Project Board",
        created_by = user.objects.get(id=new_user.id),
    )

    request.session['board_id'] = new_board.id

    first_column = columns.objects.create(
        title = "Work to Do",
        created_by = user.objects.get(id=new_user.id),
        board = board.objects.get(id=new_board.id)
    )

    first_card = card.objects.create(
        subject = "Create Cards",
        content = "Make cards to keep track of a task or job that needs to be done.",
        created_by = user.objects.get(id=new_user.id),
        status = columns.objects.get(id=first_column.id),
        # owners = user.objects.get(id=new_user.id),
    )
    
    second_card = card.objects.create(
        subject = "Cards for the Tasks",
        content = "Put in your tasks to keep track of what you need to do and what is done.",
        created_by = user.objects.get(id=new_user.id),
        status = columns.objects.get(id=first_column.id),
        # owners = user.objects.get(id=new_user.id),
    )
    return redirect('/complete')



def home(request):
    if 'user_id' not in request.session:
        return redirect('/info')

    if 'board_id' not in request.session:
        return redirect('/select')

    User = user.objects.get(id=request.session['user_id'])
    home_board = board.objects.get(id=request.session['board_id'])
    columns = home_board.columns.all()

    context = {
        'user' : User,
        'board' : home_board,
        'Columns' : columns
    }
    return render(request, 'home.html', context)


def reenter(request):
    if request.method == 'GET':
        return redirect('/info')

    email = request.POST['email']
    password = request.POST['pw']

    if not user.objects.authenticate(email, password):
        messages.error(request, "Invalid email or password")
        return redirect('/info')

    User = user.objects.get(email=email)
    request.session['user_id'] = User.id

    print('user id#', User.id)
    return redirect('/select')


def select(request):
    if 'user_id' not in request.session:
        return redirect('/')

    User = user.objects.get(id=request.session['user_id'])
    myboards = board.objects.filter(created_by=User)

    context = {
        'user' : User,
        'boards' : myboards
    }

    return render(request, 'select.html', context)

def home_sesh(request, board_id):
    request.session['board_id'] = board_id
    return redirect('/complete')




# board actions ------------------------------------------

def create_board(request):
    pass

def edit_board(request):
    pass

def add_group(request):
    pass

# column actions ------------------------------------------

def create_column(request):
    pass

def edit_column(request):
    pass


# card actions --------------------------------------------

def create_card(request):
    pass

def edit_card(request):
    pass

def move_card(request):
    pass



# profile actions -----------------------------------------

def profile(request):
    pass

def edit_about(request):
    pass

def edit_info(request):
    pass


# logout ----------------------------------------------------

def logout(request):
    request.session.clear()
    return redirect('/info')
