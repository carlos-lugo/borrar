import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views import View
from wr.models import ReportIndexList


class WrPortfolioView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = request.user.last_login.today()

        members = ReportIndexList.objects.distinct().values_list('team_member').values(
            'user',
            'user__id',
            'user__name',
            'user__email',
        )
        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'members': members,
        }

        return TemplateResponse(request, 'wr/portfolio.html', context)
