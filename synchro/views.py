from cStringIO import StringIO

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.response import TemplateResponse
from django.core.management import call_command

from synchro import reset_synchro
from synchro.models import options


@staff_member_required
def synchro(request):
    if 'synchro' in request.POST:
        so = StringIO()
        try:
            call_command('synchronize', stdout=so)
            messages.add_message(request, messages.INFO, so.getvalue())
        except Exception as e:
            msg = 'An error occured: %s (%s)' % (str(e), e.__class__.__name__)
            messages.add_message(request, messages.ERROR, msg)
        finally:
            so.close()
    elif 'reset' in request.POST:
        reset_synchro()
        msg = 'Synchronization has been reset.'
        messages.add_message(request, messages.INFO, msg)
    return TemplateResponse(request, 'synchro.html', {'last': options.last_check})
