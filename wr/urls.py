from django.urls import path

from wr.views.wrTopView import WrTopView
from wr.views.wrSearchView import WrSearchView
from wr.views.wrSearchDetailView import WrSearchDetailView
from wr.views.wrPortfolioView import WrPortfolioView
from wr.views.wrPortfolioDetailView import WrPortfolioDetailView
from wr.views.wrReportView import WrReportView
from wr.views.wrReplyView import WrReplyView
from wr.views.wrReplyDetailView import WrReplyDetailView

urlpatterns = [
    path('', WrTopView.as_view()),
    path('search', WrSearchView.as_view()),
    path('search/<int:pk>/', WrSearchDetailView.as_view()),
    path('portfolio', WrPortfolioView.as_view()),
    path('portfolio/<int:pk>/', WrPortfolioDetailView.as_view()),
    path('report/', WrReportView.as_view()),
    path('reply/', WrReplyView.as_view()),
    path('reply/<str:date>/<int:member>/', WrReplyDetailView.as_view()),
]
