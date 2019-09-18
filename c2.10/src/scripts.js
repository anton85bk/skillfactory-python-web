const url = new URL('https://sf-pyw.mosyag.in/sse/vote/stats')

const header = new Headers({
    'Access-Control-Allow-Credentials': true,
    'Access-Control-Allow-Origin': '*'
})

const cats_progress = document.querySelector('.cats-bar')
console.log(cats_progress)
const parrots_progress = document.querySelector('.parrots-bar')
const dogs_progress = document.querySelector('.dogs-bar')

const ES = new EventSource(url, header)

ES.onopen = event => {
//    console.log(event)
}

ES.onerror = error => {
//    ES.readyState ? progress.textContent = "Some error" : null;
}

ES.onmessage = message => {
    console.log(message.data)
    array = JSON.parse(message.data)
    cats_progress.style.cssText = `width: ${array['cats']}px;`
    cats_progress.textContent = `${array['cats']}`
    parrots_progress.style.cssText = `width: ${array['parrots']}px;`
    parrots_progress.textContent = `${array['parrots']}`
    dogs_progress.style.cssText = `width: ${array['dogs']}px;`
    dogs_progress.textContent = `${array['dogs']}`
}

