
var btnSignin = document.querySelector("#signin");
var btnSignup = document.querySelector("#signup");

var body = document.querySelector("body");


btnSignin.addEventListener("click", function () {
   body.className = "sign-in-js"; 
});

btnSignup.addEventListener("click", function () {
    body.className = "sign-up-js";
})

// Acessa o elemento de vídeo pelo ID
var video = document.getElementById('backgroundVideo');
if (video) {
    video.playbackRate = 0.2; // Ajusta a velocidade de reprodução
    video.play().catch(error => {
        console.error('Erro ao tentar reproduzir o vídeo:', error);
    });
} else {
    console.error('Elemento #backgroundVideo não encontrado.');
}






document.addEventListener("DOMContentLoaded", function () {
    var body = document.querySelector("body");

    btnSignin.addEventListener("click", function () {
       body.className = "sign-in-js"; 
    });

    btnSignup.addEventListener("click", function () {
        body.className = "sign-up-js";
    });

    // Acessa o elemento de vídeo pelo ID
    var video = document.getElementById('backgroundVideo');
    if (video) {
        video.playbackRate = 0.7; // Ajusta a velocidade de reprodução
        video.play().catch(error => {
            console.error('Erro ao tentar reproduzir o vídeo:', error);
        });
    } else {
        console.error('Elemento #backgroundVideo não encontrado.');
    }

    // Código existente para o popup
    const popup = document.getElementById("popup");
    const closePopup = document.getElementById("close-popup");

    // Mostra o popup
    function showPopup() {
        popup.classList.add("active");
        popup.classList.remove("hidden");
    }

    // Fecha o popup
    closePopup.addEventListener("click", () => {
        popup.classList.remove("active");
        popup.classList.add("hidden");
    });

    // Adiciona um listener no formulário de cadastro
    const registerForm = document.querySelector("form[action='/register']");
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Impede o envio padrão para capturar o sucesso

        const formData = new FormData(registerForm);
        const response = await fetch(registerForm.action, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            showPopup(); // Mostra o popup após o sucesso do envio
        }
        //quero fechar o popup depois de 5 segundos
        setTimeout(() => {
            popup.classList.remove("active");
            popup.classList.add("hidden");
        }
        , 2500);
    });
});