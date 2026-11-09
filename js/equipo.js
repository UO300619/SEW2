/* ***************************************/
/*             LaVuelta2026              */
/*               equipo.js               */
/* ***************************************/
/*    DATOS ESTUDIANTE                   */
/* --------------------------------------*/
/*  Nombre y Apellidos: Enol Ruiz Barcala */
/*  Correo electrónico (uniovi): UO300619@uniovi.es */
/*  Grupo de laboratorio: 5              */
/* ***************************************/

class Ciclista {
    constructor(dorsal, nombre, apellidos, fechaNacimiento, nacionalidad, codigoNacionalidad) {
        this.dorsal = dorsal;
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.fechaNacimiento = fechaNacimiento;
        this.nacionalidad = nacionalidad;
        this.codigoNacionalidad = codigoNacionalidad;
    }

    getNombreCompleto() {
        return this.nombre + " – " + this.apellidos;
    }

    getDorsal() {
        return this.dorsal;
    }

    getInformacionAdicional() {
        return this.fechaNacimiento + ", " + this.nacionalidad;
    }
}

class Equipo {
    constructor(nombre, codigoUCI, pais) {
        this.nombre = nombre;
        this.codigoUCI = codigoUCI;
        this.pais = pais;
        this.director = "";
        this.categoria = "";
        this.paginaWeb = "";
        this.alineacion = [];
    }

    rellenarAtributos(director, categoria, paginaWeb) {
        this.director = director;
        this.categoria = categoria;
        this.paginaWeb = paginaWeb;
    }

    datosBasicos() {
        return this.nombre + " (" + this.codigoUCI + ")";
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return "<ul>" +
            "<li>Director: " + this.director + "</li>" +
            "<li>Categoría: " + this.categoria + "</li>" +
            "</ul>";
    }

    getPaginaWeb() {
        const parrafo = document.createElement("p");
        const enlace = document.createElement("a");
        enlace.href = this.paginaWeb;
        enlace.title = "Ficha del " + this.nombre + " en la web oficial de La Vuelta";
        enlace.textContent = this.paginaWeb;
        parrafo.appendChild(document.createTextNode("Ficha del equipo en la web oficial de La Vuelta: "));
        parrafo.appendChild(enlace);
        document.querySelector("main section:first-of-type").appendChild(parrafo);
    }

    async leerEquipo() {
        const respuesta = await fetch("js/recursos/lavuelta.json");
        const datos = await respuesta.json();
        const equipo = datos.equipos.find(e => e.codigo_uci === this.codigoUCI);
        this.alinearCiclistas(equipo.corredores);
    }

    alinearCiclistas(corredores) {
        corredores.forEach(c => {
            this.alineacion.push(new Ciclista(c.dorsal, c.nombre, c.apellidos, c.fecha_nacimiento, c.nacionalidad, c.nacionalidad_codigo));
        });
    }

    mostrarAlineacion() {
        const ordenados = [...this.alineacion].sort((a, b) => a.getDorsal() - b.getDorsal());
        let html = "";
        ordenados.forEach(ciclista => {
            html += "<article>" +
                "<h4>" + ciclista.getNombreCompleto() + "</h4>" +
                "<img src=\"multimedia/ciclista.png\" alt=\"Icono de un ciclista genérico\" />" +
                "<p>" + ciclista.getDorsal() + "</p>" +
                "<p>" + ciclista.getInformacionAdicional() + "</p>" +
                "</article>";
        });
        document.querySelector("main section:last-of-type").insertAdjacentHTML("beforeend", html);
    }
}

const astana = new Equipo("XDS Astana Team", "XAT", "Kazajistán");
astana.rellenarAtributos("Alexandr Shefer", "UCI WorldTeam", "https://www.lavuelta.es/es/equipo/XAT/xds-astana-team");

const seccion = document.createElement("section");
const encabezado = document.createElement("h3");
encabezado.textContent = astana.datosBasicos() + " - " + astana.getPais();
seccion.appendChild(encabezado);
seccion.insertAdjacentHTML("beforeend", astana.getInformacionSecundaria());

document.querySelector("main > h2").insertAdjacentElement("afterend", seccion);

astana.getPaginaWeb();

astana.leerEquipo().then(() => astana.mostrarAlineacion());
