/* ***************************************/
/*             LaVuelta2026              */
/*             formulario.js             */
/* ***************************************/
/*    DATOS ESTUDIANTE                   */
/* --------------------------------------*/
/*  Nombre y Apellidos: Enol Ruiz Barcala */
/*  Correo electrónico (uniovi): UO300619@uniovi.es */
/*  Grupo de laboratorio: 5              */
/* ***************************************/

class Formulario {
    constructor() {
        this.puntuacion = 0;
        this.dureza = "";
        this.descripcion = "";
        this.usuario = "";
        this.parrafoCalificacion = null;

        const boton = document.querySelector('form button[type="submit"]');
        boton.addEventListener("click", this.analizar.bind(this));
    }

    analizar(event) {
        const form = event.target.closest("form");

        // Si falta algún campo obligatorio, el navegador muestra el aviso y no se corrige
        if (!form.reportValidity()) {
            event.preventDefault();
            return;
        }
        // Evita que se recargue la página al enviar el formulario
        event.preventDefault();

        this.puntuacion = 0;

        const numero = form.querySelector('input[name="numero-etapa"]').value;
        if (Number(numero) === 5) {
            this.puntuacion++;
        }

        const fecha = form.querySelector('input[name="fecha"]').value;
        if (fecha === "2026-08-26") {
            this.puntuacion++;
        }

        const salida = form.querySelector('select[name="salida"]').value;
        if (salida === "Falset") {
            this.puntuacion++;
        }

        const llegada = form.querySelector('select[name="llegada"]').value;
        if (llegada === "Roquetes") {
            this.puntuacion++;
        }

        const tipo = form.querySelector('input[name="tipo"]:checked');
        if (tipo !== null && tipo.value === "mediaMontana") {
            this.puntuacion++;
        }

        const hitosMarcados = [];
        form.querySelectorAll('input[name="hitos"]:checked').forEach(hito => {
            hitosMarcados.push(hito.value);
        });
        const hitosCorrectos = ["puertoMontana", "sprintIntermedio", "sprintBonificado"];
        if (hitosMarcados.length === hitosCorrectos.length &&
            hitosCorrectos.every(hito => hitosMarcados.includes(hito))) {
            this.puntuacion++;
        }

        const longitud = form.querySelector('input[name="longitud"]').value;
        if (longitud !== "" && Number(longitud) === 173.3) {
            this.puntuacion++;
        }

        const desnivel = form.querySelector('input[name="desnivel"]').value;
        if (desnivel !== "" && Number(desnivel) === 1662) {
            this.puntuacion++;
        }

        this.dureza = form.querySelector('input[name="dureza"]').value;
        this.descripcion = form.querySelector('textarea[name="descripcion"]').value;
        this.usuario = form.querySelector('input[name="usuario"]').value;

        this.calificar();
    }

    calificar() {
        const form = document.querySelector("form");

        // Si ya se había mostrado una calificación, se sustituye por la nueva
        if (this.parrafoCalificacion !== null) {
            this.parrafoCalificacion.remove();
        }

        const parrafo = document.createElement("p");
        parrafo.textContent = this.usuario + " has obtenido " + this.puntuacion +
            " puntos, la dureza que has asignado a la etapa es " + this.dureza +
            " y tu descripción " + this.descripcion;

        form.insertAdjacentElement("afterend", parrafo);
        this.parrafoCalificacion = parrafo;
    }
}

const formulario = new Formulario();
