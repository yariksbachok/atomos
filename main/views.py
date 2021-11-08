from django.db.models import Count
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as log
from .models import *
from PIL import Image

def best_auth():
    best_authors = user_profile.objects.order_by('token_cost')[:5]
    return reversed(best_authors)

def find_username(message):
    for _ in message.split():
        print(message)
        if "@" in _:
            try:
                user = User.objects.get(username__iexact=_.split('@')[1])
                print(user.email)
                message = message.replace(_, f'[{_}](/profile/{user.username})')
            except:
                print(_, 'не найден')
    return message

def index(requests):
    if requests.user.is_authenticated:
        return redirect('/main')
    else:
        return render(requests, 'index.html')

def login(requests):
    if requests.method == "GET":
        return render(requests, 'login.html')
    elif requests.method == "POST":
        #try:
        try:
            user = authenticate(username=requests.POST['email'], password=requests.POST['psw'])
            log(requests, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/main')
        except:
            try:
                user = User.objects.get(email=requests.POST['email'])
                if user.check_password(requests.POST['psw']):
                    log(requests, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('/main')
                else:
                    error_message = 'Не верный пароль или логин.'
                    return render(requests, 'login.html', {'error_message': error_message})
            except:
                error_message = 'Не верный пароль или логин..'
                return render(requests, 'login.html', {'error_message': error_message})

def auth(requests):
    if requests.method == "GET":
        return render(requests, 'auth.html')
    elif requests.method == "POST":
        error_message = "Пользователь с таким ником уже зареестрирован"
        try:
            user = User.objects.create_user(requests.POST['email'], requests.POST['email'], requests.POST['psw'])
            user.save()
            session = authenticate(username=requests.POST['email'], password=requests.POST['psw'])
            log(requests, session)
            return render(requests, 'vk.html')
        except:
            return render(requests, 'auth.html', {'error_message': error_message})


@csrf_protect
def vk(requests):
    if requests.method == "POST":
        return render(requests, 'vk.html')

def end_reg(requests):
    if requests.method == "GET":
        if requests.user.is_authenticated:
            return render(requests, 'end_reg.html')
        else:
            return redirect('/login')
    elif requests.method == "POST":
        user = User.objects.get(id=requests.user.id)
        user.first_name = requests.POST['first_name']
        user.last_name = requests.POST['last_name']
        user.username = requests.POST['username']
        new_profile = user_profile(user=user)
        new_profile.save()
        user.save()

        return redirect('/main')


def log_out(requests):
    logout(requests)
    return redirect("/")


def main_news(requests):
    if requests.user.is_authenticated:
        if requests.user.first_name != "":
            post = all_posts.objects.filter(is_post=True)
            h_posts = hidden_posts.objects.filter(user=requests.user).values()
            h_posts = [item['post_id'] for item in list(h_posts)]
            like = [ like.post.id for like in requests.user.likes_set.all()]
            return render(requests, 'main.html', {'some_list': reversed(post), 'like': like,
                                                  'hidden': h_posts, 'best_authors': best_auth()})
        else:
            return redirect('/end_reg')
    else:
        return redirect('/login')

def publicate(requests, id):
    if requests.user.is_authenticated:
        if requests.method == "GET":
            if requests.user.first_name != "":
                post = all_posts.objects.get(id=id)
                like = likes.objects.filter(user=requests.user)
                comment = all_posts.objects.filter(is_post=False, parent=post)
                dout_comment = all_posts.objects.filter(is_post=False)
                h_posts = hidden_posts.objects.filter(user=requests.user).values()
                lk = []
                for l in like:
                    lk.append(l.post.id)
                return render(requests, 'post.html', {'i': post,'hidden':h_posts,'dout_comment': dout_comment,
                                                      'like': lk, 'comment':comment, 'best_authors':best_auth()})
            else:
                return redirect('/end_reg')

        if requests.method == "POST":
            message = find_username(requests.POST['message'])
            post = all_posts.objects.get(id=id)
            new_post = all_posts(owner=requests.user, message=message, is_post=False, parent=post)
            new_post.save()
            files = requests.FILES.getlist('termek_file')
            for i in files:
                img = PostImage(post=new_post, images=i)
                img.save()
            post.CommentCount = all_posts.objects.filter(parent=post).count()
            post.save()
            return redirect(f'/post/{id}')
    else:
        return redirect('/login')

def delPost(requests):
    post_id = requests.GET['post_id']
    all_posts.objects.get(id=post_id, owner=requests.user).delete()
    return HttpResponse('Post has been deleted')


def addComplain(requests):
    post_id = requests.GET['post_id']
    post = all_posts.objects.get(id=post_id)
    cp = complain(post=post, user=requests.user)
    cp.save()
    return HttpResponse('Post has been complain')


def addPost(requests):
    message = find_username(requests.POST['message'])
    new_post = all_posts(owner=requests.user, message=message)
    new_post.save()
    files = requests.FILES.getlist('termek_file')
    for i in files:
        img = PostImage(post=new_post, images=i)
        img.save()
    return redirect('/main')


def addLike(requests):
    post_id = requests.GET['post_id']
    post = all_posts.objects.get(id=post_id)
    try:
        like = likes.objects.get(post=post, user=requests.user)
        like.delete()
    except Exception as ex:
        like = likes(user=requests.user, post=post)
        like.save()
    post.likeCount = likes.objects.filter(post=post).count()
    post.save()
    return HttpResponse('sddsdsdsdsd')

def addHidePost(requests):
    post_id = requests.GET['post_id']
    post = all_posts.objects.get(id=post_id)
    user = requests.user
    hpost = hidden_posts(user=user, post=post)
    hpost.save()
    return HttpResponse('Post has been saved')


def notification(requests):
    if requests.user.is_authenticated:
        return render(requests, 'notification.html', {'best_authors':best_auth()})
    else:
        return redirect('/login')

def mention(requests):
    if requests.user.is_authenticated:
        posts = reversed(all_posts.objects.filter(message__contains=f"[@{requests.user.username}]"))
        return render(requests, 'mention.html', {'best_authors':best_auth(), 'posts':posts})
    else:
        return redirect('/login')


def settings(requests):
    if requests.method == 'GET':
        if requests.user.is_authenticated:
            return render(requests, 'settings.html', {'best_authors':best_auth()})
        else:
            return redirect('/login')
    if requests.method == 'POST':
        errors = []
        successful_messages = []
        username = requests.POST['username']
        name = requests.POST['name']
        email = requests.POST['email']
        old_psw = requests.POST['old_psw']
        new_psw = requests.POST['new_psw']
        if username:
            if( user_profile.objects.get(user=requests.user).is_username_changed):
                error = 'Username уже был изменен'
                errors.append(error)
            else:
                try:
                    User.objects.get(username=username)
                    error = f'Username {username} занят'
                    errors.append(error)
                except:
                    user = User.objects.get(id=requests.user.id)
                    user.username = username
                    user.save()
                    profile = user_profile.objects.get(user=requests.user)
                    profile.is_username_changed = True
                    profile.save()
                    message = 'Username успешно изменен'
                    successful_messages.append(message)
        if name:
            name = name.split(' ')
            if len(name) != 2:
                error = 'Введите имя и фамилию в формате Имя Фамилия'
                errors.append(error)
            else:
                user = User.objects.get(id=requests.user.id)
                user.first_name = name[0]
                user.last_name = name[1]
                user.save()
                message = 'Имя и фамилия были успешно изменены'
                successful_messages.append(message)
        if email:
            try:
                User.objects.get(email=email)
                error = 'Указаный email уже занят'
                errors.append(error)
            except:
                user = User.objects.get(id=requests.user.id)
                user.email=email
                user.save()
                message = 'Email был успешно изменен'
                successful_messages.append(message)
        if old_psw:
            user = User.objects.get(id=requests.user.id)
            if user.check_password(old_psw):
                if new_psw:
                    if user.check_password(new_psw):
                        error = 'Вы ввели старый пароль'
                        errors.append(error)
                    else:
                        user.set_password(new_psw)
                        user.save()
                        message = 'Пароль был успешно изменен'
                        successful_messages.append(message)
                else:
                    error = 'Введите новый пароль'
                    errors.append(error)
            else:
                error = 'Неправильный пароль'
                errors.append(error)
        if new_psw:
            if not old_psw:
                error = 'Введите старый пароль'
                errors.append(error)
        if errors:
            return render(requests, 'settings.html', {'best_authors':best_auth(), 'errors':errors,
                                                      'messages':successful_messages})
        if messages:
            return render(requests, 'settings.html', {'best_authors':best_auth(), 'errors':errors, 'messages':successful_messages})
        return redirect('/settings')

def wallet(requests):
    if requests.user.is_authenticated:
        return render(requests, 'wallet.html', {'best_authors':best_auth()})
    else:
        return redirect('/login')

def profile(requests, username):
    if requests.user.is_authenticated:
        profile = User.objects.get(username=username)
        post = all_posts.objects.filter(is_post=True, owner=profile, is_pinned=False)
        pinned = all_posts.objects.filter(is_pinned=True, owner=profile)
        like = likes.objects.filter(user=requests.user)
        lk = []
        for l in like:
            lk.append(l.post.id)
        return render(requests, 'profile.html', {'profile':profile, 'some_list': reversed(post),
                                                 'like': lk,'best_authors':best_auth(), 'pinned':pinned })
    else:
        return redirect('/login')

def pin(requests):
    post_id = requests.GET['id']
    post = all_posts.objects.get(id=post_id)
    try:
        if all_posts.objects.get(owner=requests.user, is_pinned=True) != post:
            pass
        else:
            post.is_pinned = False
            post.save()
    except:
        post.is_pinned = True
        post.save()
    return HttpResponse('done')

def exchange(requests):
    if requests.user.is_authenticated:
        n = 3
        profiles = list(reversed(user_profile.objects.order_by('token_cost')))[:n]
        return render(requests, 'exchange.html', {'all_people': profiles,'best_authors':best_auth()})
    else:
        return redirect('/login')

def ex_show_more(requests):
    count_exist = int(requests.GET['count'])
    n = 3
    profiles = user_profile.objects.order_by('token_cost')
    profiles = profiles[::-1][count_exist:count_exist + n]
    rendered_profiles = []
    for profile in profiles:
        rendered_profile = render_to_string('patterns/one_profile.html', {'i': profile})
        rendered_profiles.append(rendered_profile)
    return JsonResponse(rendered_profiles, safe=False)


def search(requests):
    if requests.user.is_authenticated:
        n = 3
        all_people = list(reversed(user_profile.objects.all()))[:n]
        return render(requests, 'search.html', {'all_people':all_people,'best_authors':best_auth()})
    else:
        return redirect('/login')


def search_show_more(requests):
    count_exist = int(requests.GET['count'])
    n = 2
    profiles = user_profile.objects.all()
    profiles = profiles[::-1][count_exist:count_exist + n]
    rendered_profiles = []
    for profile in profiles:
        print(profile)
        rendered_profile = render_to_string('patterns/one_profile.html', {'i': profile})
        rendered_profiles.append(rendered_profile)
    print(profiles)
    return JsonResponse(rendered_profiles, safe=False)

def search_profile(requests):
    search_value = requests.GET['value'].lower()
    profiles = user_profile.objects.all()
    found_profiles = []
    for profile in profiles:
        name = str(profile.user.first_name) + " " + str(profile.user.last_name)
        name = name.lower()
        if search_value in name:
            found_profiles.append(profile)
    rendered_profiles = []
    for profile in found_profiles:
        rendered_profile = render_to_string('patterns/one_profile.html', {'i':profile})
        rendered_profiles.append(rendered_profile)
    return JsonResponse(rendered_profiles, safe=False)

def search_post(requests):
    search_value = requests.GET['value'].lower()
    posts = all_posts.objects.filter(message__icontains=search_value)
    like = [ like.post.id for like in requests.user.likes_set.all()]
    rendered_posts = []
    for post in posts:
        rendered_post = render_to_string('patterns/block_comments.html', {'i': post, 'like': like})
        rendered_posts.append(rendered_post)
    return JsonResponse(rendered_posts, safe=False)


def publications(requests):
    if requests.user.is_authenticated:
        posts = reversed(all_posts.objects.all()[:5])
        like = [like.post.id for like in requests.user.likes_set.all()]
        return render(requests, 'publications.html', {'best_authors':best_auth(), 'profile_list': posts, 'like':like})
    else:
        return redirect('/login')

def fill_buy_popup(requests):
    id = int(requests.GET['id'])
    profile = model_to_dict(user_profile.objects.get(id=id))
    response_profile = {
        'id': profile['id'],
        'user': profile['user'],
        'balance': profile['balance'],
        'token_cost': profile['token_cost'],
        'balance': profile['token_cost'],
        'procent': profile['procent'],
    }
    user = model_to_dict(User.objects.get(id=profile['user']))
    user = clean_user(user)
    response_profile['user'] = user
    return JsonResponse(response_profile, safe=False)

def publications_show_more(requests):
    count_exist = int(requests.GET['count'])
    n = 1
    posts = all_posts.objects.all()[count_exist:count_exist + n]
    posts = reversed(posts)
    like = [like.post.id for like in requests.user.likes_set.all()]
    rendered_posts = []
    for post in posts:
        rendered_post = render_to_string('patterns/block_comments.html', {'i':post, 'like':like})
        rendered_posts.append(rendered_post)
    return JsonResponse(rendered_posts, safe=False)

def clean_user(user):
    user = user.copy()
    del user['password']
    del user['last_login']
    del user['is_superuser']
    del user['is_staff']
    del user['is_active']
    del user['date_joined']
    del user['groups']
    del user['user_permissions']
    return user

def messages(requests, id):
    if not requests.user.is_authenticated:
        return redirect('/login')
    user = requests.user
    chats = chat.objects.filter(user=user).order_by('-data')
    chat_users = []
    for c in chats:
        u = c.user.all().exclude(id=user.id)
        if u:
            chat_users.append(u[0])
    if int(id) == 0:
        return render(requests, 'messages.html',
                      {'chat_users': chat_users, 'messages': [], 'to_user': {}, 'user': user})
    to_user = User.objects.get(id=id)
    users = [user, to_user]
    msg = []
    try:
        current_chat = chat.objects.filter(user__in=users).annotate(num_user=Count('user')).filter(num_user=len(users))[0]
        msg = current_chat.messages.all()
    except Exception as e:
        current_chat = chat.objects.create()
        current_chat.user.add(users[0])
        current_chat.user.add(users[1])
        current_chat.save()
    avatars = {
        'to_user' : to_user.profile.get().avatar,
        'user' : user.profile.get().avatar
    }
    context = {'chat_users':chat_users, 'messages':msg, 'to_user':to_user, 'user':user, 'avatars': avatars}
    return render(requests, 'messages.html', context)


def api_save_photo_profile(requests):
    try:
        if requests.method == 'POST':
            files = requests.FILES['termek_file']
            left = str(requests.POST['left']).rstrip('px')
            top = str(requests.POST['top']).rstrip('px')
            width = str(requests.POST['width']).rstrip('px')
            height = str(requests.POST['height']).rstrip('px')
            if files:
                us = User.objects.get(id=requests.user.id)
                try:
                    new = user_profile.objects.get(user=us)
                    new.avatar = files
                    new.save()
                except:
                    new_photo = user_profile(user = us, avatar=files)
                    new_photo.save()
                st = str(files)
                im = Image.open('main/static/media/avatars/' + st)
                left = int(left) - 100
                top = int(top) - 100
                box = (left, top, left+int(width), top+int(height))
                resized_img = im.resize((500, 281), Image.ANTIALIAS)
                im_crop = resized_img.crop(box)
                im_crop.save('main/static/media/avatars/'+st, quality=95)
                return redirect('/settings')

    except Exception as e:
        print(e)
        return redirect('/settings')

def api_change_back_photo(requests):
    try:
        if requests.method == 'POST':
            files = requests.FILES['termek_file']
            if files:
                l = (requests.POST['top']).rstrip('px')
                top = int(l) - 100
                bottom = top + 100
                print(top, bottom)
                print('==================================================================')
                us = User.objects.get(id=requests.user.id)
                try:
                    new = user_profile.objects.get(user=us)
                    new.background = files
                    new.save()
                except:
                    new_photo = user_profile(user = us, background=files)
                    new_photo.save()
                st = str(files)
                im = Image.open('main/static/media/avatars/' + st)
                box = (0, top, 600, bottom)
                resized_img = im.resize((600, 400), Image.ANTIALIAS)
                im_crop = resized_img.crop(box)
                im_crop.save('main/static/media/avatars/' + st, quality=95)
                return redirect('/profile/'+requests.user.username)
        else:
            return redirect('/profile/'+requests.user.username)
    except Exception as e:
        print(e)
        return redirect('/profile/'+requests.user.username)

def change_main_photo(requests):
    if requests.user.is_authenticated:
        return render(requests, 'main_photo.html')

def main_backraund(requests):
    if requests.user.is_authenticated:
        return render(requests, 'main_backgraund.html')