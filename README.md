![Community project](https://raw.githubusercontent.com/softbutterfly/culqi-api-python/master/resources/softbutterfly-open-source-community-project.png)

![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/culqi-api-python)
![PyPI - Package version](https://img.shields.io/pypi/v/culqi-api-python)
![PyPI - Downloads](https://img.shields.io/pypi/dm/culqi-api-python)
![PyPI - MIT License](https://img.shields.io/pypi/l/culqi-api-python)

[![Build Status](https://www.travis-ci.org/softbutterfly/culqi-api-python.svg?branch=develop)](https://www.travis-ci.org/softbutterfly/culqi-api-python)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8ac045251e9745eea3b89c2896b1f777)](https://www.codacy.com/gh/softbutterfly/culqi-api-python/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=softbutterfly/culqi-api-python&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/8ac045251e9745eea3b89c2896b1f777)](https://www.codacy.com/gh/softbutterfly/culqi-api-python/dashboard?utm_source=github.com&utm_medium=referral&utm_content=softbutterfly/culqi-api-python&utm_campaign=Badge_Coverage)
[![codecov](https://codecov.io/gh/softbutterfly/culqi-api-python/branch/master/graph/badge.svg?token=pbqXUUOu1F)](https://codecov.io/gh/softbutterfly/culqi-api-python)
[![Requirements Status](https://requires.io/github/softbutterfly/culqi-api-python/requirements.svg?branch=master)](https://requires.io/github/softbutterfly/culqi-api-python/requirements/?branch=master)

# Culqi API Python

Biblioteca de CULQI para el lenguaje Python, pagos simples en tu sitio web.

## Requisitos

- Python 3.6, 3.7, 3.8, 3.9
- Credenciales de comercio en [Culqi](https://culqi.com).

## Instalación

```bash
pip install culqi-api-python
```

![Sample](https://raw.githubusercontent.com/softbutterfly/culqi-api-python/master/resources/carbon.png)

Cada metodo retona un diccionario con la estructura

```python
{
      "status": status_code,
      "data": data
}
```

El `status_code` es el estatus HTTP numérico devuelto por la solicitud HTTP que se
realiza al API de Culqi, y `data` contiene el cuerpo de la respuesta obtenida.

## Documentación

- [Referencia de API](https://www.culqi.com/api/)
- [Ejemplos](https://github.com/softbutterfly/culqi-api-python/wiki)
- [Wiki](https://github.com/softbutterfly/culqi-api-python/wiki)

## Changelog

Todos los cambios en las versiones de esta biblioteca están listados en
el [historial de cambios](CHANGELOG.md).

## Desarrollo

Revisa nuestra [guia de contribución](CONTRIBUTING.md)

## Contribuidores

Mira la lista de contribuidores [aquí](https://github.com/softbutterfly/culqi-api-python/graphs/contributors).

## Historia...

La libreria de Culqi para Python inicio su desarrollo en enero del 2017, d ela mano de [@william-muro-culqi](https://github.com/william-muro-culqi) y [@marti1125](https://github.com/marti1125), posteriorme [@brayancruces](https://github.com/brayancruces), [@KhanMaytok](https://github.com/KhanMaytok) y [@oskargicast](https://github.com/oskargicast) complementaron el trabajo incial y mantiuvieron la libreria estable hasta mediados de 2019. En enero del 2020 [@zodiacfireworks](https://github.com/zodiacfireworks) hace una refactorizacion completa de la libreria, estos cambios son aprobados y mejorados por [@joelibaceta](https://github.com/joelibaceta). Con estos cambios se publicaron las versiones 1.0.0, 1.0.1, 1.0.2 y 1.0.3 de la libreria. [@zodiacfireworks](https://github.com/zodiacfireworks) envió más cambios para corregir algunos errores de empaquetamiento, lamentablemente, tras mas de un año de haber sido enviados, no se publicaron a traves del canal oficial, por este motivo es que en [@SoftButterfly](https://github.com/softbutterfly) hemos tomado la iniciativa publicar esta libreria, compatible con la original, con los cambios que no llegaron a publicarse y otras mejoras que se pueden ver en el [historial de cambios](https://github.com/softbutterfly/culqi-api-python/blob/master/CHANGELOG.md). Con el fin de respetar el trabajo de quienes participaron del desarrollo de esta libreria en el repositorio focial de Culqi, el historial original de contribuciones se ha mantenido en este repositorio.
