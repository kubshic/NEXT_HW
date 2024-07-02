const username = document.querySelector('.username');
const usernameWrapper = document.querySelector('.usernameWrapper');
const header = document.querySelector('#header');
const displayUsername = document.querySelector('#displayUsername');
const resetBtn = document.querySelector('#resetBtn');

function setUsername() {
    const name = username.value.trim();
    if (name === '') return; // Ignore empty input
    window.localStorage.setItem('username', name);
    username.value = '';
    checkUsername();
}

function checkUsername() {
    const checkName = window.localStorage.getItem('username');
    if (checkName) {
        usernameWrapper.style.display = 'none';
        displayUsername.innerHTML = `<h1>${checkName}의 투두리스트</h1>`;
        resetBtn.style.display = 'block';
    } else {
        usernameWrapper.style.display = 'flex';
        displayUsername.innerHTML = '';
        resetBtn.style.display = 'none';
    }
}

// 입력했던 사용자의 이름을 초기화하는 함수
function resetUsername() {
    window.localStorage.removeItem('username');
    checkUsername();
}

// Check username when the DOM content is loaded
document.addEventListener('DOMContentLoaded', checkUsername);
