"""Lógica de bloqueio de tentativas (equivalente ao auth.php do PHP)."""
from django.conf import settings
from django.utils import timezone
from api.models import AlertaSeguranca


def _get_store(request, chave):
    if 'tentativas' not in request.session:
        request.session['tentativas'] = {}
    return request.session['tentativas'].setdefault(
        chave, {'count': 0, 'bloqueado_ate': 0, 'alerta_enviado': False}
    )


def verificar_limite_tentativas(request, chave='senha'):
    store = request.session.get('tentativas', {}).get(chave)
    if not store:
        return None
    agora = int(timezone.now().timestamp())
    if store.get('bloqueado_ate', 0) <= agora:
        return None
    restante = store['bloqueado_ate'] - agora
    permanente = store.get('count', 0) >= settings.TENTATIVAS_LIMITE_TOTAL
    mensagem = (
        'Acesso bloqueado por 2 horas devido a excesso de tentativas. O administrador foi notificado.'
        if permanente
        else f'Demasiadas tentativas erradas. Tenta novamente em {restante} segundos.'
    )
    return {'restante': restante, 'permanente': permanente, 'mensagem': mensagem}


def registar_tentativa_falhada(request, chave='senha', user=None):
    agora = int(timezone.now().timestamp())
    store = _get_store(request, chave)
    store['count'] = store.get('count', 0) + 1
    count = store['count']
    bloqueado_ate = 0

    if count >= settings.TENTATIVAS_LIMITE_TOTAL:
        bloqueado_ate = agora + settings.TENTATIVAS_BLOQUEIO_TOTAL_SEGUNDOS
        if not store.get('alerta_enviado'):
            AlertaSeguranca.objects.create(
                tipo='bloqueio_total',
                descricao=(
                    f'Bloqueio de 2 horas após {count} tentativas falhadas '
                    f'seguídas na ação "{chave}". O administrador foi notificado.'
                ),
                ip=_client_ip(request),
                utilizador=user if user and user.is_authenticated else None,
            )
            store['alerta_enviado'] = True
    elif count >= settings.TENTATIVAS_LIMITE_INTERMEDIO:
        bloqueado_ate = agora + settings.TENTATIVAS_BLOQUEIO_INTERMEDIO_SEGUNDOS
    elif count >= settings.TENTATIVAS_LIMITE_INICIAL:
        bloqueado_ate = agora + settings.TENTATIVAS_BLOQUEIO_INICIAL_SEGUNDOS

    if bloqueado_ate > 0:
        store['bloqueado_ate'] = bloqueado_ate

    request.session['tentativas'][chave] = store
    request.session.modified = True
    return {'count': count, 'bloqueado_ate': bloqueado_ate}


def limpar_tentativas(request, chave='senha'):
    if 'tentativas' in request.session and chave in request.session['tentativas']:
        del request.session['tentativas'][chave]
        request.session.modified = True


def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def registar_acao(request, acao, detalhes=''):
    from api.models import Auditoria
    user = request.user
    if not user.is_authenticated or not getattr(user, 'is_admin', False):
        return
    Auditoria.objects.create(
        admin=user,
        admin_nome=user.nome,
        acao=acao,
        detalhes=detalhes,
        ip=_client_ip(request),
    )
