const mainUrl = 'https://www.guvictory.xyz/api/';

async function helpTabChange(event, tabName) {

    let i, tabcontent, tablinks;
    
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks-js");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "flex";
    event.currentTarget.className += " active";

    await getDataForPage(tabName);
};

async function getDataForPage(dataType) {

    current_url = dataType == 'Student' ? 'student' : 'instructor';
    el_id = dataType == 'Student' ? 0: 1;

    let questions = await fetch(mainUrl + current_url + '_questions/');
    questions = await questions.json();
    let topics = await fetch(mainUrl + current_url + '_topics/');
    topics = await topics.json();

    questionsParent = document.getElementsByClassName('help__questions__content')[el_id];
    topicsParent = document.getElementsByClassName('help__topics__content')[el_id];

    questionsParent.innerHTML = '';
    questions.forEach((val) => {
        console.log(val);
        questionsParent.innerHTML +=
        `
            <div class="help__questions__content__card">
                <span class="text">${val.title}</span>
            </div>
        `;
    });

    topicsParent.innerHTML = '';
    topics.forEach((val) => {
        topicsParent.innerHTML +=
        `
            <div class="help__topics__content__card">
                <i class="help-icon far fa-grin-stars"></i>
                <div class="hr"></div>
                <span class="text">${val.title}</span>
            </div>
        `;
    });
};