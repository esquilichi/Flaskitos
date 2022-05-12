function change_graphic(strin){
    var img = document.getElementById('escaparate-graficos');
    img.src = "/graphics/" + strin
}

function edit_plotly(){
    let porcentaje = document.getElementById('porcentaje').value;
    let n_usuarios = document.getElementById('n_usuarios').value;
    alert(porcentaje)
    alert(n_usuarios);
    window.location = '/dashboard?n=' + n_usuarios + '&critico=' + porcentaje;
}