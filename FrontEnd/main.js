const form = document.getElementById('formulario');

form.addEventListener('submit', (e) =>{
    e.preventDefault()
    
    const datos = new FormData(form)
    fetch('http://127.0.0.1:9000/transcribe', {
        method : "POST",
        body : datos
    })
    .then(response => {
        if(!response.ok){
            throw new Error("Error en la peticion")
        }
        return response.json()
    })
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        console.error("Hubo un error", error);
    })
})