from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from api.models import Membro
from api.serializers import (
    MembroSerializer, MembroAdminSerializer, RegisterSerializer,
    LoginSerializer, ChangePasswordSerializer, MudarNivelSerializer,
)
from api.utils import (
    verificar_limite_tentativas, registar_tentativa_falhada,
    limpar_tentativas, registar_acao,
)


def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class RegisterAPI(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response({
            'user': MembroSerializer(user, context={'request': request}).data,
            'tokens': tokens_for(user),
        }, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        bloqueio = verificar_limite_tentativas(request, 'login')
        if bloqueio:
            return Response({'erro': bloqueio['mensagem'], 'bloqueio': bloqueio}, status=403)

        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            registar_tentativa_falhada(request, 'login')
            bloqueio = verificar_limite_tentativas(request, 'login')
            return Response({
                'erro': ser.errors.get('non_field_errors', ['Dados inválidos'])[0]
                if isinstance(ser.errors.get('non_field_errors'), list)
                else 'Dados inválidos',
                'bloqueio': bloqueio,
            }, status=400)

        limpar_tentativas(request, 'login')
        user = ser.validated_data['user']
        return Response({
            'user': MembroSerializer(user, context={'request': request}).data,
            'tokens': tokens_for(user),
        })


class MeAPI(APIView):
    def get(self, request):
        return Response(MembroSerializer(request.user, context={'request': request}).data)

    def patch(self, request):
        user = request.user
        for field in ('nome', 'email', 'telefone'):
            if field in request.data:
                setattr(user, field, request.data[field])
        if 'foto' in request.FILES:
            user.foto = request.FILES['foto']
        user.save()
        return Response(MembroSerializer(user, context={'request': request}).data)


class ChangePasswordAPI(APIView):
    def post(self, request):
        bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
        if bloqueio:
            return Response({'erro': bloqueio['mensagem'], 'bloqueio': bloqueio}, status=403)
        ser = ChangePasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = request.user
        if not user.check_security_password(ser.validated_data['senha_atual']):
            registar_tentativa_falhada(request, 'acao_sensivel', user)
            bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
            return Response({'erro': 'Senha atual incorreta.', 'bloqueio': bloqueio}, status=400)
        limpar_tentativas(request, 'acao_sensivel')
        user.set_password(ser.validated_data['nova_senha'])
        user.save()
        return Response({'mensagem': 'Palavra-passe alterada com sucesso.'})


class DeleteAccountAPI(APIView):
    def post(self, request):
        bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
        if bloqueio:
            return Response({'erro': bloqueio['mensagem'], 'bloqueio': bloqueio}, status=403)
        senha = request.data.get('senha_confirmacao', '')
        if not request.user.check_security_password(senha):
            registar_tentativa_falhada(request, 'acao_sensivel', request.user)
            bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
            return Response({'erro': 'Senha incorreta.', 'bloqueio': bloqueio}, status=400)
        limpar_tentativas(request, 'acao_sensivel')
        request.user.delete()
        return Response({'mensagem': 'Conta eliminada.'})


from api.permissions import IsAdmin


class MembrosListAPI(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = MembroAdminSerializer
    queryset = Membro.objects.all()


class MudarNivelAPI(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
        if bloqueio:
            return Response({'erro': bloqueio['mensagem'], 'bloqueio': bloqueio}, status=403)
        ser = MudarNivelSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        if data['id'] == request.user.pk:
            return Response({'erro': 'Não é permitido alterar o próprio nível.'}, status=400)
        membro = Membro.objects.filter(pk=data['id']).first()
        if not membro:
            return Response({'erro': 'Membro não encontrado.'}, status=404)
        if not request.user.check_security_password(data['senha_confirmacao']):
            registar_tentativa_falhada(request, 'acao_sensivel', request.user)
            bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
            tentativas = request.session.get('tentativas', {}).get('acao_sensivel', {}).get('count', 0)
            return Response({
                'erro': 'Senha incorreta.',
                'bloqueio': bloqueio,
                'tentativas': tentativas,
            }, status=400)
        limpar_tentativas(request, 'acao_sensivel')
        membro.nivel = data['mudar_nivel']
        membro.is_staff = data['mudar_nivel'] == 'admin'
        membro.save()
        registar_acao(
            request,
            'promover_admin' if data['mudar_nivel'] == 'admin' else 'despromover_admin',
            f'{"Promoveu" if data["mudar_nivel"] == "admin" else "Despromoveu"} "{membro.nome}"',
        )
        return Response({
            'mensagem': 'Membro promovido.' if data['mudar_nivel'] == 'admin' else 'Membro despromovido.',
            'membro': MembroAdminSerializer(membro, context={'request': request}).data,
        })


class SenhaSegurancaAPI(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
        if bloqueio:
            return Response({'erro': bloqueio['mensagem'], 'bloqueio': bloqueio}, status=403)
        atual = request.data.get('senha_atual', '')
        nova = request.data.get('senha_seguranca', '')
        conf = request.data.get('confirmacao', '')
        if not request.user.check_security_password(atual):
            registar_tentativa_falhada(request, 'acao_sensivel', request.user)
            bloqueio = verificar_limite_tentativas(request, 'acao_sensivel')
            return Response({'erro': 'Senha atual incorreta.', 'bloqueio': bloqueio}, status=400)
        if len(nova) < 8 or nova != conf:
            return Response({'erro': 'Senha de segurança inválida.'}, status=400)
        limpar_tentativas(request, 'acao_sensivel')
        request.user.senha_seguranca = make_password(nova)
        request.user.save()
        registar_acao(request, 'senha_seguranca', 'Atualizou senha de segurança')
        return Response({'mensagem': 'Senha de segurança guardada.'})


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from api.permissions import IsAdmin
from api.utils import registar_acao
from api.models import Evento, FotoGaleria, Mensagem, Auditoria, AlertaSeguranca
from api.serializers import (
    EventoSerializer, FotoGaleriaSerializer, MensagemSerializer,
    AuditoriaSerializer, AlertaSegurancaSerializer,
)


class EventoListAPI(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventoAdminAPI(generics.ListCreateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        ev = serializer.save()
        registar_acao(self.request, 'criar_evento', f'Criou "{ev.titulo}"')


class EventoDeleteAPI(generics.DestroyAPIView):
    queryset = Evento.objects.all()
    permission_classes = [IsAdmin]

    def perform_destroy(self, instance):
        registar_acao(self.request, 'eliminar_evento', f'Eliminou "{instance.titulo}"')
        instance.delete()


class GaleriaListAPI(generics.ListAPIView):
    queryset = FotoGaleria.objects.all()
    serializer_class = FotoGaleriaSerializer
    permission_classes = [permissions.IsAuthenticated]


class GaleriaAdminAPI(generics.ListCreateAPIView):
    queryset = FotoGaleria.objects.all()
    serializer_class = FotoGaleriaSerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        foto = serializer.save()
        registar_acao(self.request, 'adicionar_foto', f'Adicionou "{foto.legenda}"')


class GaleriaDeleteAPI(generics.DestroyAPIView):
    queryset = FotoGaleria.objects.all()
    permission_classes = [IsAdmin]

    def perform_destroy(self, instance):
        registar_acao(self.request, 'eliminar_foto', f'Eliminou "{instance.legenda}"')
        instance.delete()


class MensagemCreateAPI(generics.CreateAPIView):
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer
    permission_classes = [permissions.IsAuthenticated]


class MensagemListAPI(generics.ListAPIView):
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer
    permission_classes = [IsAdmin]


class MensagemDeleteAPI(generics.DestroyAPIView):
    queryset = Mensagem.objects.all()
    permission_classes = [IsAdmin]


class AuditoriaListAPI(generics.ListAPIView):
    queryset = Auditoria.objects.all()[:200]
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAdmin]


class AlertasListAPI(generics.ListAPIView):
    queryset = AlertaSeguranca.objects.all()[:100]
    serializer_class = AlertaSegurancaSerializer
    permission_classes = [IsAdmin]


class AlertaMarcarAPI(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        if request.data.get('todos'):
            AlertaSeguranca.objects.filter(lido=False).update(lido=True)
        elif request.data.get('id'):
            AlertaSeguranca.objects.filter(pk=request.data['id']).update(lido=True)
        return Response({'ok': True})


class HomeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'eventos': EventoSerializer(Evento.objects.all()[:3], many=True, context={'request': request}).data,
            'fotos': FotoGaleriaSerializer(FotoGaleria.objects.all()[:4], many=True, context={'request': request}).data,
            'user': {
                'nome': request.user.nome,
                'nivel': request.user.nivel,
                'is_admin': request.user.is_admin,
            },
        })
