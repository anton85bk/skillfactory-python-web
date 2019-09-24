/* вспомогательные функции */

function setCookie(name, value, options = {}) {

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }
  document.cookie = updatedCookie;
}

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
 return matches ? decodeURIComponent(matches[1]) : undefined;
}

/* запускаем код по готовности веб-страницы */
document.addEventListener("DOMContentLoaded", function(event) {
  /* часть задания про название города */
  welcome_message = document.querySelector(".welcome-message");
  city_input = document.querySelector(".city-input");
  city_name = document.querySelector(".city-name");
  clean_button = document.querySelector(".city-clean");

  city_cookie = getCookie("city");

  if (city_cookie != undefined) {
    city_input.hidden = true;
    city_name.innerText = city_cookie;
    clean_button.onclick = () => {
      clean_button.hidden = true;
      welcome_message.hidden = true;
      setCookie("city", "", {'max-age': -1});
    }
  } else {
    welcome_message.hidden = true
    city_input.oninput = () => {
      setCookie("city", city_input.value, {'max-age': 180});
    };
  }

  /* часть заадния про галочки */
  checkbox_button = document.querySelector(".checkbox-button");
  checkbox_button.hidden = true;

  // кнопка "Разблокировать галочки" удаляет куки
  checkbox_button.onclick = () => {
    for (i = 1;i <= 6; i++) {
      current_checkbox = document.querySelector("#checkbox" + String(i));
      current_checkbox.checked = false;
      current_checkbox.disabled = false;
      setCookie("checkbox" + String(i), "", {'max-age': -1});
      checkbox_button.hidden = true;
    }
  }

  // при загрузке документа галочки принимают значение из cookies и блокируются для редактирования
  for (i = 1;i <= 6; i++) {
    current_checkbox = document.querySelector("#checkbox" + String(i));
    if (getCookie("checkbox" + String(i))) {
      current_checkbox.disabled = true;
      if (getCookie("checkbox" + String(i)) == "true") {
        current_checkbox.checked = true;
      } else {
        current_checkbox.checked = false;
      }
      checkbox_button.hidden = false;
    }
  }

  list = document.querySelectorAll(".checkbox-item");
  list.forEach(
    function(element) {
      element.onclick = () => {
        setCookie(element.id, element.checked, {'max-age': 180});
      }
    }
  );
});
