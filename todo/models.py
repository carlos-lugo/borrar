from user.models.user import User
from django.db import models


class Todo(models.Model):
    """TODOモデル"""

    class Meta:
        # DBのテーブルの物理名
        db_table = 'todo'
        # テーブル名論理名
        verbose_name = verbose_name_plural = 'TODO'

    # カラム設定
    title = models.CharField(verbose_name='タイトル', max_length=255)
    expiration_date = models.DateField(verbose_name='期限⽇', null=True, blank=True)
    description = models.TextField(verbose_name='詳細', null=True, blank=True)
    is_done = models.BooleanField(verbose_name='完了フラグ', default=False)
    created_by = models.ForeignKey(User, verbose_name='登録ユーザー', on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    # ForeignKey は多対一の関連モデルを保持するためのフィールド
    # on_delete は Join元(User)が消えた時の操作

    def __str__(self):
        return self.title
