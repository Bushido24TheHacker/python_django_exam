from django.shortcuts import render, redirect
from .models import *
import bcrypt


# renders start here-----

def index(request):

    return render(request, 'index.html')


def job_dashboard(request):
    user_in_session = User.objects.get(
        email=request.session['email_session_id'])
    context = {

        'user': user_in_session,
        'jobs_to_add': Job.objects.filter(jobs_to_add=True),
        'jobs_to_remove': Job.objects.filter(jobs_to_add=False),

    }
    return render(request, 'job_dashboard.html', context)


def create(request):
    user_in_session = User.objects.get(
        email=request.session['email_session_id'])

    context = {
        'user': user_in_session,

    }
    return render(request, 'create.html', context)


def edit_job(request, job_id):
    user_in_session = User.objects.get(
        email=request.session['email_session_id'])
    context = {
        'job': Job.objects.get(id=job_id),
        'user': user_in_session
    }

    return render(request, 'edit_job.html', context)


def specific_job(request, job_id):
    user = User.objects.get(email=request.session['email_session_id'])

    context = {
        'user': user,
        'job': Job.objects.get(id=job_id)



    }

    return render(request, 'view_job.html', context)
# redirect functions------


def register(request):
    user_errors = User.objects.user_validator(request.POST)
    if len(user_errors) > 0:
        for key, value in user_errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hashed_pw = bcrypt.hashpw(
            request.POST["password"].encode(), bcrypt.gensalt()).decode()
    print("hashed_pw:", hashed_pw)
    new_user = User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=hashed_pw
    )
    request.session["email_session_id"] = new_user.email
    return redirect('/dashboard')


def login(request):
    user_list = User.objects.filter(email=request.POST["email"])
    if len(user_list) == 1:
        print("We found User")
        print(user_list[0].password)
        print(request.POST)
        if bcrypt.checkpw(request.POST["password"].encode(), user_list[0].password.encode()):
            print("password match")
            request.session["email_session_id"] = user_list[0].email
            return redirect("/dashboard")
        else:
            print("password failed")
            messages.error(request, "password failed")
            return redirect("/")
    else:
        print("no user with that email")
        messages.error(request, "no user with that email")
        return redirect('/')


def logout(request):
    request.session.clear()

    return redirect('/')


def create_job(request):
    job_errors = Job.objects.job_validator(request.POST)
    if len(job_errors) > 0:
        for key, value in job_errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else:

        Job.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            category=request.POST['category'],
            user=User.objects.get(email=request.session['email_session_id'])

        )

    return redirect('/dashboard')


def edit(request, job_id):
    edit_errors = Job.objects.edit_validator(request.POST)
    if len(edit_errors) > 0:
        for key, value in edit_errors.items():
            messages.error(request, value)
        return redirect(f'/jobs/edit/{job_id}')
    else:
        job_to_edit = Job.objects.get(id=job_id)
        job_to_edit.title = request.POST['title']
        job_to_edit.description = request.POST['description']
        job_to_edit.location = request.POST['location']
        job_to_edit.save()

    return redirect('/dashboard')


def delete(request, job_id):
    job_to_delete = Job.objects.get(id=job_id)
    job_to_delete.delete()
    return redirect('/dashboard')


# def granted_wish(request, wish_id):
#     batmans_idea = Wish.objects.get(id=wish_id)
#     batmans_idea.wish_granted = True
#     batmans_idea.save()

#     return redirect('/wishes')


# def like_wish(request, wish_id):
#     user = User.objects.get(
#         email=request.session["email_session_id"])
#     wish_to_like = Wish.objects.get(id=wish_id)
#     wish_to_like.users_who_liked.add(user)
#     return redirect('/wishes')


def toggle_status(request, single_job_id):
    print('toggle_status')
    job_to_toggle_status = Job.objects.get(id=single_job_id)
    print(job_to_toggle_status.title)
    print(job_to_toggle_status.jobs_to_add)

    if job_to_toggle_status.jobs_to_add == True:
        print('job added')
        job_to_toggle_status.jobs_to_add = False
        print('job removed')
    else:
        job_to_toggle_status.jobs_to_add = True

    # dog_to_toggle_status.is_good = not dog_to_toggle_status.is_good
    print(job_to_toggle_status.jobs_to_add)
    job_to_toggle_status.save()

    return redirect('/dashboard')


def view_specific_job(request, job_id):

    return redirect(f'/jobs/{job_id}')


# def post(self):
#     adjectives = self.request.get('adjective', allow_multiple=True)
#     for a in adjectives:
#         # increment count
#         self.adjective_count[a] += 1  # or whatever

#     return redirect('/create_job')
