//font = new FontFace('Roboto', 'url(../fonts/Roboto.ttf)');
//font.load().then(function() { document.fonts.add(font); });

button = document.getElementById('btn'); //кнопка
sideMenu = document.getElementById('side-menu'); //меню
textBox = document.getElementById("search"); //окно поиска

button.addEventListener('click', buttonClick); //добавление события нажатия кнопки
textBox.addEventListener("keypress", textBox_KeyPress); //добавление события нажатия на клавиатуру

n = 0;

function buttonClick() //функция нажатия кнопки
{
    if(n++ == 0) sideMenu.style.transform = 'translateX(175px)'; //document.querySelector('.side-panel').classList.add('open');
    else sideMenu.style.transform = 'translateX(0px)'; //document.querySelector('.side-panel').classList.remove('open');
    if(n > 1) n = 0; //button.value = n;
}

function textBox_KeyPress(event) //функция нажатия на клавиатуру
{
    if(event.key === "Enter")
    {
        document.getElementById("searchForm").submit();
    }
}