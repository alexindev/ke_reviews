const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const closeButton = document.querySelector('.alert .close');
const storeItems = document.querySelectorAll('.store-items');
const newStoreForm = document.querySelector('#new-store');
const reviewForm = document.querySelector('#review-data');
const messageAlertElem = document.querySelector('.alert');
const avatarForm = document.querySelector('#avatar-form');
const avatarInput = document.querySelector('#avatar-input');


// закрыть информационное окно с собщениями
closeButton.addEventListener('click', function () {
    messageAlertElem.style.display = 'none';
});


function messageAlert(message, status) {
    messageAlertElem.style.display = 'block';
    messageAlertElem.classList.remove('alert-success', 'alert-danger');
    messageAlertElem.classList.add(status === true ? 'alert-success' : 'alert-danger');
    const messageText = document.querySelector('#message-text');
    messageText.textContent = message;
}


function updateStoreStatus(storeElement, storeId, newStatus) {
    storeElement.innerHTML = newStatus === 'True'
        ? '<i class="fa fa-pause fa-lg text-warning mr-2" aria-hidden="true"></i>'
        : '<i class="fa fa-play fa-lg text-success mr-2" aria-hidden="true"></i>'
    storeElement.dataset.storeStatus = newStatus === 'True' ? 'True' : 'False'
}


// управление статусом и удалением магазинов
storeItems.forEach(storeItem => {
    const storeId = storeItem.dataset.storeId;
    const storeStatus = storeItem.querySelector('.store-status');
    const storeDelete = storeItem.querySelector('.store-delete')

    // изменить статус магазина
    storeStatus.addEventListener('click', function (e) {
        e.preventDefault();
        const storeStatus = this.dataset.storeStatus;
        const url = `api/v1/store_status/`;
        fetch(
            url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(
                    {
                        store_id: storeId,
                        store_status: storeStatus,
                    }
                )
            }
        )
            .then(response => response.json())
            .then(data => {
                if (!('message' in data)) {
                    updateStoreStatus(this, storeId, data.store_status);
                } else {
                    messageAlert(data.message, data.status)
                }
            })
            .catch(error => {
                    console.error('Ошибка смены статуса:', error);
                }
            )
    })

    // удалить магазин
    storeDelete.addEventListener('click', function (e) {
        e.preventDefault();
        const url = `api/v1/delete_store/`;
        fetch(
            url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(
                    {
                        store_id: storeId
                    }
                )
            }
        )
            .then(response => response.json())
            .then(data => {
                storeItem.remove()
                messageAlert(data.message, data.status)
            })
            .catch(error => {
                console.log('Ошибка при удаления магазина:', error)
            })
    })
})


// добавить новый магазин
newStoreForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const newStoreInput = document.querySelector('#store-url')
    const newStoreValue = newStoreInput.value
    const url = 'api/v1/new_store/'
    fetch(
        url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(
                {
                    new_store: newStoreValue
                }
            )
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === true) {
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
            }
            messageAlert(data.message, data.status)
        })
        .catch(error => {
                console.log('Ошибка добавления магазина:', error)
            }
        )
});


// форма получения данных для отзывов
reviewForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const reviewLogin = document.querySelector('#review-login').value
    const reviewPassword = document.querySelector('#review-password').value
    const url = 'api/v1/review/'
    fetch(
        url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(
                {
                    login: reviewLogin,
                    password: reviewPassword
                }
            )
        })
        .then(response => response.json())
        .then(data => {
            messageAlert(data.message, data.status)
        })
        .catch(error => {
                console.log('Ошибка добавления учетной записи для отзывов', error)
            }
        )
});


// добавить/изменить аватар пользователя
avatarForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const url = 'api/v1/avatar/'
    const userPicture = document.querySelector('#avatar-input')
    const formData = new FormData();
    formData.append('picture', userPicture.files[0]);
    fetch(
        url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData

        })
        .then(response => response.json())
        .then(data => {
            messageAlert(data.message, data.status)
        })
        .catch(error => {
                console.log('Ошибка изменения аватар', error)
            }
        )
});


// название картинки в поле input
avatarInput.addEventListener('change', function () {
    const file = avatarInput.files[0];
    const fileName = file.name;
    const labelElement = document.querySelector('label[for="avatar-input"]');
    labelElement.textContent = fileName.slice(0, 30) + '...';
});
