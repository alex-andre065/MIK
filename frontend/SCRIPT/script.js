function toggleSidebar(event) {
    if (event) {
        event.stopPropagation();
    }
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebar-overlay');
    if (!sidebar) return;

    sidebar.classList.toggle('active');
    var aberto = sidebar.classList.contains('active');

    if (overlay) {
        overlay.style.display = aberto ? 'block' : 'none';
    }

    document.body.style.overflow = aberto ? 'hidden' : '';
}

function fecharSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebar-overlay');
    if (sidebar) sidebar.classList.remove('active');
    if (overlay) overlay.style.display = 'none';
    document.body.style.overflow = '';
}

function abrirModal(event) {
    event.preventDefault();
    fecharMenuConta();
    var m = document.getElementById('modal-sair');
    if (m) m.style.display = 'flex';
}

function fecharModal() {
    var m = document.getElementById('modal-sair');
    if (m) m.style.display = 'none';
}

function abrirModalEliminar(event) {
    event.preventDefault();
    fecharMenuConta();
    var m = document.getElementById('modal-eliminar');
    if (m) m.style.display = 'flex';
}

function fecharModalEliminar() {
    var m = document.getElementById('modal-eliminar');
    if (m) m.style.display = 'none';
}

function toggleMenuConta(event) {
    if (event) {

        if (event.target.closest('.usuario-sidebar img')) return;
        event.stopPropagation();
    }
    var menu = document.getElementById('menu-conta');
    var gatilho = document.getElementById('usuario-sidebar-gatilho');
    if (!menu) return;
    var aberto = menu.classList.toggle('aberto');
    if (gatilho) gatilho.classList.toggle('aberto', aberto);
}

function fecharMenuConta() {
    var menu = document.getElementById('menu-conta');
    var gatilho = document.getElementById('usuario-sidebar-gatilho');
    if (menu) menu.classList.remove('aberto');
    if (gatilho) gatilho.classList.remove('aberto');
}

document.addEventListener('click', function (e) {
    var menu = document.getElementById('menu-conta');
    if (!menu || !menu.classList.contains('aberto')) return;
    if (!menu.contains(e.target) && !e.target.closest('#usuario-sidebar-gatilho')) {
        fecharMenuConta();
    }
});

function abrirModalDinamico(event, urlDestino) {
    event.preventDefault();
    var link = document.getElementById('link-confirmar-dinamico');
    var modal = document.getElementById('modal-dinamico');
    if (link) link.href = urlDestino;
    if (modal) modal.style.display = 'flex';
}

function fecharModalDinamico() {
    var m = document.getElementById('modal-dinamico');
    if (m) m.style.display = 'none';
}

function garantirPerfilLightbox() {
    if (document.getElementById('perfil-lightbox')) return;

    var lb = document.createElement('div');
    lb.id = 'perfil-lightbox';
    lb.className = 'perfil-lightbox';
    lb.innerHTML =
        '<span class="pl-fechar" title="Fechar">&times;</span>' +
        '<div class="pl-spinner"></div>' +
        '<img class="pl-img" alt="Foto de perfil ampliada">' +
        '<div class="pl-nome"></div>';
    document.body.appendChild(lb);

    lb.addEventListener('click', function (e) {
        if (e.target === lb || e.target.classList.contains('pl-fechar')) {
            fecharPerfilLightbox();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') fecharPerfilLightbox();
    });
}

function ampliarFotoPerfil(src, nome) {
    garantirPerfilLightbox();
    var lb = document.getElementById('perfil-lightbox');
    var img = lb.querySelector('.pl-img');
    var spinner = lb.querySelector('.pl-spinner');
    var nomeEl = lb.querySelector('.pl-nome');

    img.classList.remove('visivel');
    img.removeAttribute('src');
    spinner.style.display = 'block';
    nomeEl.textContent = nome || '';
    lb.classList.add('active');

    var pre = new Image();
    pre.onload = function () {
        img.src = src;
        spinner.style.display = 'none';
        requestAnimationFrame(function () {
            img.classList.add('visivel');
        });
    };
    pre.onerror = function () {
        spinner.style.display = 'none';
        nomeEl.textContent = 'Não foi possível carregar a foto.';
    };
    pre.src = src;
}

function fecharPerfilLightbox() {
    var lb = document.getElementById('perfil-lightbox');
    if (!lb) return;
    lb.classList.remove('active');
    var img = lb.querySelector('.pl-img');
    if (img) {
        img.classList.remove('visivel');
        img.removeAttribute('src');
    }
}

document.addEventListener('DOMContentLoaded', function () {

    document.body.addEventListener('click', function (e) {
        var img = e.target.closest('.usuario-sidebar img');
        if (!img) return;
        e.preventDefault();
        e.stopPropagation();
        var nome = '';
        var info = img.closest('.usuario-sidebar');
        if (info) {
            var span = info.querySelector('.usuario-info span');
            if (span) nome = span.textContent.trim();
        }
        ampliarFotoPerfil(img.getAttribute('src'), nome);
    });
});
