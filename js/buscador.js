/* ***************************************/
/*             LaVuelta2026              */
/*              buscador.js              */
/* ***************************************/
/*    DATOS ESTUDIANTE                   */
/* --------------------------------------*/
/*  Nombre y Apellidos: Enol Ruiz Barcala */
/*  Correo electrónico (uniovi): UO300619@uniovi.es */
/*  Grupo de laboratorio: 5              */
/* ***************************************/

class Buscador {
    constructor() {
        this.lupa = document.querySelector("search > label > img");
        this.campo = document.querySelector("search > input");

        this.lupa.addEventListener("click", this.buscar.bind(this));

        this.campo.addEventListener("keypress", function (evento) {
            if (evento.key === "Enter") {
                this.buscar();
            }
        }.bind(this));
    }

    buscar() {
        this.limpiar_busqueda();

        const resultados = [];
        const texto = this.campo.value;

        if (texto !== "") {
            const regexp = new RegExp(texto, "gi");

            const treeWalker = document.createTreeWalker(document.querySelector("body"), NodeFilter.SHOW_TEXT);

            let node = treeWalker.nextNode();

            while (node) {
                if (regexp.test(node.textContent)) {
                    resultados.push(node);
                }
                node = treeWalker.nextNode();
            }

            resultados.forEach(function (node) {
                var new_text = node.textContent.replaceAll(regexp, '<mark>$&</mark>');
                node.parentElement.innerHTML = new_text;
            });
        }
    }

    limpiar_busqueda() {
        const marcas = document.querySelectorAll("mark");

        marcas.forEach(function (marca) {
            marca.replaceWith(document.createTextNode(marca.textContent));
        });

        document.body.normalize();
    }
}

const buscador = new Buscador();
