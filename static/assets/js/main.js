function change_graphic(strin){
    var img = document.getElementById('escaparate-graficos');
    img.src = "/graphics/" + strin
}

function edit_plotly(){
    let porcentaje = document.getElementById('porcentaje').value;
    let n_usuarios = document.getElementById('n_usuarios').value;
    console.log(porcentaje)
    console.log(n_usuarios)
    url = 'http://localhost:5000/dashboard?n=' + n_usuarios + '&critico=' + porcentaje
    setTimeout(()=>{
        window.location.replace(url)
        console.log(window.location)
    },1000)
    
}