import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views import View
from wr.forms import WrSearchForm
from wr.models import ReportIndexList
from django.template.context_processors import csrf


class WrSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = request.user.last_login.today()
        report_index = ReportIndexList.objects.all()
        form = WrSearchForm()

        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'reports': report_index.order_by('-report_date', 'team', 'user'),
            'form': form,
        }

        # CFRF対策（必須）
        context.update(csrf(request))
        return TemplateResponse(request, 'wr/search.html', context)

    def post(self, request, *args, **kwargs):
        # リクエストパラメータからフォームを作成
        today = request.user.last_login.today()
        report_index = ReportIndexList.objects.all().order_by('-report_date', 'team', 'user')

        form = WrSearchForm(request.POST)
        q_teams = request.POST.getlist('team')
        q_name = request.POST.get('name')
        q_date = request.POST.get('date')

        # チームでの絞り込み
        if len(q_teams) != 0:
            report_index = report_index.filter(team__in=q_teams)

        # 名前での絞り込み
        if q_name is not None and q_name > '':
            report_index = report_index.filter(user__name__contains=q_name)

        # 報告日での絞り込み
        if q_date is not None and q_date > '':
            q_dt = datetime.datetime.strptime(q_date, '%Y/%m/%d')
            q_dt = q_dt - datetime.timedelta(days=q_dt.weekday())
            report_index = report_index.filter(report_date=q_dt)

        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'reports': report_index.order_by('-report_date', 'team', 'user'),
            'form': form,
        }

        return TemplateResponse(request, 'wr/search.html', context)
