

(function () {
    var CHAVE = 'mik-tema';
    var raiz = document.documentElement;

    function temaGuardado() {
        var t = null;
        try {
            t = localStorage.getItem(CHAVE);
        } catch (e) {
            t = null;
        }
        return (t === 'escuro') ? 'escuro' : 'claro';
    }

    function atualizarInterface(tema) {
        document.querySelectorAll('.toggle-tema-texto').forEach(function (el) {
            el.textContent = tema === 'escuro' ? 'Modo claro' : 'Modo escuro';
        });
        document.querySelectorAll('.toggle-tema-icone').forEach(function (el) {
            el.textContent = tema === 'escuro' ? '☀️' : '🌙';
        });
        document.querySelectorAll('.menu-conta-switch').forEach(function (el) {
            el.classList.toggle('ativo', tema === 'escuro');
        });
    }

    function aplicarTema(tema) {
        raiz.setAttribute('data-tema', tema);
        try {
            localStorage.setItem(CHAVE, tema);
        } catch (e) {  }
        atualizarInterface(tema);
    }

    raiz.setAttribute('data-tema', temaGuardado());

    window.alternarTema = function () {
        var atual = raiz.getAttribute('data-tema') === 'escuro' ? 'escuro' : 'claro';
        aplicarTema(atual === 'escuro' ? 'claro' : 'escuro');
    };

    document.addEventListener('DOMContentLoaded', function () {
        atualizarInterface(temaGuardado());
    });
})();
