const closeButton = document.querySelector('.alert .close');
const newStoreForm = document.querySelector('#new-store');
const reviewForm = document.querySelector('#review-data');
const messageAlertElem = document.querySelector('.alert');
const avatarForm = document.querySelector('#avatar-form');
const avatarInput = document.querySelector('#avatar-input');


document.querySelector('.stores-container').addEventListener('click', handleStoreItemClick);


// Закрыть информационное окно с собщениями
closeButton.addEventListener('click', function () {
    messageAlertElem.style.display = 'none';
});


// Вывод опевещений
function messageAlert(message, status) {
    messageAlertElem.style.display = 'block';
    messageAlertElem.classList.remove('alert-success', 'alert-danger');
    messageAlertElem.classList.add(status === true ? 'alert-success' : 'alert-danger');
    const messageText = document.querySelector('#message-text');
    messageText.textContent = message;
}


// Изменить иконку статуса магазинов
function updateStoreStatus(storeElement, storeId, newStatus) {
    storeElement.innerHTML = newStatus === 'True'
        ? '<i class="fa fa-pause fa-lg text-warning mr-2" aria-hidden="true"></i>'
        : '<i class="fa fa-play fa-lg text-success mr-2" aria-hidden="true"></i>'
    storeElement.dataset.storeStatus = newStatus === 'True' ? 'True' : 'False'
}


// Отправка и получение запроса
function fetchData(url, method, contentType, bodyData) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const headers = {
        'X-CSRFToken': csrfToken,
    };

    if (contentType) {
        headers['Content-Type'] = contentType;
    }

    return fetch(url, {
        method: method,
        headers: headers,
        body: bodyData
    })
        .then(response => response.json())
        .catch(error => {
            console.log(error)
        })
}


// Функция для обработки клика по элементам store-items
function handleStoreItemClick(event) {
    event.preventDefault();
    const targetElement = event.target;
    const storeItem = targetElement.closest('.store-items');

    if (!storeItem) return;

    const storeId = storeItem.dataset.storeId;
    const storeStatus = storeItem.querySelector('.store-status');
    const storeDelete = storeItem.querySelector('.store-delete');

    // Изменить статус магазина
    if (storeStatus.contains(targetElement)) {
        const storeStatusValue = storeStatus.dataset.storeStatus;
        const url = `api/v1/store_status/`;
        const bodyData = JSON.stringify({
            store_id: storeId,
            store_status: storeStatusValue,
        });

        fetchData(url, 'PUT', 'application/json', bodyData)
            .then(data => {
                if (data.status) {
                    updateStoreStatus(storeStatus, storeId, data.message);
                } else {
                    messageAlert(data.message, data.status);
                }
            })
            .catch(error => {
                console.log(error);
            });
    }

    // Удалить магазин
    if (storeDelete.contains(targetElement)) {
        const url = `api/v1/delete_store/`;
        const bodyData = JSON.stringify({
            store_id: storeId,
        });

        fetchData(url, 'DELETE', 'application/json', bodyData)
            .then(data => {
                storeItem.remove();
                messageAlert(data.message, data.status);
            })
            .catch(error => {
                console.log(error);
            });
    }
}


// Добавить новый магазин
newStoreForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const newStoreInput = document.querySelector('#store-url')
    const newStoreValue = newStoreInput.value
    const url = 'api/v1/new_store/'
    const bodyData = JSON.stringify(
        {
            new_store: newStoreValue
        }
    )
    fetchData(url, 'POST', 'application/json', bodyData)
        .then(data => {
            if (data.status) {
                const newStoreItem = document.createElement('div');
                newStoreItem.classList.add('store-items');
                newStoreItem.setAttribute('data-store-id', data.store_id);
                newStoreItem.innerHTML = `
                    <a href="#" class="store-delete" data-action="store-delete">
                        <i class="fa fa-trash-o fa-lg mr-2" aria-hidden="true"></i>
                    </a>
                    <a href="#" class="store-status" data-action="store-status" data-store-status="False">
                        <i class="fa fa-play fa-lg text-success mr-2" aria-hidden="true"></i>
                    </a>
                    ${newStoreValue}
                `;

                const storesContainer = document.querySelector('.stores-container');
                storesContainer.appendChild(newStoreItem);
                // storeItems = document.querySelectorAll('.store-items');
                // console.log(storeItems)
            }
            messageAlert(data.message, data.status)
        })
        .catch(error => {
            console.log(error)
        })
});


// Форма получения данных для отзывов
reviewForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const reviewLogin = document.querySelector('#review-login').value
    const reviewPassword = document.querySelector('#review-password').value
    const url = 'api/v1/review/'
    const bodyData = JSON.stringify(
        {
            login: reviewLogin,
            password: reviewPassword
        }
    )
    fetchData(url, 'PUT', 'application/json', bodyData)
        .then(data => {
            messageAlert(data.message, data.status)
        })
        .catch(error => {
            console.log(error)
        })
});


// Добавить/изменить аватар пользователя
avatarForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const url = 'api/v1/avatar/'
    const userPicture = document.querySelector('#avatar-input')
    const formData = new FormData();
    formData.append('picture', userPicture.files[0]);
    fetchData(url, 'POST', '', formData)
        .then(data => {
            if (data.status) {
                const profileIMG = document.querySelector('.profile-img');
                profileIMG.src = URL.createObjectURL(formData.get('picture'));
            }
        })
        .catch(error => {
            console.log(error)
        })
});


// Название картинки в поле input
avatarInput.addEventListener('change', function () {
    const file = avatarInput.files[0];
    const fileName = file.name;
    const labelElement = document.querySelector('label[for="avatar-input"]');
    labelElement.textContent = fileName.slice(0, 30) + '...';
});
