from django.shortcuts import render
from Task.forms import AddTask
from .toolbox import tools
from django.contrib.auth.decorators import login_required



def reform_post_data(r_post):
    tools.logger.debug(r_post['nm_Id'])
    tools.logger.debug(r_post['new_name'])
    nm_Id = r_post['nm_Id'] 
    new_name = r_post['new_name'] 
    if nm_Id.isnumeric():
        nm_Id = int(nm_Id)
    else:
        raise TypeError('Id must be the number')
    return {
        'new_name': new_name,
        'nm_Id': nm_Id,
    }

@login_required
def make_task(request):
    error_message = ''
    success_message = ''
    if request.method == 'POST':
        r_post = request.POST
        print(r_post)
        try:
            r_post = reform_post_data(r_post)
            tools.change_name(**r_post)
            success_message = 'Переименовано!'
        except Exception as e:
            tools.logger.error(e)
            print('\t'+f"{error_message = }")
            error_message = str(e)
            print('\t'+f"{error_message = }")

    context = {'form': AddTask(), 'error_message': error_message, 'success_message': success_message}
    return render(request, 'Task/make_task.html', context=context)
