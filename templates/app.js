
document.addEventListener("DOMContentLoaded", function() {
    fetch("http://127.0.0.1:8080/getPorts", requestOptions)
        .then(response => response.json())
        .then(data => console.log(data));

    });



function getSelectedValue(groupName) {
    var radios = document.querySelectorAll(`input[name="${groupName}"]:checked`);
    
    if (radios.length > 0) {
        return radios[0].value;
    } else {
        return null; // No radio button selected
    }
}

form_tag.addEventListener("submit", function(event){

    event.preventDefault();

    document.getElementById("name").disabled = true;
    document.getElementById("diagnostic").disabled = true;

    var name = document.getElementById("name").toLowerCase().replace(/ /g, '_');
    var diagnostic = document.getElementById("diagnostic").toLowerCase().replace(/ /g, '_');
    var selectedMano = getSelectedValue('mano').toLowerCase();
    var selectedDominancia = getSelectedValue('dominancia').toLowerCase();
    var selectedTipoMedida = getSelectedValue('tipoMedida').toLowerCase();

    console.log(name.value);
    console.log(diagnostic.value);
    console.log('Selected Mano:', selectedMano);
    console.log('Selected Dominancia:', selectedDominancia);
    console.log('Selected Tipo de Medida:', selectedTipoMedida);
    
    if ((name)&&(diagnostic)&&(selectedMano)&&(selectedDominancia)&&(selectedTipoMedida)){
    const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    };

    fetch("http://127.0.0.1:8000/html-response/"+name+"/"+diagnostic+"/"+selectedMano+"/"+selectedDominancia+"/"+selectedTipoMedida, requestOptions)
                .then(response => response.json())
                .then(data => console.log(data));
    }else{
        alert("Porfavor llene todos los campos");
    }
});



function deactivate() {

    alert()
    document.getElementById("cedula").disabled = false;
    document.getElementById("s_social").disabled = false;
    
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        //body: JSON.stringify({ username: username, password: password })
    };

    fetch("http://127.0.0.1:4000/"+ "deactivate", requestOptions)
                .then(response => response.json())
                .then(data => console.log(data));

}