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

        // Click sobre la lupa
        this.lupa.addEventListener("click", this.buscar.bind(this));

        // Tecla intro en el campo de búsqueda
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
            // 1) Expresión regular: todas las apariciones (g), sin distinguir mayúsculas/minúsculas (i)
            const regexp = new RegExp(texto, "gi");

            // 2) Nodos de tipo texto del body
            const treeWalker = document.createTreeWalker(document.querySelector("body"), NodeFilter.SHOW_TEXT);

            // 3) Primer nodo a analizar
            let node = treeWalker.nextNode();

            // 4) Se guardan los nodos cuyo contenido textual contiene el texto buscado
            while (node) {
                if (regexp.test(node.textContent)) {
                    resultados.push(node);
                }
                node = treeWalker.nextNode();
            }

            // 5) Se resalta cada aparición del texto buscado con <mark>
            resultados.forEach(function (node) {
                var new_text = node.textContent.replaceAll(regexp, '<mark>$&</mark>');
                node.parentElement.innerHTML = new_text;
            });
        }
    }

    limpiar_busqueda() {
        const marcas = document.querySelectorAll("mark");

        // Se sustituye cada <mark> por un nodo de texto con su contenido
        marcas.forEach(function (marca) {
            marca.replaceWith(document.createTextNode(marca.textContent));
        });

        document.body.normalize();
    }
}

const buscador = new Buscador();
