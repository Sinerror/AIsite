console.log('JS файл подключен успешно!');

document.addEventListener('DOMContentLoaded', function() {

    let button = document.getElementById('Ai_button');
    let outputText = document.getElementById('outputText');
    let inputText = document.getElementById('inputText')
    
    button.addEventListener('click', async function() {
        AI_gen(inputText, outputText);
    });

    inputText.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            AI_gen(inputText, outputText);
        }
    });

    let transl = document.getElementById('translate');

    transl.addEventListener('click', async function() {
        fetch('/GTranslate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"message" : outputText.innerHTML})
        })
        .then(response => response.json())
        .then(data => {
            outputText.innerHTML = data.message
        })
        .catch(error => {
            console.error('Ошибка при выполнении запроса:', error);
        });
    });


});

var input = document.getElementById('inputText');
var placeholder = document.querySelector('.placeholder-text');

    input.addEventListener('input', function() {
      if (input.textContent.trim() === '') {
        placeholder.classList.remove('hidden');
      } else {
        placeholder.classList.add('hidden');
      }
    });

function AI_gen(inputText, outputText){
        message = inputText.textContent.trim();

        outputText.textContent = ""

        fetch('/run_AI_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(message)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Ответ от сервера:', data);

            let eventSource = new EventSource('/AIstream?message=' + encodeURIComponent(data.message));

            eventSource.onmessage = function(event) {
                let Dmessage = stringToTuple(event.data);
                console.log(Dmessage)
                if(Dmessage[0]){
                    if(Dmessage[1]){

                        outputText.innerHTML += Dmessage[1];

                        let length = outputText.textContent.length
                        let lineCount = (outputText.innerHTML.match(/<br>/g) || []).length;
                        console.log(lineCount)

                        if (length+lineCount*16 < 200) {
                            outputText.style.fontSize = '36px';
                        } else if (length + lineCount*32 < 500) {
                            outputText.style.fontSize = '28px';
                        } else if (length + lineCount*75 < 2000) {
                            outputText.style.fontSize = '18px';
                        } else{
                            outputText.style.fontSize = '14px';
                        }
                    };
                }else{
                    eventSource.close();
                    console.log("Rensponse tokens: ", Dmessage[3])
                };
            };

            eventSource.onerror = function(error) {
                console.error("EventSource error:", error);
            };
            
        })
        .catch(error => {
            console.error('Ошибка при выполнении запроса:', error);
        });
};

function stringToTuple(str) {
    // Удаляем скобки и лишние пробелы
    str = str.slice(1, -1).trim();

    // Разделяем элементы по запятым
    let elements = str.split(',');

    // Обрезаем лишние пробелы и убираем кавычки
    elements = elements.map(item => item.trim().replace(/^'(.*)'$/, '$1'));

    // Преобразуем элементы, которые выглядят как boolean и числа
    elements = elements.map(item => {
        if (item === 'True') return true;
        if (item === 'False') return false;
        if (!isNaN(item)) return parseFloat(item);
        if (item === "'") return ""
        if (item === " ") return " "
        item = item.replace(/\\n/g, '<br/>');
        return item;
    });

    return elements;
}