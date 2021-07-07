from django.shortcuts import render, redirect
from .models import user, board, columns, card
from django.contrib import messages
import bcrypt

# Create your views here.

def landing(request):
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

    # print('password:', password, new_user.first_name, new_user.email)

    new_board = board.objects.create(
        title = "New Project Board",
        created_by = user.objects.get(id=new_user.id),
    )

    request.session['board_id'] = new_board.id

    # create starter columns and cards
    first_column = columns.objects.create(
        title = "Work to Do",
        created_by = user.objects.get(id=new_user.id),
        board = board.objects.get(id=new_board.id),
        color = 'orange'
    )
    first_card = card.objects.create(
        subject = "Create Cards",
        content = "Make cards to keep track of a task or job that needs to be done.",
        created_by = user.objects.get(id=new_user.id),
        status = columns.objects.get(id=first_column.id),
        # owners = user.objects.get(id=new_user.id),
    )
    second_card = card.objects.create(
        subject = "Drag and Drop-ability",
        content = "You can take your task cards in one column and put them in another column to better organize your work.",
        created_by = user.objects.get(id=new_user.id),
        status = columns.objects.get(id=first_column.id),
        # owners = user.objects.get(id=new_user.id),
    )
    next_column = columns.objects.create(
        title = "Work in Progress",
        created_by = user.objects.get(id=new_user.id),
        board = board.objects.get(id=new_board.id),
        color = 'yellow'
    )
    done_column = columns.objects.create(
        title = "Work Done",
        created_by = user.objects.get(id=new_user.id),
        board = board.objects.get(id=new_board.id),
        color = 'lime-green'
    )
    return redirect('/complete')



def home(request):
    if 'user_id' not in request.session:
        return redirect('/info')

    if 'board_id' not in request.session:
        return redirect('/select')

    User = user.objects.get(id=request.session['user_id'])
    home_board = board.objects.get(id=request.session['board_id'])
    # columns = home_board.columns.all()

    context = {
        'user' : User,
        'board' : home_board,
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
        return redirect('/info')

    User = user.objects.get(id=request.session['user_id'])
    myboards = board.objects.filter(created_by=User)

    context = {
        'user' : User,
        'boards' : myboards
    }
    return render(request, 'select.html', context)


def list(request):
    userslist = user.objects.all()
    User = user.objects.get(id=request.session['user_id'])
    context = {
        'user' : User,
        'friends' : userslist
    }
    return render(request, 'friends.html', context)

def home_sesh(request, board_id):
    request.session['board_id'] = board_id
    return redirect('/complete')


# board actions ------------------------------------------

def create_board(request):
    if request.method == 'GET':
        return redirect('/select')

    User = user.objects.get(id=request.session['user_id'])
    new_board = board.objects.create(
        title = request.POST['projectname'],
        created_by = User
    )

    request.session['board_id'] = new_board.id
    init_board = board.objects.get(id=request.session['board_id'])
    
    first_column = columns.objects.create(
        title = "Work to Do",
        created_by = User,
        board = init_board,
        color = 'orange'
    )
    work_col = columns.objects.get(id=first_column.id)
    first_card = card.objects.create(
        subject = "Create Cards",
        content = "Make cards to keep track of a task or job that needs to be done.",
        created_by = User,
        status = work_col,
    )
    second_card = card.objects.create(
        subject = "Drag and Drop-ability",
        content = "You can take your task cards in one column and put them in another column to better organize your work.",
        created_by = User,
        status = work_col,
    )
    columns.objects.create(
        title = "In Progress",
        created_by = User,
        board = init_board,
        color = 'yellow'
    )
    columns.objects.create(
        title = "Done",
        created_by = User,
        board = init_board,
        color = 'lime-green'
    )
    return redirect('/complete')


def edit_board(request, board_id):
    if request.method == 'GET':
        return redirect('/complete')

    project = board.objects.get(id=board_id)
    project.title = request.POST['boardname']
    project.save()
    return redirect('/complete')


def add_group(request):
    pass

def delete_board(request, board_id):
    if request.method == 'GET':
        return redirect('/select')
    
    elim_board = board.objects.get(id=board_id)
    elim_board.delete()
    return redirect('/select')

# column actions ------------------------------------------

def create_column(request, board_id):
    if request.method == 'GET':
        return redirect('/complete')

    errors = columns.objects.nonull(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/complete')

    inboard = board.objects.get(id=board_id)
    thisuser = user.objects.get(id=request.session['user_id'])
    columns.objects.create(
        title = request.POST['coltitle'],
        created_by = thisuser,
        board = inboard,
        color = request.POST['colorize']
    )
    return redirect('/complete')

def edit_column(request, column_id):
    if request.method == 'GET':
        return redirect('/complete')

    errors = columns.objects.nonull(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/complete')

    editcol = columns.objects.get(id=column_id)
    editcol.title = request.POST['coltitle']
    editcol.color = request.POST['colorize']
    editcol.save()
    return redirect('/complete')

def delete_column(request, column_id):
    if request.method == 'GET':
        return redirect('/complete')
    dropcol = columns.objects.get(id=column_id)
    dropcol.delete()
    return redirect('/complete')


# card actions --------------------------------------------

def create_card(request, column_id):
    if request.method == 'GET':
        return redirect('/complete')

    errors = card.objects.validatecard(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/complete')

    thisuser = user.objects.get(id=request.session['user_id'])
    incol = columns.objects.get(id=column_id)

    card.objects.create(
        subject = request.POST['cardname'],
        content = request.POST['info'],
        created_by = thisuser,
        status = incol
    )
    return redirect('/complete')


def edit_card(request, card_id):
    if request.method == 'GET':
        return redirect('/complete')

    errors = card.objects.validatecard(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/complete')
    
    editcard = card.objects.get(id=card_id)
    editcard.subject = request.POST['cardname']
    editcard.content = request.POST['info']
    editcard.save()
    return redirect('/complete')

def move_card(request):
    if request.method == 'GET':
        return redirect('/complete')
    # print(f'card number {card_id} has moved')
    card_id = request.POST['cardid']
    col_id = request.POST['column']
    # print('card id:',card_id , 'column id:',col_id)
    card_moved = card.objects.get(id=card_id)
    column_receive = columns.objects.get(id=col_id)
    card_moved.status = column_receive
    card_moved.save()
    return redirect('/complete')

def delete_card(request, card_id):
    if request.method == 'GET':
        return redirect('/complete')
    
    card_elim = card.objects.get(id=card_id)
    card_elim.delete()
    return redirect('/complete')


# profile actions -----------------------------------------

def profile(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/info')

    view_user = user.objects.get(id=user_id)
    logged_in = user.objects.get(id=request.session['user_id'])
    context = {
        'thisuser' : view_user,
        'user' : logged_in
    }
    return render(request, 'profile.html', context)

def edit_about(request, user_id):
    if request.method == 'GET':
        return redirect(f'/profile/{user_id}')
    
    user_edit = user.objects.get(id=user_id)
    user_edit.about_me = request.POST['aboutme']
    user_edit.save()
    return redirect(f'/profile/{user_id}')
    

def edit_info(request, user_id):
    if request.method == 'GET':
        return redirect(f'/profile/{user_id}')

    errors = user.objects.editvalid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/profile/{user_id}')

    user_info = user.objects.get(id=user_id)
    user_info.first_name = request.POST['fname']
    user_info.last_name = request.POST['lname']
    user_info.username = request.POST['uname']
    user_info.email = request.POST['email']
    user_info.save()
    return redirect(f'/profile/{user_id}')

def edit_pw(request, user_id):
    pass
#     if request.method == 'GET':
#         return redirect(f'/profile/{user_id}')
    
#     User = user_id
#     verify = request.POST['pwcheck']

#     if not user.objects.checkpoint(User, verify):
#         messages.error(request, "Password is incorrect")
#         return redirect(f'/profile/{user_id}')

#     newpassword = request.POST['newpassword']
#     matchnew = request.POST['matchpassword']

#     errors = user.objects.multipass(newpassword, matchnew)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect(f'/profile/{user_id}')

#     pw_hash = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt()).decode()

#     userpw = user.objects.get(id=user_id)
#     userpw.password = pw_hash
#     userpw.save()
#     return redirect(f'/profile/{user_id}')



# password = request.POST['pw']
    # pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
#     new_user = user.objects.create(
#         first_name = request.POST['fname'],
#         last_name = request.POST['lname'],
#         username = request.POST['uname'],
#         email = request.POST['email'],
#         password = pw_hash
#     )

    # if not user.objects.authenticate(email, password):
    #     messages.error(request, "Invalid email or password")
    #     return redirect('/info')


# logout ----------------------------------------------------

def logout(request):
    request.session.clear()
    return redirect('/info')
