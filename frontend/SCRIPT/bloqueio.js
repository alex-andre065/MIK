

function iniciarContadorBloqueio(elementId, segundosRestantes, permanente, seletoresBotoes) {
    var el = document.getElementById(elementId);
    if (!el) return;

    var restante = parseInt(segundosRestantes, 10) || 0;
    seletoresBotoes = seletoresBotoes || [];

    function definirBotoes(desativado) {
        seletoresBotoes.forEach(function (sel) {
            document.querySelectorAll(sel).forEach(function (btn) {
                btn.disabled = desativado;
            });
        });
    }

    function formatarTempo(segundos) {
        var h = Math.floor(segundos / 3600);
        var m = Math.floor((segundos % 3600) / 60);
        var s = segundos % 60;
        if (h > 0) {
            return h + 'h ' + String(m).padStart(2, '0') + 'm ' + String(s).padStart(2, '0') + 's';
        }
        if (m > 0) {
            return m + 'm ' + String(s).padStart(2, '0') + 's';
        }
        return s + 's';
    }

    function atualizar() {
        if (restante <= 0) {
            if (permanente) {

                el.textContent = 'O bloqueio pode ter expirado. Atualiza a página para tentar novamente.';
            } else {
                el.textContent = 'Já podes tentar novamente.';
                definirBotoes(false);
            }
            clearInterval(intervalo);
            return;
        }

        el.textContent = permanente
            ? 'Acesso bloqueado por 2 horas. O administrador foi notificado. (' + formatarTempo(restante) + ')'
            : 'Demasiadas tentativas erradas. Tenta novamente em ' + formatarTempo(restante) + '.';

        restante--;
    }

    definirBotoes(true);
    atualizar();
    var intervalo = setInterval(atualizar, 1000);
}
