const API_URL = 'https://mik-backend-pqcb.onrender.com';
const API = {
  get base() {
    return (window.MIK_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
  },

  get token() {
    return localStorage.getItem('mik_access');
  },

  setTokens(tokens) {
    if (tokens.access) localStorage.setItem('mik_access', tokens.access);
    if (tokens.refresh) localStorage.setItem('mik_refresh', tokens.refresh);
  },

  clearAuth() {
    localStorage.removeItem('mik_access');
    localStorage.removeItem('mik_refresh');
    localStorage.removeItem('mik_user');
  },

  get user() {
    try { return JSON.parse(localStorage.getItem('mik_user') || 'null'); }
    catch { return null; }
  },

  setUser(u) {
    localStorage.setItem('mik_user', JSON.stringify(u));
  },

  async request(path, options = {}) {
    const headers = options.headers || {};
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = headers['Content-Type'] || 'application/json';
    }
    if (this.token) headers['Authorization'] = 'Bearer ' + this.token;

    const res = await fetch(this.base + path, { ...options, headers });
    let data = null;
    const ct = res.headers.get('content-type') || '';
    if (ct.includes('application/json')) {
      data = await res.json();
    }

    if (res.status === 401) {
      // Tentar refresh
      const refreshed = await this.tryRefresh();
      if (refreshed) return this.request(path, options);
      this.clearAuth();
      if (!location.pathname.endsWith('login.html') && !location.pathname.endsWith('cadastro.html')) {
        location.href = 'login.html';
      }
      throw new Error('Sessão expirada');
    }

    if (!res.ok) {
      const err = new Error((data && (data.erro || data.detail)) || 'Erro na pedido');
      err.status = res.status;
      err.data = data;
      throw err;
    }
    return data;
  },

  async tryRefresh() {
    const refresh = localStorage.getItem('mik_refresh');
    if (!refresh) return false;
    try {
      const res = await fetch(this.base + '/api/auth/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      if (data.access) {
        localStorage.setItem('mik_access', data.access);
        return true;
      }
    } catch (_) {}
    return false;
  },

  // Auth
  login(login_input, password) {
    return this.request('/api/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ login_input, password }),
    });
  },
  register(formData) {
    return this.request('/api/auth/register/', { method: 'POST', body: formData });
  },
  me() { return this.request('/api/auth/me/'); },
  updateMe(data) {
    const isForm = data instanceof FormData;
    return this.request('/api/auth/me/', {
      method: 'PATCH',
      body: isForm ? data : JSON.stringify(data),
      headers: isForm ? {} : { 'Content-Type': 'application/json' },
    });
  },
  changePassword(payload) {
    return this.request('/api/auth/me/password/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  deleteAccount(senha_confirmacao) {
    return this.request('/api/auth/me/delete/', {
      method: 'POST',
      body: JSON.stringify({ senha_confirmacao }),
    });
  },

  // Conteúdo
  home() { return this.request('/api/home/'); },
  eventos() { return this.request('/api/eventos/'); },
  galeria() { return this.request('/api/galeria/'); },
  contacto(payload) {
    return this.request('/api/contacto/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // Admin
  membros() { return this.request('/api/auth/membros/'); },
  mudarNivel(payload) {
    return this.request('/api/auth/membros/nivel/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  adminEventos() { return this.request('/api/admin/eventos/'); },
  criarEvento(payload) {
    return this.request('/api/admin/eventos/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  eliminarEvento(id) {
    return this.request('/api/admin/eventos/' + id + '/', { method: 'DELETE' });
  },
  adminGaleria() { return this.request('/api/admin/galeria/'); },
  adicionarFoto(formData) {
    return this.request('/api/admin/galeria/', { method: 'POST', body: formData });
  },
  eliminarFoto(id) {
    return this.request('/api/admin/galeria/' + id + '/', { method: 'DELETE' });
  },
  mensagens() { return this.request('/api/admin/mensagens/'); },
  eliminarMensagem(id) {
    return this.request('/api/admin/mensagens/' + id + '/', { method: 'DELETE' });
  },
  historico() { return this.request('/api/admin/historico/'); },
  alertas() { return this.request('/api/admin/alertas/'); },
  marcarAlertas(payload) {
    return this.request('/api/admin/alertas/marcar/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  senhaSeguranca(payload) {
    return this.request('/api/auth/seguranca/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
};

window.API = API;
