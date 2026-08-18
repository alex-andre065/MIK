function requireAuth() {
  if (!window.API || !API.token) location.href = 'login.html';
}
function sair() {
  API.clearAuth();
  location.href = 'login.html';
}
function fillUser() {
  const u = API.user;
  if (!u) return;
  const nome = document.getElementById('user-nome');
  const foto = document.getElementById('user-foto');
  const admin = document.getElementById('link-admin');
  if (nome) nome.textContent = u.nome || '';
  if (foto && u.foto_url) foto.src = u.foto_url;
  if (admin && (u.nivel === 'admin' || u.is_admin)) admin.style.display = '';
}
function esc(s) {
  const d = document.createElement('div');
  d.textContent = s || '';
  return d.innerHTML;
}
