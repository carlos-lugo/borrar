from django.contrib import admin
from .models import ContentType, WeeklyReport, ReportIndexList


class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "active",)
    list_filter = ("active",)
    filter_horizontal = ()
    ordering = ("active", "order",)
    search_fields = ("name",)


class ReportIndexListAdmin(admin.ModelAdmin):
    """週報インデックスモデル用 ModelAdmin"""

    # モデル一覧画面のカスタマイズ
    list_display = ('report_date', 'team', 'user')
    ordering = ('report_date', 'team', 'user')
    search_fields = ("team__name", 'user__email', "user__name",)

    fieldsets = (
        ('報告日', {'fields': ('report_date',)}),
        ('チーム', {'fields': ('team',)}),
        ('ユーザー', {'fields': ('user',)}),
    )

    # その他のカスタマイズ
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(WeeklyReport)
admin.site.register(ReportIndexList, ReportIndexListAdmin)
