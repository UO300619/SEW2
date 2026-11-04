
import sys
import math
import xml.etree.ElementTree as ET


class Svg(object):


    ESPACIO_SVG = "http://www.w3.org/2000/svg"

    def __init__(self, ancho, alto):

        self.raiz = ET.Element('svg',
                               xmlns=self.ESPACIO_SVG,
                               version="2.0",
                               width=str(ancho),
                               height=str(alto),
                               viewBox="0 0 {} {}".format(ancho, alto))

    def addRect(self, x, y, width, height, fill, strokeWidth, stroke):

        ET.SubElement(self.raiz, 'rect',
                      x=str(x), y=str(y), width=str(width), height=str(height),
                      fill=fill, stroke=stroke)
        self.raiz[-1].set('stroke-width', str(strokeWidth))

    def addCircle(self, cx, cy, r, fill, stroke='black'):

        ET.SubElement(self.raiz, 'circle',
                      cx=self._n(cx), cy=self._n(cy), r=str(r),
                      fill=fill, stroke=stroke)

    def addLine(self, x1, y1, x2, y2, stroke, strokeWidth, dash=None):

        linea = ET.SubElement(self.raiz, 'line',
                              x1=self._n(x1), y1=self._n(y1),
                              x2=self._n(x2), y2=self._n(y2),
                              stroke=stroke)
        linea.set('stroke-width', str(strokeWidth))
        if dash:
            linea.set('stroke-dasharray', dash)

    def addPolyline(self, points, stroke, strokeWidth, fill):
 
        pl = ET.SubElement(self.raiz, 'polyline',
                           points=points, stroke=stroke, fill=fill)
        pl.set('stroke-width', str(strokeWidth))
        pl.set('stroke-linejoin', 'round')

    def addText(self, texto, x, y, fontFamily, fontSize, style,
                anchor='start', rotate=None, fill='black'):

        t = ET.SubElement(self.raiz, 'text', x=self._n(x), y=self._n(y), fill=fill)
        t.set('font-family', fontFamily)
        t.set('font-size', str(fontSize))
        t.set('text-anchor', anchor)
        if style and style != 'none':
            t.set('style', style)
        if rotate is not None:
            t.set('transform', 'rotate({} {} {})'.format(rotate, self._n(x), self._n(y)))
        t.text = texto

    def _n(self, valor):

        return '{:.2f}'.format(float(valor)).rstrip('0').rstrip('.')

    def escribir(self, nombreArchivoSVG):

        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG, encoding='utf-8', xml_declaration=True)


class Etapa(object):


    NAMESPACES = {'u': 'http://www.uniovi.es'}
    RADIO_TIERRA_KM = 6371.0

    def __init__(self, archivoXML):

        try:
            self.arbol = ET.parse(archivoXML)
        except IOError:
            print('No se encuentra el archivo ', archivoXML)
            sys.exit(1)
        except ET.ParseError:
            print('Error procesando el archivo XML = ', archivoXML)
            sys.exit(1)
        self.raiz = self.arbol.getroot()

    def getNombre(self):

        return self.raiz.find('./u:nombreE', self.NAMESPACES).text.strip()

    def getNumero(self):

        return self.raiz.find('./u:numeroE', self.NAMESPACES).text.strip()

    def getLongitudKm(self):

        return float(self.raiz.find('./u:longitud', self.NAMESPACES).text)

    def _haversine(self, p1, p2):

        lon1, lat1, lon2, lat2 = map(math.radians, (p1[0], p1[1], p2[0], p2[1]))
        a = (math.sin((lat2 - lat1) / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
        return 2 * self.RADIO_TIERRA_KM * math.asin(math.sqrt(a))

    def getPerfil(self):

        xpaths = ['./u:origen/u:coordenada',
                  './u:puntos/u:punto/u:coordenada',
                  './u:meta/u:coordenada']
        coordenadas = []
        for xp in xpaths:
            for c in self.raiz.findall(xp, self.NAMESPACES):
                coordenadas.append((float(c.get('longitud')),
                                    float(c.get('latitud')),
                                    float(c.get('altitud'))))

        acumulada = [0.0]
        for anterior, actual in zip(coordenadas, coordenadas[1:]):
            acumulada.append(acumulada[-1] + self._haversine(anterior, actual))

        factor = self.getLongitudKm() / acumulada[-1] if acumulada[-1] > 0 else 1.0
        return [(d * factor, c[2]) for d, c in zip(acumulada, coordenadas)]

    def getHitos(self):

        hitos = []
        for hito in self.raiz.findall('./u:hitos/u:hito', self.NAMESPACES):
            hitos.append({'tipo': hito.get('tipo'),
                          'nombre': hito.get('nombre') or hito.get('tipo'),
                          'distancia': float(hito.get('distancia'))})
        return sorted(hitos, key=lambda h: h['distancia'])


class Altimetria(object):


    ANCHO, ALTO = 1100, 700
    MARGEN_IZQ, MARGEN_DER, MARGEN_SUP, MARGEN_INF = 80, 40, 70, 330
    FUENTE = 'Arial, Helvetica, sans-serif'

    COLOR_HITO = {
        'puertoMontana': '#2e9e3e',
        'sprintIntermedio': '#1f6fd1',
        'sprintBonificado': '#1f6fd1',
        'puntoAnonimo': '#e6b800',
    }

    def __init__(self, etapa):
        self.etapa = etapa
        self.perfil = etapa.getPerfil()
        self.hitos = etapa.getHitos()
        self.svg = Svg(self.ANCHO, self.ALTO)

        self.kmTotal = etapa.getLongitudKm()
        self.altMax = math.ceil(max(a for _, a in self.perfil) / 100.0) * 100
        self.altMin = 0
        self.anchoGraf = self.ANCHO - self.MARGEN_IZQ - self.MARGEN_DER
        self.altoGraf = self.ALTO - self.MARGEN_SUP - self.MARGEN_INF

    def _x(self, km):

        return self.MARGEN_IZQ + km / self.kmTotal * self.anchoGraf

    def _y(self, alt):

        base = self.MARGEN_SUP + self.altoGraf
        return base - (alt - self.altMin) / (self.altMax - self.altMin) * self.altoGraf

    def _altitudEn(self, km):

        for (d1, a1), (d2, a2) in zip(self.perfil, self.perfil[1:]):
            if d1 <= km <= d2:
                return a1 if d2 == d1 else a1 + (a2 - a1) * (km - d1) / (d2 - d1)
        return self.perfil[-1][1]

    def _dibujarFondo(self):

        s = self.svg
        s.addRect(0, 0, self.ANCHO, self.ALTO, 'white', 0, 'white')
        s.addText('Altimetría - Etapa {}: {}'.format(self.etapa.getNumero(), self.etapa.getNombre()),
                  self.ANCHO / 2, 32, self.FUENTE, 20, 'font-weight: bold', anchor='middle')

        base = self.MARGEN_SUP + self.altoGraf
        for alt in range(self.altMin, self.altMax + 1, 100):
            y = self._y(alt)
            s.addLine(self.MARGEN_IZQ, y, self.ANCHO - self.MARGEN_DER, y, '#d0d0d0', 1)
            s.addText(str(alt), self.MARGEN_IZQ - 8, y + 4, self.FUENTE, 12, 'none', anchor='end')
        s.addText('Altitud (m)', 22, self.MARGEN_SUP + self.altoGraf / 2,
                  self.FUENTE, 14, 'none', anchor='middle', rotate=-90)

        for km in range(0, int(self.kmTotal) + 1, 20):
            x = self._x(km)
            s.addLine(x, base, x, base + 6, 'black', 1)
            s.addText(str(km), x, base + 20, self.FUENTE, 12, 'none', anchor='middle')
        s.addText('Distancia (km)', self.MARGEN_IZQ + self.anchoGraf / 2, base + 40,
                  self.FUENTE, 14, 'none', anchor='middle')

    def _dibujarPerfil(self):

        base = self.MARGEN_SUP + self.altoGraf
        puntos = ['{:.2f},{:.2f}'.format(self._x(d), self._y(a)) for d, a in self.perfil]
        puntos.append('{:.2f},{:.2f}'.format(self._x(self.perfil[-1][0]), base))
        puntos.append('{:.2f},{:.2f}'.format(self._x(self.perfil[0][0]), base))
        puntos.append(puntos[0])
        self.svg.addPolyline(' '.join(puntos), '#b22222', 2, '#e8c9a0')

    def _dibujarHitos(self):

        s = self.svg
        base = self.MARGEN_SUP + self.altoGraf
        ultimoX = -100
        desplazamiento = 0
        for h in self.hitos:
            color = self.COLOR_HITO.get(h['tipo'], '#e6b800')
            x = self._x(h['distancia'])
            y = self._y(self._altitudEn(h['distancia']))
            s.addLine(x, y, x, base, color, 1.5, dash='5,3')
            s.addCircle(x, y, 5, color)

            desplazamiento = desplazamiento + 16 if abs(x - ultimoX) < 16 else 0
            ultimoX = x
            xt = x + 4 + desplazamiento
            s.addText('{} ({:g} km)'.format(h['nombre'], h['distancia']),
                      xt, base + 58, self.FUENTE, 12, 'none', rotate=90)

    def generar(self, archivoSVG):
 
        self._dibujarFondo()
        self._dibujarPerfil()
        self._dibujarHitos()
        self.svg.escribir(archivoSVG)
        print('Creado el archivo:', archivoSVG)


class Xml2Altimetria(object):


    @classmethod
    def main(cls):

        argumentos = sys.argv[1:]
        archivoXML = argumentos[0] if len(argumentos) > 0 else 'etapaEsquema.xml'
        archivoSVG = argumentos[1] if len(argumentos) > 1 else 'altimetria.svg'
        Altimetria(Etapa(archivoXML)).generar(archivoSVG)


if __name__ == '__main__':
    Xml2Altimetria.main()
