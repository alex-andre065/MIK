
(function () {
    'use strict';

    var style = document.createElement('style');
    style.textContent = `
        #global-loader {
            display: none;
            position: fixed;
            inset: 0;
            z-index: 99999;
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            justify-content: center;
            align-items: center;
            flex-direction: column;
            gap: 16px;
        }
        #global-loader.active {
            display: flex;
        }
        #global-loader .gl-spinner {
            width: 56px;
            height: 56px;
            border: 4px solid rgba(255, 255, 255, 0.2);
            border-top-color: #007bff;
            border-radius: 50%;
            animation: gl-spin 0.75s linear infinite;
        }
        #global-loader .gl-texto {
            color: rgba(255, 255, 255, 0.9);
            font-size: 15px;
            font-family: Arial, sans-serif;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        @keyframes gl-spin {
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    function criarLoader() {
        if (document.getElementById('global-loader')) return;
        var el = document.createElement('div');
        el.id = 'global-loader';
        el.setAttribute('aria-live', 'polite');
        el.setAttribute('aria-busy', 'true');
        el.innerHTML = '<div class="gl-spinner"></div><div class="gl-texto">A processar...</div>';
        document.body.appendChild(el);
    }

    function mostrarLoader(texto) {
        criarLoader();
        var el = document.getElementById('global-loader');
        var t = el.querySelector('.gl-texto');
        if (t) t.textContent = texto || 'A processar...';
        el.classList.add('active');
    }

    function esconderLoader() {
        var el = document.getElementById('global-loader');
        if (el) el.classList.remove('active');
    }

    window.mostrarLoader = mostrarLoader;
    window.esconderLoader = esconderLoader;

    function mesmoSite(href) {
        if (!href || href === '#' || href.indexOf('javascript:') === 0) return false;
        try {
            var url = new URL(href, window.location.href);
            return url.origin === window.location.origin;
        } catch (e) {
            return false;
        }
    }

    function deveIgnorarLink(a) {
        if (!a) return true;
        if (a.target === '_blank') return true;
        if (a.hasAttribute('download')) return true;
        if (a.getAttribute('href') === '#') return true;
        if (a.onclick && a.getAttribute('onclick') && (
            a.getAttribute('onclick').indexOf('abrirModal') !== -1 ||
            a.getAttribute('onclick').indexOf('fechar') !== -1 ||
            a.getAttribute('onclick').indexOf('ampliar') !== -1 ||
            a.getAttribute('onclick').indexOf('toggle') !== -1 ||
            a.getAttribute('onclick').indexOf('preventDefault') !== -1
        )) return true;

        var href = a.getAttribute('href') || '';
        if (href.charAt(0) === '#') return true;
        return false;
    }

    document.addEventListener('DOMContentLoaded', function () {
        criarLoader();

        document.querySelectorAll('form').forEach(function (form) {
            form.addEventListener('submit', function (e) {
                if (form.hasAttribute('data-no-loader') || form.hasAttribute('data-ajax') || form.closest('.modal-container')) {
                    return;
                }
                if (form.checkValidity && !form.checkValidity()) return;
                var texto = 'A processar...';
                if (form.querySelector('[name="senha_confirmacao"], [name="senha_atual"]')) {
                    texto = 'A verificar...';
                } else if (form.querySelector('[name="mudar_nivel"]')) {
                    texto = 'A atualizar nível...';
                } else if (form.querySelector('[name="eliminar"]')) {
                    texto = 'A eliminar...';
                } else if (form.querySelector('[name="login_input"]')) {
                    texto = 'A entrar...';
                }
                mostrarLoader(texto);
            });
        });

        document.body.addEventListener('click', function (e) {
            var a = e.target.closest('a');
            if (!a) return;
            if (deveIgnorarLink(a)) return;
            var href = a.getAttribute('href');
            if (!mesmoSite(href)) return;

            mostrarLoader('A carregar...');
        });

        window.addEventListener('pageshow', function () {
            esconderLoader();
        });
    });
})();
