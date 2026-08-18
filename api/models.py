from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db import models
from django.utils import timezone


class MembroManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        if not nome:
            raise ValueError('O nome é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('nivel', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nome, password, **extra_fields)


class Membro(AbstractBaseUser, PermissionsMixin):
    NIVEIS = (
        ('user', 'Utilizador'),
        ('admin', 'Administrador'),
    )
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=30, blank=True, default='')
    foto = models.ImageField(upload_to='uploads/', default='uploads/padrao.jpg', blank=True)
    nivel = models.CharField(max_length=10, choices=NIVEIS, default='user')
    senha_seguranca = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MembroManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        db_table = 'membros'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def is_admin(self):
        return self.nivel == 'admin' or self.is_superuser

    def check_security_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        if check_password(raw_password, self.password):
            return True
        if self.senha_seguranca and check_password(raw_password, self.senha_seguranca):
            return True
        return False


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    data_atividade = models.CharField(max_length=100, blank=True, default='')
    descricao = models.TextField(blank=True, default='')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'painel_eventos'
        ordering = ['-id']

    def __str__(self):
        return self.titulo


class FotoGaleria(models.Model):
    imagem = models.ImageField(upload_to='uploads/')
    legenda = models.CharField(max_length=255, blank=True, default='')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'painel_galeria'
        ordering = ['-id']

    def __str__(self):
        return self.legenda or f'Foto #{self.pk}'


class Mensagem(models.Model):
    nome = models.CharField(max_length=150)
    assunto = models.CharField(max_length=200)
    texto = models.TextField()
    data_envio = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'mensagens'
        ordering = ['-id']

    def __str__(self):
        return f'{self.assunto} — {self.nome}'


class Auditoria(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='acoes_auditoria')
    admin_nome = models.CharField(max_length=150)
    acao = models.CharField(max_length=80)
    detalhes = models.TextField(blank=True, null=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auditoria'
        ordering = ['-criado_em']


class AlertaSeguranca(models.Model):
    tipo = models.CharField(max_length=50)
    descricao = models.TextField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertas')
    criado_em = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    class Meta:
        db_table = 'alertas_seguranca'
        ordering = ['lido', '-criado_em']
