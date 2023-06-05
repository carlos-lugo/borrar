import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.template.response import TemplateResponse
from django.views import View
from django.db.models import Q, Max, Count, F
from wr.forms import WrForm, WrSearchForm, WrReportFormSet, WrReplyForm
from wr.models import WeeklyReport, ReportIndexList, ContentType
from user.models import TeamMember, Team
from django.template.context_processors import csrf


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


class WrSearchDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        today = request.user.last_login.today()
        indexes = []
        for index in ReportIndexList.objects.filter(min_weekly_report_id=pk).order_by('report_date', 'team', 'user'):
            indexes.append(
                {'report_date': index.report_date,
                 'team_member': index.team_member,
                 'team': index.team,
                 'user': index.user,
                 'reports': WeeklyReport.objects.filter(member=index.team_member, report_date=index.report_date).order_by('report_date', F('type').desc(nulls_last=True), 'created_date'), }
            )

        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'indexes': indexes,
            'back': 'search',
        }

        return TemplateResponse(request, 'wr/detail.html', context)


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
            'back': 'portfolio',
        }

        return TemplateResponse(request, 'wr/detail.html', context)


class WrReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = request.user.last_login.today()
        report_from = today - datetime.timedelta(days=today.weekday())
        report_end = today + datetime.timedelta(days=(6 - today.weekday()))
        c_types = ContentType.objects.filter(active=True).order_by('order')

        try:
            member = TeamMember.objects.get(user=request.user, end_date=None)
        except TeamMember.DoesNotExist:
            return HttpResponseRedirect('/wr')

        my_report = WeeklyReport.objects.filter(member=member, report_date=report_from, created_user=request.user, type__isnull=False)

        if len(c_types) < 1 or len(c_types) < len(my_report) or not member.can_report:
            return HttpResponseRedirect('/wr')

        form_initial = []
        for c_type in c_types:
            form_initial.append({'member': member, 'report_date': report_from, 'type': c_type.id, 'content': '', 'created_user': request.user, })

        formset = WrReportFormSet(None, queryset=my_report, initial=form_initial, )
        context = {
            'today': today,
            'report_from': report_from,
            'report_end': report_end,
            'formset': formset,
            'types': c_types,
        }
        return TemplateResponse(request, 'wr/report.html', context)

    def post(self, request, *args, **kwargs):
        today = request.user.last_login.today()
        report_from = today - datetime.timedelta(days=today.weekday())
        report_end = today + datetime.timedelta(days=(6 - today.weekday()))
        formset = WrReportFormSet(request.POST)
        member = TeamMember.objects.get(user=request.user, end_date=None)
        c_types = ContentType.objects.filter(active=True).order_by('order')
        context = {
            'today': today,
            'report_from': report_from,
            'report_end': report_end,
            'formset': formset,
            'types': c_types,
        }

        # フォームを使ってバリデーション
        if not formset.is_valid():
            return TemplateResponse(request, 'wr/report.html', context)

        # バリデーションOKの場合はオブジェクトを保存
        instances = formset.save(commit=False)
        # 新たに作成されたfileと更新されたfileを取り出し、ユーザーを紐づけて保存
        for counter, weekly_report in enumerate(instances):
            weekly_report.member = member
            weekly_report.report_date = report_from
            weekly_report.created_user = request.user
            weekly_report.created_date = datetime.datetime.now()
            weekly_report.save()

        # TOP画面にリダイレクト
        return HttpResponseRedirect('/wr/')


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


class WrReplyDetailView(LoginRequiredMixin, View):
    def get(self, request, date, member, *args, **kwargs):
        today = request.user.last_login.today()
        report_date = datetime.datetime.strptime(date, '%Y%m%d')
        indexes = []

        for index in ReportIndexList.objects.filter(team_member__id=member, report_date=report_date).order_by('report_date', 'team', 'user'):
            indexes.append(
                {'report_date': index.report_date,
                 'team_member': index.team_member,
                 'team': index.team,
                 'user': index.user,
                 'reports': WeeklyReport.objects.filter(member=index.team_member, report_date=index.report_date).order_by('report_date', F('type').desc(nulls_last=True), 'created_date'), }
            )

        context = {
            'today': today,
            'report_from': today - datetime.timedelta(days=today.weekday()),
            'report_end': today + datetime.timedelta(days=(6 - today.weekday())),
            'indexes': indexes,
            'back': 'reply',
        }

        return TemplateResponse(request, 'wr/reply_detail.html', context)


# 以下Viewのサンプルプログラム
class WrCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': WrForm(),
        }
        return TemplateResponse(request, 'wr/todo_create.html', context)

    def post(self, request, *args, **kwargs):
        # リクエストパラメータからフォームを作成
        form = WrForm(request.POST)
        # フォームを使ってバリデーション
        if not form.is_valid():
            # バリデーションNGの場合はリクエスト元の画面のテンプレートを再表示
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'wr/todo_create.html', context)

        # バリデーションOKの場合はオブジェクトを保存
        todo = form.save(commit=False)
        todo.created_by = request.user
        todo.save()
        # TODOリスト画面にリダイレクト
        return HttpResponseRedirect('/wr/')


class WrUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            todo = WeeklyReport.objects.get(id=pk, created_by=request.user)
        except WeeklyReport.DoesNotExist:
            return HttpResponseRedirect('/wr/edit/')

        context = {
            'form': WrForm(instance=todo),
        }
        return TemplateResponse(request, 'wr/todo_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            todo = WeeklyReport.objects.get(id=pk, created_by=request.user)
        except WeeklyReport.DoesNotExist:
            raise Http404

        form = WrForm(request.POST, instance=todo)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'wr/todo_update.html', context)

        form.save()
        return HttpResponseRedirect('/wr/')
