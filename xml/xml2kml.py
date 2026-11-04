
import sys
import xml.etree.ElementTree as ET


class Kml(object):


    ESPACIO_KML = "http://www.opengis.net/kml/2.2"
    URL_ICONOS = "http://maps.google.com/mapfiles/kml/paddle/"

    ESTILOS_PUNTO = {
        "rojo": "red-circle.png",
        "verde": "grn-circle.png",
        "azul": "blu-circle.png",
        "amarillo": "ylw-circle.png",
    }

    def __init__(self, nombreDocumento):

        self.raiz = ET.Element('kml', xmlns=self.ESPACIO_KML)
        self.doc = ET.SubElement(self.raiz, 'Document')
        ET.SubElement(self.doc, 'name').text = nombreDocumento
        self._crearEstilosPunto()

    def _crearEstilosPunto(self):

        for nombre, icono in self.ESTILOS_PUNTO.items():
            estilo = ET.SubElement(self.doc, 'Style', id=nombre)
            iconStyle = ET.SubElement(estilo, 'IconStyle')
            ET.SubElement(iconStyle, 'scale').text = '1.1'
            icon = ET.SubElement(iconStyle, 'Icon')
            ET.SubElement(icon, 'href').text = self.URL_ICONOS + icono

    def addPlacemark(self, nombre, descripcion, long, lat, alt, modoAltitud, estilo):

        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        ET.SubElement(pm, 'description').text = descripcion
        ET.SubElement(pm, 'styleUrl').text = '#' + estilo
        punto = ET.SubElement(pm, 'Point')
        ET.SubElement(punto, 'coordinates').text = '{},{},{}'.format(long, lat, alt)
        ET.SubElement(punto, 'altitudeMode').text = modoAltitud

    def addLineString(self, nombre, extrude, tesela, listaCoordenadas, modoAltitud, color, ancho):

        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement(linea, 'color').text = color
        ET.SubElement(linea, 'width').text = ancho
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls, 'extrude').text = extrude
        ET.SubElement(ls, 'tessellate').text = tesela
        ET.SubElement(ls, 'altitudeMode').text = modoAltitud
        ET.SubElement(ls, 'coordinates').text = listaCoordenadas

    def escribir(self, nombreArchivoKML):

        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)


class Etapa(object):


    NAMESPACES = {'u': 'http://www.uniovi.es'}

    def __init__(self, archivoXML):

        self.archivoXML = archivoXML
        try:
            self.arbol = ET.parse(archivoXML)
        except IOError:
            print('No se encuentra el archivo ', archivoXML)
            sys.exit(1)
        except ET.ParseError:
            print('Error procesando el archivo XML = ', archivoXML)
            sys.exit(1)
        self.raiz = self.arbol.getroot()

    def _coordenadas(self, coordenada):

        return (coordenada.get('longitud'),
                coordenada.get('latitud'),
                coordenada.get('altitud'))

    def getNombre(self):

        return self.raiz.find('.//u:nombreE', self.NAMESPACES).text.strip()

    def getNumero(self):

        return self.raiz.find('.//u:numeroE', self.NAMESPACES).text.strip()

    def getOrigen(self):
 
        c = self.raiz.find('./u:origen/u:coordenada', self.NAMESPACES)
        return self._coordenadas(c)

    def getMeta(self):
        
        c = self.raiz.find('./u:meta/u:coordenada', self.NAMESPACES)
        return self._coordenadas(c)

    def getHitos(self):

        hitos = []
        for hito in self.raiz.findall('./u:hitos/u:hito', self.NAMESPACES):
            c = hito.find('./u:coordenada', self.NAMESPACES)
            long, lat, alt = self._coordenadas(c)
            hitos.append({
                'tipo': hito.get('tipo'),
                'categoria': hito.get('categoria'),
                'nombre': hito.get('nombre'),
                'distancia': hito.get('distancia'),
                'long': long, 'lat': lat, 'alt': alt,
            })
        return hitos

    def getPuntos(self, maximo):

        coordenadas = [self._coordenadas(c) for c in
                       self.raiz.findall('./u:puntos/u:punto/u:coordenada', self.NAMESPACES)]
        n = len(coordenadas)
        if n <= maximo:
            return coordenadas
        indices = sorted({round(i * (n - 1) / (maximo - 1)) for i in range(maximo)})#Si hay más del máximo (30), elige maximo puntos repartidos por igual con esta línea





        v 
        return [coordenadas[i] for i in indices]


class Xml2Kml(object):


    MAX_PUNTOS = 30
    MODO_ALTITUD = 'clampToGround'
    COLOR_RUTA = 'ff00a5ff'  

  
    COLOR_HITO = {
        'puertoMontana': 'verde',
        'sprintIntermedio': 'azul',
        'sprintBonificado': 'azul',
        'puntoAnonimo': 'amarillo',
    }

    def __init__(self, archivoXML='etapaEsquema.xml', archivoKML='etapa.kml'):
        self.archivoXML = archivoXML
        self.archivoKML = archivoKML

    def _descripcionHito(self, hito):

        partes = ['Tipo: ' + hito['tipo']]
        if hito['categoria']:
            partes.append('Categoría: ' + hito['categoria'])
        partes.append('Distancia desde la salida: {} km'.format(hito['distancia']))
        partes.append('Altitud: {} m'.format(hito['alt']))
        return '. '.join(partes)

    def generar(self):
  
        etapa = Etapa(self.archivoXML)
        kml = Kml('Etapa {} - {}'.format(etapa.getNumero(), etapa.getNombre()))

        puntos = etapa.getPuntos(self.MAX_PUNTOS)
        origen = etapa.getOrigen()
        meta = etapa.getMeta()
        trazado = [origen] + puntos + [meta]
        coordenadas = '\n'.join('{},{},{}'.format(*p) for p in trazado)
        kml.addLineString('Ruta de la etapa', '0', '1', coordenadas,
                          self.MODO_ALTITUD, self.COLOR_RUTA, '4')


        kml.addPlacemark('Salida: ' + etapa.getNombre().split(' - ')[0],
                         'Punto de salida de la etapa',
                         *origen, self.MODO_ALTITUD, 'rojo')
        kml.addPlacemark('Meta',
                         'Punto de meta de la etapa',
                         *meta, self.MODO_ALTITUD, 'rojo')

        for hito in etapa.getHitos():
            color = self.COLOR_HITO.get(hito['tipo'], 'amarillo')
            kml.addPlacemark(hito['nombre'] or hito['tipo'],
                             self._descripcionHito(hito),
                             hito['long'], hito['lat'], hito['alt'],
                             self.MODO_ALTITUD, color)

        kml.escribir(self.archivoKML)
        print('Creado el archivo:', self.archivoKML)

    @classmethod
    def main(cls):

        argumentos = sys.argv[1:]
        archivoXML = argumentos[0] if len(argumentos) > 0 else 'etapaEsquema.xml'
        archivoKML = argumentos[1] if len(argumentos) > 1 else 'etapa.kml'
        cls(archivoXML, archivoKML).generar()


if __name__ == '__main__':
    Xml2Kml.main()
