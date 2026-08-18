const toggleSenha = document.getElementById('toggleSenha');
const campoSenha = document.getElementById('senha');

toggleSenha.addEventListener('click', function () {
    const tipoAtual = campoSenha.getAttribute('type');
        campoSenha.setAttribute('type', tipoAtual === 'password' ? 'text' : 'password');
        toggleSenha.textContent = tipoAtual === 'password' ? '🙈' : '👁';
});