const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const messageAlertElem = document.querySelector('.alert');


// Закрыть информационное окно с сообщениями
if (window.location.pathname === '/users/auth/' || window.location.pathname === '/users/register/') {
    const closeButton = document.querySelector('.alert .close');  // Выберите кнопку закрытия внутри .alert
    closeButton.addEventListener('click', function () {
        messageAlertElem.remove();
    });
}


// Вывод уведомлений
function messageAlert(message, status) {
    // информационное окно
    messageAlertElem.style.display = 'block';
    messageAlertElem.classList.remove('alert-success', 'alert-danger');
    messageAlertElem.classList.add(status === true ? 'alert-success' : 'alert-danger');
    const messageText = document.querySelector('#message-text');
    messageText.textContent = message;
}


// страница авторизации
function authPage() {
    const authForm = document.querySelector('#form-auth')
    authForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(authForm)
        const login = formData.get('login-user')
        const password = formData.get('login-pass')

        if (login && password) {
            const url = `${window.location.origin}/api/v1/auth/`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    username: login,
                    password: password
                })
            })
                .then(response => {
                    if (response.status === 200) {
                        window.location.href = `${window.location.origin}/profile/dashboard/`;
                    } else {
                        return response.json()
                    }
                })
                .then(data => {
                    if (data) {
                        messageAlert(data.message, false)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        } else {
            messageAlert('Необходимо заполнить все поля', false)
        }
    })
}


// страница регистрации
function registerPage() {
    const regForm = document.querySelector('#form-reg')
    regForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(regForm)
        const login = formData.get('reg-name')
        const password = formData.get('reg-pass')
        const passwordConfirm = formData.get('reg-pass-confirm')

        if (login && password && passwordConfirm) {
            if (password !== passwordConfirm) {
                messageAlert('Пароли не совпадают', false)
            } else {
                const url = `${window.location.origin}/api/v1/register/`;
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        username: login,
                        password: password
                    })
                })
                    .then(response => {
                        if (response.status === 201) {
                            window.location.href = `${window.location.origin}/users/auth/`;
                        } else {
                            return response.json()
                        }
                    })
                    .then(data => {
                        if (data) {
                            messageAlert(data.message, false)
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        } else {
            messageAlert('Необходи заполнить все поля', false)
        }
    })
}


if (window.location.pathname === '/users/auth/') {
    authPage()
}

if (window.location.pathname === '/users/register/') {
    registerPage()
}