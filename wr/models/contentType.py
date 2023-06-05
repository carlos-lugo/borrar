from django.db import models


class ContentType(models.Model):
    """週報内容区分モデル"""

    class Meta:
        # DBのテーブルの物理名
        db_table = 'content_type'
        # テーブル名論理名
        verbose_name = verbose_name_plural = '週報内容区分'
        # 属するアプリ
        app_label = 'wr'

    # カラム設定
    name = models.CharField(verbose_name='名称', max_length=255)
    order = models.IntegerField(verbose_name='表示順',default=0)
    active = models.BooleanField(verbose_name='有効フラグ', default=True)

    def __str__(self):
        return f'name={self.name}, active={self.active}'
