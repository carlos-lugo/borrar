from django.db import models
from django.utils.timezone import now
from user.models.user import User
from user.models.teamMember import TeamMember
from wr.models.contentType import ContentType


class WeeklyReport(models.Model):
    """週報モデル"""

    class Meta:
        # DBのテーブルの物理名
        db_table = 'weekly_report'
        # テーブル名論理名
        verbose_name = verbose_name_plural = '週報'
        # 属するアプリ
        app_label = 'wr'
        constraints = [
            models.UniqueConstraint(
                fields=["member", "report_date", "type", "created_user"],
                name="report_unique"
            ),
        ]

    # カラム設定
    member = models.ForeignKey(TeamMember, verbose_name='報告者', on_delete=models.PROTECT, related_name="member_weekly_reports")
    report_date = models.DateField(verbose_name='報告日')
    type = models.ForeignKey(ContentType, verbose_name='内容区分', on_delete=models.PROTECT, null=True, blank=True, related_name="type_weekly_reports")
    content = models.TextField(verbose_name='報告', null=True, blank=True)
    created_user = models.ForeignKey(User, verbose_name='記入者', on_delete=models.PROTECT, null=True, blank=True, related_name="created_user_weekly_reports")
    created_date = models.DateTimeField(verbose_name='記入⽇', default=now, )

    def __str__(self):
        return f'user={self.member.user.name}, report_date={self.report_date}'
