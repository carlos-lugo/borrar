import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views import View
from django.db.models import F
from wr.models import WeeklyReport, ReportIndexList


class WrPortfolioDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        today = request.user.last_login.today()
        indexes = []

        for index in ReportIndexList.objects.filter(user__id=pk).order_by('report_date'):
            indexes.append(
                {'report_date': index.report_date,
                 'team_member': index.team_member,
                 'team': index.team,
                 'user': index.user,
                 'reports': WeeklyReport.objects.filter(member=index.team_member, report_date=index.report_date).order_by('report_date', F('type').desc(nulls_last=True), 'created_date'),
                 }
            )

        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'indexes': indexes,
            'target': indexes[0]['user'],
            'back': 'portfolio',
        }

        return TemplateResponse(request, 'wr/detail.html', context)
