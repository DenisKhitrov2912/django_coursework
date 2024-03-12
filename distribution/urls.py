from django.urls import path

from distribution.views import ClientsCreateView, ClientsDetailView, ClientsListView, ClientsUpdateView, \
    ClientsDeleteView, MessageCreateView, MessageDetailView, MessageListView, MessageUpdateView, MessageDeleteView, \
    DistParamsCreateView, DistParamsDetailView, DistParamsListView, DistParamsUpdateView, DistParamsDeleteView, \
    TrySendingDetailView, TrySendingListView, TrySendingDeleteView

urlpatterns = [
    path('', ClientsCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', ClientsDetailView.as_view(), name='client'),
    path('clients/', ClientsListView.as_view(), name='clients'),
    path('client/edit/<int:pk>/', ClientsUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>/', ClientsDeleteView.as_view(), name='client_delete'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message'),
    path('messages', MessageListView.as_view(), name='messages'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('distparams/create/', DistParamsCreateView.as_view(), name='distparams_create'),
    path('distparams/<int:pk>', DistParamsDetailView.as_view(), name='distparams_one'),
    path('distparams/', DistParamsListView.as_view(), name='distparams'),
    path('distparams/edit/<int:pk>', DistParamsUpdateView.as_view(), name='distparams_edit'),
    path('distparams/delete/<int:pk>', DistParamsDeleteView.as_view(), name='distparams_delete'),
    path('trysending/<int:pk>', TrySendingDetailView.as_view(), name='trysending_one'),
    path('trysending', TrySendingListView.as_view(), name='trysending'),
    path('trysending/delete/<int:pk>', TrySendingDeleteView.as_view(), name='trysending_delete')
]
