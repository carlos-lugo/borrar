import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views import View
from wr.forms import WrReportFormSet
from wr.models import WeeklyReport, ContentType
from user.models import TeamMember


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
