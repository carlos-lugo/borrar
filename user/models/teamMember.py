from django.db import models
from django.utils.timezone import now
from user.models.user import User
from user.models.team import Team


class TeamMember(models.Model):
    """チームメンバーモデル"""

    class Meta:
        # DBのテーブルの物理名
        db_table = 'team_member'
        # テーブル名論理名
        verbose_name = 'チームメンバー'  # 単数形
        verbose_name_plural = 'チームメンバー群'  # 複数形
        # 属するアプリ
        app_label = 'user'

        constraints = [
            models.UniqueConstraint(
                fields=["user", "end_date"],
                name="member_unique"
            ),
        ]

    # カラム設定
    team = models.ForeignKey(Team, verbose_name="チーム",  on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT, related_name="user_teams")
    can_report = models.BooleanField(verbose_name='報告可能フラグ', default=True)
    can_reply = models.IntegerField(verbose_name='返信可能フラグ', default=0)
    start_date = models.DateField(verbose_name='開始⽇', default=now)
    end_date = models.DateField(verbose_name='終了⽇', null=True, blank=True)

    # ForeignKey は多対一の関連モデルを保持するためのフィールド
    # on_delete は Join元(User)が消えた時の操作

    def __str__(self):
        return f'team={self.team.name}, user={self.user.name}'
