/* ***************************************/
/*             LaVuelta2026              */
/*              carrusel.js              */
/* ***************************************/
/*    DATOS ESTUDIANTE                   */
/* --------------------------------------*/
/*  Nombre y Apellidos: Enol Ruiz Barcala */
/*  Correo electrónico (uniovi): UO300619@uniovi.es */
/*  Grupo de laboratorio: 5              */
/* ***************************************/

class Carrusel {
    constructor(busqueda) {
        this.busqueda = busqueda;
        this.actual = 0;
        this.maximo = 4;
    }

    getFotografias() {
        const flickrAPI = "https://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?";

        $.getJSON(flickrAPI, {
            tags: this.busqueda,
            tagmode: "any",
            format: "json"
        }).done(function (datos) {
            const fotografias = this.procesarJSONFotografias(datos);
            this.mostrarFotografias(fotografias);
        }.bind(this));
    }

    procesarJSONFotografias(datos) {
        const fotografias = [];

        $.each(datos.items, function (i, item) {
            fotografias.push({
                url: item.media.m.replace("_m.", "_z."),
                // Texto alternativo de la imagen en caso de que no haya titulo
                titulo: item.title.trim() !== "" ? item.title : "Fotografía de LaVuelta2026 obtenida de Flickr"
            });
            if (i === this.maximo) {
                return false;
            }
        }.bind(this));

        return fotografias;
    }

    mostrarFotografias(fotografias) {
        const articulo = $("<article></article>");
        articulo.append($("<h2></h2>").text("Instantáneas de LaVuelta"));
        articulo.append($("<img />").attr({
            src: fotografias[this.actual].url,
            alt: fotografias[this.actual].titulo
        }));
        $("main").append(articulo);

        setInterval(this.cambiarFotografia.bind(this, fotografias), 3000);
    }

    cambiarFotografia(fotografias) {
        this.actual++;
        if (this.actual > this.maximo) {
            this.actual = 0;
        }

        $("article h2 + img").attr({
            src: fotografias[this.actual].url,
            alt: fotografias[this.actual].titulo
        });
    }
}

const carrusel = new Carrusel("lavuelta2026");
carrusel.getFotografias();
