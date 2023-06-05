import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.template.response import TemplateResponse
from django.views import View
from django.db.models import Q
from user.models import TeamMember


class WrTopView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        today = request.user.last_login.today()
        try:
            status = TeamMember.objects.get(user=request.user, end_date=None)
        except TeamMember.DoesNotExist:
            raise Http404

        history = TeamMember.objects.filter(Q(user=request.user, can_reply__gt=0), Q(end_date=None) | Q(end_date__gte=today - datetime.timedelta(days=30)))
        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'report': status.can_report,
            'reply': history.exists(),
        }
        return TemplateResponse(request, 'wr/top.html', context)
