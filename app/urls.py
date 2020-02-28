from django.urls import path

from . import views

urlpatterns = [
    #  renders
    path('', views.index),
    path('dashboard', views.job_dashboard),
    path('jobs/new', views.create),
    path('jobs/edit/<int:job_id>', views.edit_job),
    path('jobs/<int:job_id>', views.specific_job),
    # redirects
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('create_job', views.create_job),
    path('edit_job/<int:job_id>', views.edit),
    path('remove_job/<int:job_id>', views.delete),
    path('jobs/<int:single_job_id>/toggle_status', views.toggle_status),

    path('jobs/<int:job_id>', views.view_specific_job),
    # path('post', views.post)

]
