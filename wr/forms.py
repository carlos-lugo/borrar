from django import forms
from wr.models import WeeklyReport
from wr.models import ContentType
from user.models import Team


class WrForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        # 入力値が3文字より短ければバリデーションエラー
        if len(title) < 3:
            raise forms.ValidationError('タイトルは3文字以上で入力してください')
        return title


class WrSearchForm(forms.Form):
    team = forms.MultipleChoiceField(
        label='チーム選択',
        required=False,
        disabled=False,
        choices=[(t.id, f'{t.name} {t.start_date} - {t.end_date or ""}') for t in Team.objects.all()],
        widget=forms.SelectMultiple(attrs={'id': 'team', }),
    )

    name = forms.CharField(
        label='報告者名',
        required=False,
        disabled=False,
        max_length=255,
        widget=forms.TextInput,
    )

    date = forms.DateField(
        label='報告週',
        required=False,
        disabled=False,
        input_formats="%Y-%m-%d",
    )


class WrReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = WeeklyReport
        fields = '__all__'
        widgets = {"type": forms.HiddenInput}
        labels = {'content': ''}

    def clean_content(self):
        content = self.cleaned_data['content']
        # 入力値が3文字より短ければバリデーションエラー
        if len(content) < 0:
            raise forms.ValidationError('必ず入力してください')
        return content


WrReportFormSet = forms.modelformset_factory(
    WeeklyReport,
    form=WrReportForm,
    exclude=['member', 'report_date', 'created_user', 'created_date'],
    extra=len(ContentType.objects.filter(active=True)) if len(ContentType.objects.filter(active=True)) > 0 else 0,
    max_num=len(ContentType.objects.filter(active=True)) if len(ContentType.objects.filter(active=True)) > 0 else 0,
)


class WrReplyForm(forms.Form):
    date = forms.DateField(
        label='報告週',
        required=True,
        disabled=False,
        input_formats="%Y-%m-%d",
    )

    member = forms.ChoiceField(
        label='報告者',
        required=True,
        disabled=False,
        widget=forms.widgets.Select,
    )


WrReplyFormSet = forms.modelformset_factory(
    WeeklyReport,
    form=WrReportForm,
    exclude=['member', 'report_date', 'created_user', 'created_date'],
    extra=1,
    max_num=1,
)
