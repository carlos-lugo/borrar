import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views import View
from django.db.models import Q, F
from wr.forms import WrReplyForm
from wr.models import WeeklyReport
from user.models import TeamMember, Team


class WrReplyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = WrReplyForm()
        today = request.user.last_login.today()
        history = TeamMember.objects.filter(Q(user=request.user, can_reply__gt=0), Q(end_date=None) | Q(end_date__gte=today - datetime.timedelta(days=30)))
        if not history.exists():
            return HttpResponseRedirect('/wr')

        # 返信対象者取得サンプル
        where = []
        for tm in history:
            if tm.can_reply == 1:
                where.append(tm.team)
            elif tm.can_reply > 1 and Team.objects.filter(Q(start_date__lte=today), Q(end_date=None) | Q(end_date__gte=today)).exists():
                for t in Team.objects.filter(Q(start_date__lte=today), Q(end_date=None) | Q(end_date__gte=today)):
                    where.append(t)

        if history.filter(can_reply__gt=1).exists():
            teams = TeamMember.objects.all().order_by(F('team'), F('end_date').desc(nulls_last=False), F('team__end_date').desc(nulls_last=False), 'user')
        else:
            teams = TeamMember.objects.filter(team__in=history.distinct().values_list('team')).order_by(F('team'), F('end_date').desc(nulls_last=False), F('team__end_date').desc(nulls_last=False), 'user')

        form.fields["member"].choices = ((x.id, f'{x.team.name} {x.user.name}  {x.start_date} - {x.end_date or ""}') for x in teams)

        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'form': form,
        }
        return TemplateResponse(request, 'wr/reply.html', context)

    def post(self, request, *args, **kwargs):
        form = WrReplyForm(request.POST)
        today = request.user.last_login.today()
        history = TeamMember.objects.filter(Q(user=request.user, can_reply__gt=0), Q(end_date=None) | Q(end_date__gte=today - datetime.timedelta(days=30)))

        if history.filter(can_reply__gt=1).exists():
            teams = TeamMember.objects.all().order_by(F('end_date').desc(nulls_last=False), F('team__end_date').desc(nulls_last=False), 'team', 'user')
        else:
            teams = TeamMember.objects.filter(team__in=history.distinct().values_list('team')).order_by(F('end_date').desc(nulls_last=False), F('team__end_date').desc(nulls_last=False), 'team', 'user')

        form.fields["member"].choices = ((x.id, f'{x.team.name} {x.user.name}  {x.start_date} - {x.end_date or ""}') for x in teams)

        q_member = request.POST.get('member')
        q_date = request.POST.get('date')

        reports = WeeklyReport.objects.all()
        # チームでの絞り込み
        if q_member is not None and q_member > '':
            reports = reports.filter(member__id=q_member)

        # 報告日での絞り込み
        if q_date is not None and q_date > '':
            q_dt = datetime.datetime.strptime(q_date, '%Y/%m/%d')
            q_dt = q_dt - datetime.timedelta(days=q_dt.weekday())
            reports = reports.filter(report_date=q_dt)

        reports = reports.order_by('-report_date', 'type', 'created_date')
        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'form': form,
            'reports': reports,
        }
        return TemplateResponse(request, 'wr/reply.html', context)
