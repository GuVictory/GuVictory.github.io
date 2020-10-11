const mainUrl = 'http://localhost:8000/api/'
const app = document.getElementById('app');

if (!app) console.log('app not found');

app.addEventListener('click', (evt) => {
    evt.preventDefault();

    switch(evt.target.tagName) {
        case 'A':
            navbarLinkClicked(evt.target.getAttribute('section'));
            break;
        case 'DIV':
            if(evt.target.classList.contains("card")) {
                cardClicked(evt.target.getAttribute('card_section'));
            }
            break;

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
            newElement =  `<div class="card" card_section="${linkUrl}/${element.id}">
                                <span class="card_title text">${element.title}</span>
                                <div class="hr"></div>
                                <footer class="card__footer">
                                    <i class="card_edit far fa-edit" card_section="${linkUrl}/${element.id}"></i>
                                    <i class="card_delete far fa-trash-alt" card_section="${linkUrl}/${element.id}"></i>
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