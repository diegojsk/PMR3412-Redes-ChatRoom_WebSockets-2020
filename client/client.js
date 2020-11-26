/*
PMR3412 - Redes Industriais (2020)
Diego Jun Sato Kurashima - 10274231

Segunda Entrega - Exercício 2
Client (client.js)
*/

var chat_window = document.getElementById("chat");
var message_input = document.getElementById("message_input");
var websocket = new WebSocket("ws://localhost:8080");

// Add new messages to message view
websocket.onmessage = function(message){
    chat_window.innerHTML += ('<p>' + message.data + '</p>')
    chat_window.scrollTop = chat_window.scrollHeight;
}

// Send messages on Enter
message_input.onkeyup = function(event){

    if (event.keyCode == 13) {
    websocket.send(message_input.value);
    message_input.value = "";
     }
 }