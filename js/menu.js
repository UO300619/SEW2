/* ***************************************/
/*             LaVuelta2026              */
/*               menu.js                 */
/* ***************************************/
/*    DATOS ESTUDIANTE                   */
/* --------------------------------------*/
/*  Nombre y Apellidos: Enol Ruiz Barcala */
/*  Correo electrónico (uniovi): UO300619@uniovi.es */
/*  Grupo de laboratorio: 5              */
/* ***************************************/

class Menu {
    constructor() {
        this.boton = document.querySelector("header > button");
        this.menu = document.querySelector("nav");

        this.boton.addEventListener("click", this.desplegar.bind(this));
    }

    desplegar() {
        const nav = document.querySelector("nav");

        // toggle devuelve true si la clase queda añadida (menú abierto)
        const abierto = nav.classList.toggle("abierto");

        this.boton.textContent = abierto ? "x" : "☰";
        this.boton.setAttribute("aria-expanded", String(abierto));
    }
}

const menu = new Menu();
