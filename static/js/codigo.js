const fechaInicio = new Date();

datos = JSON.parse(datos.replaceAll("'",'"'));

function ImprimirPregunta(num_pregunta){
    document.querySelector(".contador").innerHTML = num_pregunta + 1 + "/20";
    document.querySelector(".titulo").innerText = datos[num_pregunta]["pregunta"];
    const respuestas = datos[num_pregunta]["respuestas"];
    var textoRespuestas = "";
    for(var i=0;i<respuestas.length;i++){
        textoRespuestas += `<button class="btn boton btn-respuesta">${respuestas[i]["respuesta"]}</button>`
    }
    document.querySelector(".contenedor-respuestas").innerHTML = textoRespuestas;
    const botones = document.querySelectorAll(".btn-respuesta");
    for(var i=0;i<botones.length;i++){
        const boton = botones[i];
        boton.addEventListener("click",(evento)=>{
            var posBoton = -1;
            for(var j=0;j<botones.length;j++){
                if(boton==botones[j]){
                    posBoton = j;
                    break;
                }
            }
            document.querySelector(".respuestas").value += (datos[num_pregunta]["respuestas"][posBoton]["id"]).toString()+"|";
            document.querySelector(".tiempo").value = (Math.abs(fechaInicio - new Date())/1000/60).toString();            
            if(num_pregunta!=19){
                evento.preventDefault();
                ImprimirPregunta(num_pregunta+1);
            }
        });
    }
}

ImprimirPregunta(0);