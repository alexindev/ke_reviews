const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const closeButton = document.querySelector('.alert .close');
const storeElements = document.querySelectorAll('.store-status');
const newStoreForm = document.querySelector('#new-store');
const reviewForm = document.querySelector('#review-data');
const messageAlertElem = document.querySelector('.alert');


// закрыть информационное окно с собщениями
closeButton.addEventListener('click', function () {
    messageAlertElem.style.display = 'none';
});

function updateStoreStatus(storeId, newStatus) {
    const storeElement = document.querySelector(`[data-store-id="${storeId}"]`);

    storeElement.innerHTML = newStatus === 'True'
        ? '<i class="fa fa-pause fa-lg text-warning mr-2" aria-hidden="true"></i>'
        : '<i class="fa fa-play fa-lg text-success mr-2" aria-hidden="true"></i>'

    storeElement.dataset.storeStatus = newStatus === 'True' ? 'True' : 'False'
}

// изменить статус магазина
storeElements.forEach((element) => {
    element.addEventListener('click', function (e) {
        e.preventDefault();
        const storeId = element.dataset.storeId;
        const storeStatus = element.dataset.storeStatus;
        const url = `api/v1/store_status/${storeId}/`;
        fetch(
            url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(
                    {
                        store_status: storeStatus,
                    }
                ),
            })
            .then(response => response.json())
            .then(data => {
                updateStoreStatus(storeId, data.store_status);
            })
            .catch(error => {
                    console.error('Ошибка смены статуса:', error);
                }
            );
    });
});

function messageAlert(message, status) {
    messageAlertElem.style.display = 'block';
    messageAlertElem.classList.remove('alert-success', 'alert-danger');
    messageAlertElem.classList.add(status === true ? 'alert-success' : 'alert-danger');

    const messageText = document.querySelector('#message-text');
    messageText.textContent = message;
}

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
            messageAlert(data.message, data.status)
        })
        .catch(error => {
            console.log('Ошибка добавления магазина:', error)
        }
    )
})

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
        .catch(error =>{
            console.log('Ошибка добавления учетной записи для отзывов', error)
        }
    );
})