from django.db import models
from user.models.user import User
from user.models.teamMember import TeamMember
from user.models.team import Team


class ReportIndexList(models.Model):
    """週報インデックスViewモデル"""

    class Meta:
        managed = False
        # テーブル名論理名
        verbose_name = verbose_name_plural = '週報インデックス'
        db_table = 'report_index_list'

    report_date = models.DateField(verbose_name="報告日", editable=False)
    team_member = models.ForeignKey(TeamMember, verbose_name="報告者", on_delete=models.SET_NULL, related_name="team_report_indexes", blank=True, null=True, editable=False)
    team = models.ForeignKey(Team, verbose_name="報告者チーム", on_delete=models.SET_NULL, related_name="team_report_indexes", blank=True, null=True, editable=False)
    user = models.ForeignKey(User, verbose_name='報告者ユーザー', on_delete=models.SET_NULL, related_name="user_report_indexes", blank=True, null=True, editable=False)
    min_weekly_report_id = models.IntegerField(verbose_name="週報Id", editable=False)

    def __str__(self):
        return f'report_date={self.report_date} team={self.team.name}, user={self.user.name},'

# 作成時参考資料
# https://akiyoko.hatenablog.jp/entry/2020/12/05/101431
