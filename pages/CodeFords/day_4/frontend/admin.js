const mainUrl = 'https://www.guvictory.xyz/api/'
const app = document.getElementById('app');

if (!app) console.log('app not found');

navbarLinkClicked('student_questions')

app.addEventListener('click', (evt) => {
    evt.preventDefault();

    if (evt.target.getAttribute('section') == 'create_new') {
        createNew();
    }
    else if(evt.target.getAttribute('section') == 'card') {
        if(evt.target.tagName == 'DIV') {
            cardClicked(evt.target.getAttribute('card_section'));
        }
    }
    else {
        if (evt.target.parentNode.tagName == 'NAV') {
            prevLink = document.querySelector('.navbar__item.active');
            prevLink.classList.remove('active');
            evt.target.classList.add('active');
            navbarLinkClicked(evt.target.getAttribute('section'));
        }
    }
});

async function navbarLinkClicked(linkUrl) {
    let response = await fetch(mainUrl + linkUrl + '/');
    if (response.ok) { // if HTTP-status is 200-299
        let json = await response.json();

        // Изменим название раздела
        mainTitle = document.getElementById('main_title_js');
        mainTitle.innerHTML = linkUrl.split('_')[0] + ' ' + linkUrl.split('_')[1];

        // Подгрузим все карточки в html дерево
        mainBody = document.getElementById('main__body');
        mainBody.innerHTML = '';
        json.forEach((element) => {
            newElement =  `<div class="card" card_section="${linkUrl}/${element.id}" section="card">
                                <span class="card_title text">${element.title}</span>
                                <div class="hr"></div>
                                <footer class="card__footer">
                                    <i 
                                        class="card_edit far fa-edit" 
                                        card_section="${linkUrl}/${element.id}" 
                                        section="card" 
                                        onclick="onEditButtonClicked('${linkUrl}/${element.id}')">
                                    </i>
                                    <i 
                                        class="card_delete far fa-trash-alt" 
                                        card_section="${linkUrl}/${element.id}" 
                                        section="card" 
                                        onclick="onDeleteButtonClicked('${linkUrl}/${element.id}')">
                                        </i>
                                </footer>
                            </div>`
            mainBody.innerHTML += newElement;
        });

    } else {
        alert("HTTP-Error: " + response.status);
    }
}

async function cardClicked(linkUrl) {
    let response = await fetch(mainUrl + linkUrl);
    if (response.ok) { // if HTTP-status is 200-299
        let json = await response.json();
        console.log(json);
    } else {
        alert("HTTP-Error: " + response.status);
    }
}

async function createNew() {
    mainTitle = document.getElementById('main_title_js');
    current_url = mainTitle.textContent.toLowerCase().split(' ').join('_');


    textForFormHeader = mainTitle.textContent.slice(0, -1);

    mainBody = document.getElementById('main__body');
    mainBody.innerHTML = '';
    formNode = `
                <div class="form">
                    <span class="form__title text text--uppercase text--bold">Create new ${textForFormHeader}</span>
                    <textarea name="title" type="text" placeholder="Title for card" class="text form__input" id="create_input" ></textarea> 
                    <div class="form__buttons">
                        <button class="button form__button_cancle" id="cancle_button" onclick="onCancleClicked('${current_url}')">
                            <span class="text form__button__text">Cancle</span>
                        </button>
                        <button class="button primary form__button_create" onclick="onCreateButtonClicked()">
                            <span class="text form__button__text">Create</span>
                        </button>
                    </div>
                </div>
                `
    mainBody.innerHTML += formNode;
}

async function onCreateButtonClicked() {
    mainTitle = document.getElementById('main_title_js');
    current_url = mainTitle.textContent.toLowerCase().split(' ').join('_');

    inputText = document.getElementById('create_input');
    data = {
        'title': inputText.value,
    }

    if(inputText.value != '') {
        let response = await fetch(mainUrl + current_url + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data)
            });
    }

    navbarLinkClicked(current_url);
}

async function onEditButtonClicked(linkUrl) {
    mainTitle = document.getElementById('main_title_js');
    current_url = mainTitle.textContent.toLowerCase().split(' ').join('_');

    let response = await fetch(mainUrl + linkUrl);

    if (response.ok) {
        let json = await response.json();

        mainBody = document.getElementById('main__body');
        mainBody.innerHTML = '';

        textForFormHeader = linkUrl.split('/').join(' ');
        formNode = `
                <div class="form">
                    <span class="form__title text text--uppercase text--bold">Edit ${textForFormHeader}</span>
                    <textarea
                        name="title"
                        type="text"
                        placeholder="Title for card"
                        class="text form__input"
                        id="edit_input"
                        rows=5>${json.title}</textarea>
                    <div class="form__buttons">
                        <button class="button form__button_cancle" onclick="onCancleClicked('${current_url}')">
                            <span class="text form__button__text">Cancle</span>
                        </button>
                        <button
                            class="button primary form__button_create"
                            onclick="onSaveButtonClicked('${current_url}','${json.id}')">
                            <span class="text form__button__text">Save</span>
                        </button>
                    </div>
                </div>
                `
        mainBody.innerHTML += formNode;
    } else {
        alert("HTTP-Error: " + response.status);
    }
}

async function onCancleClicked(prevUrl) {
    navbarLinkClicked(prevUrl);
}

async function onSaveButtonClicked(linkUrl, id) {
    inputText = document.getElementById('edit_input');

    data = {
        'title': inputText.value,
    }

    if(inputText.value != '') {
        let response = await fetch(mainUrl + linkUrl + '/' + id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data)
        });

        if(response.ok) {
            navbarLinkClicked(linkUrl);
        } else {
            alert("HTTP-Error: " + response.status);
        }
    }
}

async function onDeleteButtonClicked(linkUrl) {
    response = await fetch(mainUrl + linkUrl, {
        method: 'DELETE',
    });
    navbarLinkClicked(linkUrl.split('/')[0]);
}

const openMobileMenu = (evt) => {
    navbar = document.getElementById('navbar');
    menuBtn = document.getElementById('menu_icon');

    if(menuBtn.classList.contains('open')) {
        menuBtn.classList.remove('open');
        navbar.classList.remove('open');
    } else {
        menuBtn.classList.add('open');
        navbar.classList.add('open');
    }
}