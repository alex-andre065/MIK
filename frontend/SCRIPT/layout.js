/**
 * Layout comum do MIK — adaptado do layout do projeto PHP.
 * Mantém a separação front-end/API do Django.
 */
(function () {
  function esc(s) {
    var d = document.createElement('div');
    d.textContent = s || '';
    return d.innerHTML;
  }

  function user() {
    try { return JSON.parse(localStorage.getItem('mik_user') || 'null'); } catch (e) { return null; }
  }

  window.MIK_sair = function () {
    if (window.API) API.clearAuth();
    location.href = 'login.html';
  };

  window.MIK_requireAuth = function () {
    if (!localStorage.getItem('mik_access')) {
      location.href = 'login.html';
      return false;
    }
    return true;
  };

  window.MIK_renderShell = function (opts) {
    opts = opts || {};
    var u = user() || {};
    var foto = u.foto_url || 'img/padrao.jpg';
    var nome = u.nome || 'Utilizador';
    var telefone = u.telefone || '';
    var isAdmin = u.nivel === 'admin' || u.is_admin;
    var subtitulo = opts.subtitulo || 'Somos Apostólicos, Somos Proféticos, Somos MIK';
    var pagina = opts.pagina || '';

    var header = document.getElementById('mik-header');
    if (header) {
      header.innerHTML =
        '<a class="logo" href="index.html">' +
          '<img src="img/IMG-20260708-WA0001.jpg" alt="MIK" onerror="this.style.display=\'none\'">' +
          '<div class="info"><h5>MIK</h5><p>' + esc(subtitulo) + '</p></div>' +
        '</a>' +
        '<button class="menu-btn" type="button" onclick="toggleSidebar(event)" aria-label="Abrir menu"><span class="hamburger-icon" aria-hidden="true">☰</span></button>';
    }

    var sidebar = document.getElementById('mik-sidebar');
    if (sidebar) {
      function link(href, label, active) {
        return '<a href="' + href + '"' + (active ? ' class="ativo"' : '') + '>' + label + '</a>';
      }

      sidebar.innerHTML =
        '<button class="close-btn" onclick="fecharSidebar()">X</button>' +
        '<div class="usuario-sidebar" id="usuario-sidebar-gatilho" onclick="toggleMenuConta(event)">' +
          '<img src="' + esc(foto) + '" alt="Foto de Perfil" id="user-foto" onerror="this.src=\'img/padrao.jpg\'">' +
          '<div class="usuario-info">' +
            '<span id="user-nome">' + esc(nome) + '</span>' +
            '<p style="display:flex;align-items:center;gap:6px;">' +
              '<span style="display:inline-block;width:8px;height:8px;background-color:#28a745;border-radius:50%;box-shadow:0 0 6px #28a745;"></span> Conta Ativa</p>' +
            '<p class="usuario-telefone" id="user-sub">' + esc(telefone) + '</p>' +
          '</div>' +
          '<span class="seta-menu-conta">&#9662;</span>' +
        '</div>' +
        '<div class="menu-conta" id="menu-conta">' +
          '<a href="definicoes.html" class="menu-conta-item"><span class="menu-conta-icone">&#9881;&#65039;</span> Definições da Conta</a>' +
          (isAdmin ? '<a href="admin.html" class="menu-conta-item"><span class="menu-conta-icone">&#128737;</span> Painel Administrativo</a>' : '') +
          '<button type="button" class="menu-conta-item menu-conta-tema" onclick="alternarTema()">' +
            '<span style="display:flex;align-items:center;gap:12px;"><span class="menu-conta-icone toggle-tema-icone">&#127769;</span><span class="toggle-tema-texto">Modo escuro</span></span>' +
            '<span class="menu-conta-switch"></span></button>' +
          '<div class="menu-conta-separador"></div>' +
          '<a href="#" class="menu-conta-item menu-conta-perigo" onclick="abrirModal(event);return false;"><span class="menu-conta-icone">&#128682;</span> Sair do Site</a>' +
          '<a href="eliminar-conta.html" class="menu-conta-item menu-conta-perigo"><span class="menu-conta-icone">&#128465;&#65039;</span> Eliminar Conta</a>' +
        '</div>' +
        '<nav class="sidebar-links">' +
          link('index.html', '🏠 Início', pagina === 'inicio') +
          link('sobre.html', '❓ Sobre', pagina === 'sobre') +
          link('eventos.html', '📅 Eventos', pagina === 'eventos') +
          link('contacto.html', '📞 Contacto', pagina === 'contacto') +
          link('galeria.html', '📷 Galeria', pagina === 'galeria') +
          (!isAdmin ? link('definicoes.html', '⚙️ Definições', pagina === 'definicoes') : '') +
          (isAdmin ? '<a href="admin.html" style="color:#28a745;font-weight:bold;">⚙️ Painel Administrativo</a>' : '') +
        '</nav>';
    }

    if (!document.getElementById('modal-sair')) {
      var m = document.createElement('div');
      m.id = 'modal-sair';
      m.className = 'modal-container';
      m.innerHTML =
        '<div class="modal-box">' +
          '<h3>Terminar Sessão</h3>' +
          '<p>Tens a certeza que queres sair do site?</p>' +
          '<div class="modal-botoes">' +
            '<button class="btn-cancelar" onclick="fecharModal()">Cancelar</button>' +
            '<button class="btn-confirmar" onclick="MIK_sair()">Sim, Sair</button>' +
          '</div>' +
        '</div>';
      document.body.appendChild(m);
    }
  };
})();
