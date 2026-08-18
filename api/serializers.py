from rest_framework import serializers
from django.contrib.auth import authenticate
from api.models import Membro


class MembroSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Membro
        fields = ('id', 'nome', 'email', 'telefone', 'foto', 'foto_url', 'nivel', 'date_joined')
        read_only_fields = ('id', 'nivel', 'date_joined')

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            url = obj.foto.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class MembroAdminSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Membro
        fields = ('id', 'nome', 'email', 'telefone', 'foto', 'foto_url', 'nivel', 'is_active', 'date_joined')

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            url = obj.foto.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Membro
        fields = ('nome', 'email', 'telefone', 'password', 'foto')

    def create(self, validated_data):
        foto = validated_data.pop('foto', None)
        user = Membro.objects.create_user(
            email=validated_data['email'],
            nome=validated_data['nome'],
            password=validated_data['password'],
            telefone=validated_data.get('telefone', ''),
        )
        if foto:
            user.foto = foto
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    login_input = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login_input = data['login_input'].strip()
        password = data['password']
        qs = Membro.objects.filter(email__iexact=login_input)
        if not qs.exists():
            qs = Membro.objects.filter(telefone=login_input)
        if not qs.exists():
            qs = Membro.objects.filter(nome__iexact=login_input)
        if qs.count() > 1:
            raise serializers.ValidationError('Vários utilizadores com esse nome. Use e-mail ou telefone.')
        if qs.count() == 0:
            raise serializers.ValidationError('Dados de acesso inválidos.')
        user = qs.first()
        auth_user = authenticate(username=user.email, password=password)
        if not auth_user:
            raise serializers.ValidationError('Dados de acesso inválidos.')
        data['user'] = auth_user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    senha_atual = serializers.CharField()
    nova_senha = serializers.CharField(min_length=8)
    confirmacao = serializers.CharField()

    def validate(self, data):
        if data['nova_senha'] != data['confirmacao']:
            raise serializers.ValidationError({'confirmacao': 'As senhas não coincidem.'})
        return data


class MudarNivelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    mudar_nivel = serializers.ChoiceField(choices=['admin', 'user'])
    senha_confirmacao = serializers.CharField()
from rest_framework import serializers
from api.models import Evento, FotoGaleria, Mensagem, Auditoria, AlertaSeguranca


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ('id', 'titulo', 'data_atividade', 'descricao', 'criado_em')
        read_only_fields = ('id', 'criado_em')


class FotoGaleriaSerializer(serializers.ModelSerializer):
    imagem_url = serializers.SerializerMethodField()

    class Meta:
        model = FotoGaleria
        fields = ('id', 'imagem', 'imagem_url', 'legenda', 'criado_em')
        read_only_fields = ('id', 'criado_em')

    def get_imagem_url(self, obj):
        request = self.context.get('request')
        if obj.imagem and hasattr(obj.imagem, 'url'):
            url = obj.imagem.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class MensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensagem
        fields = ('id', 'nome', 'assunto', 'texto', 'data_envio')
        read_only_fields = ('id', 'data_envio')


class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = ('id', 'admin_nome', 'acao', 'detalhes', 'ip', 'criado_em')


class AlertaSegurancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaSeguranca
        fields = ('id', 'tipo', 'descricao', 'ip', 'criado_em', 'lido')
