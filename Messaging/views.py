from django.db.models import Q, Max
from django.http import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from .models import *
from Hospital_Management.models import Appointment, Doctor
from django.contrib.auth import get_user_model

User = get_user_model()


class Index(generic.ListView, LoginRequiredMixin):
    model = Chat
    context_object_name = 'chats'
    template_name = 'chats.html'

    def get_queryset(self):
        qs = self.model.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)).\
            annotate(last_message_time=Max('messages__timestamp'))
        return qs

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        context['user'] = self.request.user.id
        return context


def newChat(request, *args, **kwargs):
    chat = Chat.objects.filter(
        (Q(receiver_id=kwargs['receiver']) | Q(receiver_id=kwargs['sender'])) &
        (Q(sender_id=kwargs['receiver']) | Q(sender_id=kwargs['sender']))
    )
    if chat:
        return JsonResponse({'chat_id': chat.values_list('id', flat=True)})

    new_chat = Chat.objects.create(receiver_id=kwargs['receiver'], sender_id=kwargs['sender'])
    return JsonResponse({'chat_id': new_chat.id})


def get_doctors(request):
    # Get all past and current appointments for the patient
    appointments = Appointment.objects.filter(Q(patient__patient=request.user)
                                              | Q(assigned_doctor__name__staff=request.user))
    appointments = appointments.values_list('assigned_doctor__name__staff', flat=True)

    assigned_doctors_id = []
    for id in appointments:
        assigned_doctors_id.append(id)

    # Get all chat objects involving the patient
    patient_chats = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

    chat_senders = set(patient_chats.values_list('sender', flat=True))
    chat_receivers = set(patient_chats.values_list('receiver', flat=True))

    assigned_doctors = User.objects.filter(id__in=assigned_doctors_id)

    doctors_without_chats = []
    for doctor in assigned_doctors:
        if doctor.id not in chat_senders and doctor not in chat_receivers:
            doctors_without_chats.append(doctor)

    # Get email and id of each doctor
    doctors_data = [{'id': doctor.id, 'name': doctor.email} for doctor in doctors_without_chats]
    if doctors_data:
        return JsonResponse({'doctors': doctors_data})
    else:
        return JsonResponse({'error': 'No Doctor to chat with'}, status=404)


def get_chat_messages(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    receiver = chat.receiver.id
    messages = Message.objects.filter(chat=chat)

    data = []
    for message in messages:
        data.append({
            "content": message.content,
            "sender": message.sender.id,
            "receiver": message.receiver.id,
            "timestamp": message.timestamp.strftime("%I:%M %p | %b %d"),
        })

    return JsonResponse({'data': data, 'receiver': receiver}, safe=False)

