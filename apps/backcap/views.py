from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import update_object
from django.contrib.auth.decorators import login_required

from .models import Feedback
from .forms import FeedbackNewForm, FeedbackEditForm

@login_required
def feedback_new(request, referer=None):
    """
    Create a new feedback
    """
    if request.method == 'POST':
        feedback_form = FeedbackNewForm(request.POST)

        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user
            feedback.save()

            return redirect('backcap:feedback-thanks')
    else:
        feedback_form = FeedbackNewForm(initial={'referer': referer})

    return render_to_response(template_name='backcap/feedback_new.html',
                              dictionary={'feedback_form': feedback_form},
                              )

@login_required
def feedback_thanks(request):
    """
    Called when a feedback has been successfully submitted
    """
    return render_to_response(template_name='backcap/feedback_thanks.html')


# XXX: Security
def feedback_update(request, feedback_id):
    """
    Edit a single feedback
    """
    return update_object(request,
                         form_class=FeedbackEditForm,
                         object_id=feedback_id,
                         template_name='backcap/feedback_update.html',
                         )

def feedback_list(request, page=1):
    """
    Display all the feedbacks
    """
    return object_list(request,
                       queryset=Feedback.objects.exclude(status='C'),
                       template_name='backcap/feedback_list.html',
                       template_object_name='feedback',
                       paginate_by=7,
                       page=page,
                       )

def feedback_detail(request, feedback_id):
    """
    Shows a single feedback
    """
    return object_detail(request,
                         queryset=Feedback.objects.all(),
                         object_id=feedback_id,
                         template_object_name='feedback',
                         template_name='backcap/feedback_detail.html',
                         )

# XXX Security
def feedback_close(request, feedback_id):
    """
    Closes a feedback. This means it has been resolved.
    """
    feedback = get_object_or_404(Feedback, id=feedback_id)

    # Close it, then save
    feedback.status = 'C'
    feedback.save()

    return redirect(feedback)
        

from voting.views import vote_on_object

def feedback_vote(request, feedback_id, direction):
    return vote_on_object(request,
                          model=Feedback,
                          direction=direction,
                          object_id=feedback_id,
                          template_object_name='vote',
                          template_name='kb/link_confirm_vote.html',
                          allow_xmlhttprequest=True)
