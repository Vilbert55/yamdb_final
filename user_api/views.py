from django.core.mail import send_mail
from rest_framework import viewsets, permissions, generics
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from .serializers import UserSerializer, EmailSerializer
from .permissions import IsAdmin
from .random import text_gen
from .exceptions import RefreshConfirmationCode


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    def perform_create(self, serializer):
        if 'email' not in self.request.data:
            raise ValidationError('Email field is requiered')
        return serializer.save(email=self.request.data.get('email'))


class UserGeneric(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        obj = self.request.user
        return obj


class EmailVIew(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def perform_create(self, serializer):

        email = self.request.data.get('email')
        if not email:
            raise ValidationError('Email field is requiered')
        confirmation_code = text_gen(6)
        exists = User.objects.filter(email=email).exists()
        send_mail(
            'Confirmation code',
            f'Your confirmation code: {confirmation_code}',
            'dergun12345@gmail.com',
            [email, ],
            fail_silently=False
        )
        if exists:
            user = User.objects.get(email=email)
            user.confirmation_code = confirmation_code
            user.save()
            raise RefreshConfirmationCode(
                f'Your new confirmation code: {str(confirmation_code)}')

        serializer.save(
            email=email, confirmation_code=confirmation_code, username=email)


@api_view(['POST', ])
def token_view(request):
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = generics.get_object_or_404(
        User, email=email, confirmation_code=confirmation_code)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
