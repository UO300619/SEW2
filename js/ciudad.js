/* ***************************************/
/*             LaVuelta2026              */
/*               ciudad.js               */
/* ***************************************/
/*    DATOS ESTUDIANTE                   */
/* --------------------------------------*/
/*  Nombre y Apellidos: Enol Ruiz Barcala */
/*  Correo electrónico (uniovi): UO300619@uniovi.es */
/*  Grupo de laboratorio: 5              */
/* ***************************************/

class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;
        this.poblacion = 0;
        this.latitud = 0;
        this.longitud = 0;
        this.altitud = 0;
    }

    rellenarAtributos(poblacion, latitud, longitud, altitud) {
        this.poblacion = poblacion;
        this.latitud = latitud;
        this.longitud = longitud;
        this.altitud = altitud;
    }

    getCiudad() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return "<ul>" +
            "<li>Gentilicio: " + this.gentilicio + "</li>" +
            "<li>Población: " + this.poblacion + " habitantes</li>" +
            "</ul>";
    }

    escribeCoordenadas() {
        const parrafo = document.createElement("p");
        parrafo.textContent = "Coordenadas del centro de " + this.nombre +
            ": latitud " + this.latitud + "º, longitud " + this.longitud +
            "º, altitud " + this.altitud + " m";
        document.querySelector("main section").appendChild(parrafo);
    }
}

const falset = new Ciudad("Falset", "España", "Falsetano/a");
falset.rellenarAtributos(2890, 41.1458, 0.8203, 350);

const seccion = document.createElement("section");
const encabezado = document.createElement("h3");
encabezado.textContent = falset.getCiudad() + " (" + falset.getPais() + ")";
seccion.appendChild(encabezado);
seccion.insertAdjacentHTML("beforeend", falset.getInformacionSecundaria());

document.querySelector("main > h2").insertAdjacentElement("afterend", seccion);

falset.escribeCoordenadas();
