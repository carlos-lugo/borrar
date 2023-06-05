from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views import View
from .forms import TodoForm
from .models import Todo


class TodoListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        todo_list = Todo.objects.filter(created_by=request.user).order_by('expiration_date')
        context = {
            'today': today,
            'todo_list': todo_list,
        }
        return TemplateResponse(request, 'todo/todo_list.html', context)


class TodoCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': TodoForm(),
        }
        return TemplateResponse(request, 'todo/todo_create.html', context)

    def post(self, request, *args, **kwargs):
        # リクエストパラメータからフォームを作成
        form = TodoForm(request.POST)
        # フォームを使ってバリデーション
        if not form.is_valid():
            # バリデーションNGの場合はリクエスト元の画面のテンプレートを再表示
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'todo/todo_create.html', context)

        # バリデーションOKの場合はオブジェクトを保存
        todo = form.save(commit=False)
        todo.created_by = request.user
        todo.save()
        # TODOリスト画面にリダイレクト
        return HttpResponseRedirect('/todo/')


class TodoUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            todo = Todo.objects.get(id=pk, created_by=request.user)
        except Todo.DoesNotExist:
            return HttpResponseRedirect('/todo/edit/')

        context = {
            'form': TodoForm(instance=todo),
        }
        return TemplateResponse(request, 'todo/todo_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            todo = Todo.objects.get(id=pk, created_by=request.user)
        except Todo.DoesNotExist:
            raise Http404

        form = TodoForm(request.POST, instance=todo)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'todo/todo_update.html', context)

        form.save()
        return HttpResponseRedirect('/todo/')
