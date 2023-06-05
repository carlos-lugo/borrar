from django.db import models
from django.utils.timezone import now


class Team(models.Model):
    """チームマスタモデル"""

    class Meta:
        # DBのテーブルの物理名
        db_table = 'team'
        # テーブル名論理名

        verbose_name = 'チーム'  # 単数形
        verbose_name_plural = 'チーム群'  # 複数形
        # 属するアプリ
        app_label = 'user'

    # カラム設定
    name = models.CharField(verbose_name='名称', max_length=255)
    blanch = models.CharField(verbose_name='所属名', null=True, blank=True, max_length=255)
    start_date = models.DateField(verbose_name='開始⽇', default=now)
    end_date = models.DateField(verbose_name='終了⽇', null=True, blank=True)

    # ForeignKey は多対一の関連モデルを保持するためのフィールド
    # on_delete は Join元(User)が消えた時の操作

    def __str__(self):
        return f'name={self.name} {self.start_date} - {self.end_date}'
