const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const closeButton = document.querySelector('.alert .close');
const messageAlertElem = document.querySelector('.alert');


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
    const storeDelete = storeItem.querySelector('.store-delete');
    const storeStatus = storeItem.querySelector('.store-status');

    // Изменить статус магазина
    if (storeStatus.contains(targetElement)) {
        const storeStatusValue = storeStatus.dataset.storeStatus;
        const url = `${window.location.origin}/api/v1/store_status/`;
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
        const url = `${window.location.origin}/api/v1/delete_store/`;
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


// Страница настроек
if (window.location.pathname === '/profile/settings/') {

    // Блок со всеми магазинами в настройках
    document.querySelector('.stores-container').addEventListener('click', handleStoreItemClick);

    // Добавить новый магазин
    const newStoreForm = document.querySelector('#new-store');
    newStoreForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const newStoreInput = document.querySelector('#store-url')
        const newStoreValue = newStoreInput.value;
        const url = `${window.location.origin}/api/v1/new_store/`;
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
                }
                messageAlert(data.message, data.status)
            })
            .catch(error => {
                console.log(error)
            })
    });


    // Форма получения данных для отзывов
    const reviewForm = document.querySelector('#review-data');
    reviewForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const reviewLogin = document.querySelector('#review-login').value
        const reviewPassword = document.querySelector('#review-password').value
        const url = `${window.location.origin}/api/v1/review/`;
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

    // Получить новый токен
    const getTokenBtn = document.querySelector('#get-token')
    getTokenBtn.addEventListener('click', function (e) {
        e.preventDefault();
        getTokenBtn.disabled = true;
        const url = `${window.location.origin}/api/v1/get_token/`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                messageAlert(data.message, data.status);
                if (data.status) {
                    setTimeout(() => getTokenTaskStatus(data.task_id), 1000)
                } else {
                    getTokenBtn.disabled = false;
                }
            })
            .catch(error => {
                console.log(error)
            })
    })

    // Получить статус таска при получении токена
    function getTokenTaskStatus(taskId) {
        fetch(`${window.location.origin}/api/v1/get_task_status/?task_id=${taskId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status) {
                    if (data.token) {
                        messageAlert(data.message, true)
                        changeTokenMessage()
                        getTokenBtn.disabled = false;
                    } else {
                        messageAlert(data.message, true)
                        setTimeout(() => getTokenTaskStatus(taskId), 1000)
                    }
                } else {
                    console.log('epic fail')
                    messageAlert(data.message, false)
                    getTokenBtn.disabled = false;
                }
            })
            .catch(error => {
                console.log(error)
                getTokenBtn.disabled = false;
            })
    }

    // Изменить сообщение в поле управления токеном
    function changeTokenMessage() {
        const tokenMessage = document.querySelector('.token-info')
        getTokenBtn.textContent = 'Обновить токен'
        if (tokenMessage) {
            tokenMessage.textContent = 'Токен получен';
            tokenMessage.classList.remove('text-gray');
            tokenMessage.classList.add('text-success');
        }
    }


    // Добавить/изменить аватар пользователя
    const avatarForm = document.querySelector('#avatar-form');
    avatarForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const url = `${window.location.origin}/api/v1/avatar/`
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
    const avatarInput = document.querySelector('#avatar-input');
    avatarInput.addEventListener('change', function () {
        const file = avatarInput.files[0];
        const fileName = file.name;
        const labelElement = document.querySelector('label[for="avatar-input"]');
        labelElement.textContent = fileName.slice(0, 30) + '...';
    });
}


// Страница с отзывами
if (window.location.pathname === '/profile/reviews/') {

    // Кнопка обновить отзывы
    const updateReviewsBtn = document.querySelector('#update-reviews')

    if (updateReviewsBtn) {

        // При загрузке страницы сразу загружаем первую страницу отзывов
        loadPage(`${window.location.origin}/api/v1/get_reviews/`);

        updateReviewsBtn.addEventListener('click', function (e) {
            e.preventDefault();
            fetch(`${window.location.origin}/api/v1/update_reviews/`)
                .then(response => response.json())
                .then(data => {
                    messageAlert(data.message, data.status)
                    setTimeout(()=> loadPage(`${window.location.origin}/api/v1/get_reviews/`), 3000);
                })
        })
    }
}

function renderReviewsTable(data) {
    const reviewsTable = document.querySelector('.table');
    reviewsTable.innerHTML = `
      <thead>
        <tr>
          <th>Магазин</th>
          <th>Название товара</th>
          <th>Рейтинг</th>
          <th>Текст отзыва</th>
          <th>Отзыв получен</th>
        </tr>
      </thead>
      <tbody>
        ${data.results.map(review => `
          <tr>
            <td>${review.store}</td>
            <td class="w-25 text-wrap">${review.product}</td>
            <td>${review.rating}</td>
            <td class="w-75 text-wrap text-sm">${review.content}</td>
            <td>${review.date_create}</td>
          </tr>
        `).join('')}
      </tbody>
    `;
}


// Функция для создания кнопок пагинации с использованием стилей Bootstrap
function createPaginationButtons(data) {
    const paginationUl = document.querySelector('.pagination');
    paginationUl.innerHTML = ''; // Очищаем содержимое, если есть

    if (data.items !== 0) {
        // Кнопки для всех доступных страниц
        for (let pageNumber = 1; pageNumber <= data.total_pages; pageNumber++) {
            const pageButton = document.createElement('li');
            pageButton.classList.add('page-item');
            if (pageNumber === data.current_page) {
                pageButton.classList.add('active');
            }
            pageButton.innerHTML = `
                <button class="page-link ml-1">${pageNumber}</button>
            `;
            pageButton.addEventListener('click', function () {
                loadPage(`${window.location.origin}/api/v1/get_reviews/?page=${pageNumber}`);
            });
            paginationUl.appendChild(pageButton);
        }
    }
}


// Функция для загрузки данных и отображения таблицы и пагинации
function loadPage(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderReviewsTable(data);
            createPaginationButtons(data);
        })
        .catch(error => {
            console.error('Ошибка при получении данных:', error);
        });
}

