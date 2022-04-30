# Introducción

La API de Culqi está construido bajo los estándares de REST. Es decir, nuestra API posee URLs orientada a recursos, y hace uso de los códigos de respuesta HTTP para indicar los posibles errores en el API. Es importante indicar que se encuentra implementada una autenticación HTTP (Bearer Token), solicitada en cada petición. Además, soportamos las solicitudes HTTP de origen cruzado (CORS), permitiendo que tu sitio y Culqi puedan interactuar de manera segura mediante nuestra API desde una aplicación cliente (aunque NUNCA deberías exponer tu Llave Secreta en el código de la aplicación web cliente). Por otro lado, un objeto JSON es retornado en cada una las peticiones hacia el API, incluyendo los errores. Adicionalmente nuestras bibliotecas convierten las respuestas en objetos específicos para cada lenguaje soportado.

Finalmente, para que puedas comenzar a experimentar con nuestra API, todas las cuentas registradas en Culqi poseen llaves para el entorno de pruebas (Regístrate y obtén tus llaves) y el entorno de producción. Usando las llaves de prueba las transacciones nunca pasan por las redes bancarias y no tienen ningún costo. (¡Recuerda usar tarjetas de prueba, no tarjetas reales al probar!).

# Inicialización

Para inicializar el cliente necesitamos la llave pública y la llave privada que nos dan en Culqi al crear nuestro comercio. Suponiendo que hemos colocado nuestras llaves en un archivo `.env`, procedemos a cargarlas de la siguiente manera.


```python
import os
import json
from uuid import uuid4
from copy import deepcopy
from dotenv import load_dotenv

load_dotenv();
```

Asumiendo que nuestras llaves fueron almacenadas en las variables de entorno `API_PUBLIC_KEY` y `API_PRIVATE_KEY`, inicializamos el cliente así


```python
from culqi import Culqi

public_key = os.environ.get("API_PUBLIC_KEY")
private_key = os.environ.get("API_PRIVATE_KEY")

culqi = Culqi(public_key=public_key, private_key=private_key)
```

# Recursos

Para mostrar la forma de acceder a los distintos recuros de Culqi emplearemos datos de pruebas. Estos datos serán los mismos que utilizamos en los tests.


```python
class Data:
    CARD = {
        "successful": {
            "visa": {
                "card_number": "4111111111111111",
                "expiration_month": "09",
                "expiration_year": "2025",
                "cvv": "123",
                "email": "richard@piedpiper.com",
            },
            "master_card": {
                "card_number": "5111111111111118",
                "expiration_month": "06",
                "expiration_year": "2025",
                "cvv": "039",
                "email": "richard@piedpiper.com",
            },
            "american_express": {
                "card_number": "371212121212122",
                "expiration_month": "11",
                "expiration_year": "2025",
                "cvv": "2841",
                "email": "richard@piedpiper.com",
            },
            "diners_club": {
                "card_number": "36001212121210",
                "expiration_month": "04",
                "expiration_year": "2025",
                "cvv": "964",
                "email": "richard@piedpiper.com",
            },
        },
        "stolen_card": {
            "visa": {
                "card_number": "4000020000000000",
                "expiration_month": "10",
                "expiration_year": "2025",
                "cvv": "354",
                "email": "richard@piedpiper.com",
            }
        },
        "lost_card": {
            "visa": {
                "card_number": "4000030000000009",
                "expiration_month": "08",
                "expiration_year": "2025",
                "cvv": "836",
                "email": "richard@piedpiper.com",
            }
        },
        "insufficient_funds": {
            "visa": {
                "card_number": "4000040000000008",
                "expiration_month": "03",
                "expiration_year": "2025",
                "cvv": "295",
                "email": "richard@piedpiper.com",
            }
        },
        "contact_issuer": {
            "master_card": {
                "card_number": "5400000000000005",
                "expiration_month": "01",
                "expiration_year": "2025",
                "cvv": "492",
                "email": "richard@piedpiper.com",
            }
        },
        "incorrect_cvv": {
            "master_card": {
                "card_number": "5400020000000003",
                "expiration_month": "07",
                "expiration_year": "2025",
                "cvv": "203",
                "email": "richard@piedpiper.com",
            }
        },
        "issuer_not_available": {
            "american_express": {
                "card_number": "370001000000000",
                "expiration_month": "04",
                "expiration_year": "2025",
                "cvv": "2511",
                "email": "richard@piedpiper.com",
            }
        },
        "issuer_decline_operation": {
            "american_express": {
                "card_number": "370002000000008",
                "expiration_month": "05",
                "expiration_year": "2025",
                "cvv": "1810",
                "email": "richard@piedpiper.com",
            }
        },
        "invalid_card": {
            "diners_club": {
                "card_number": "36000000000008",
                "expiration_month": "09",
                "expiration_year": "2025",
                "cvv": "683",
                "email": "richard@piedpiper.com",
            }
        },
        "processing_error": {
            "diners_club": {
                "card_number": "36000100000007",
                "expiration_month": "12",
                "expiration_year": "2025",
                "cvv": "820",
                "email": "richard@piedpiper.com",
            }
        },
        "fraudulent": {
            "diners_club": {
                "card_number": "36000200000006",
                "expiration_month": "01",
                "expiration_year": "2025",
                "cvv": "230",
                "email": "richard@piedpiper.com",
            }
        },
    }

    CHARGE = {
        "amount": 1000,
        "capture": False,
        "currency_code": "PEN",
        "description": "Venta de prueba",
        "email": "richard@piedpiper.com",
        "installments": 0,
        "source_id": None,
    }

    REFUND = {
        "amount": 100,
        "reason": "solicitud_comprador",
        "charge_id": None,
    }

    CUSTOMER = {
        "address": "Avenida Lima 123213",
        "address_city": "LIMA",
        "country_code": "PE",
        "email": None,
        "first_name": "Richard",
        "last_name": "Piedpiper",
        "phone_number": "+51998989789",
    }

    PLAN = {
        "amount": 1000,
        "currency_code": "PEN",
        "interval": "dias",
        "interval_count": 2,
        "limit": 10,
        "name": None,
        "trial_days": 30,
    }

    ORDER = {
        "amount": 1000,
        "currency_code": "PEN",
        "description": "Venta de prueba",
        "order_number": None,
        "client_details": {
            "first_name": "Richard",
            "last_name": "Piedpiper",
            "email": "richard@piedpiper.com",
            "phone_number": "+51998989789",
        },
        "expiration_date": 1893474000,
        "confirm": False,
    }
```

Una función que vamos a emplear es `display` para mostrar de manera legible las respuestas entregadas por Culqi en cada una de nuestras operaciones,


```python
def display(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))
```

## Tokens

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/tokens`](https://apidocs.culqi.com/#/tokens)


```python
def get_token_data(code, provider):
    return deepcopy(Data.CARD[code][provider])
```

### Listar


```python
token_list = culqi.token.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    }
)

display(token_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/tokens?limit=1&before=tkn_test_CcP3ZegM0zlVNuQv",
                "next": "https://api.culqi.com/v2/tokens?limit=1&after=tkn_test_CcP3ZegM0zlVNuQv",
                "cursors": {
                    "before": "tkn_test_CcP3ZegM0zlVNuQv",
                    "after": "tkn_test_CcP3ZegM0zlVNuQv"
                },
                "remaining_items": 0
            },
            "items": [
                {
                    "object": "token",
                    "id": "tkn_test_CcP3ZegM0zlVNuQv",
                    "type": "card",
                    "creation_date": 1615131583000,
                    "email": "richard0b7f@piedpiper.com",
                    "card_number": "360001****0007",
                    "last_four": "0007",
                    "active": true,
                    "iin": {
                        "object": "iin",
                        "bin": "360001",
                        "card_brand": "Diners",
                        "card_type": "credito",
                        "card_category": null,
                        "issuer": {
                            "name": "",
                            "country": "PERU",
                            "country_code": "PE",
                            "website": null,
                            "phone_number": null
                        },
                        "installments_allowed": []
                    },
                    "client": {
                        "ip": "191.98.182.73",
                        "ip_country": "Peru",
                        "ip_country_code": "PE",
                        "browser": "UNKNOWN",
                        "device_fingerprint": null,
                        "device_type": "Escritorio"
                    },
                    "metadata": {}
                }
            ]
        }
    }


### Crear


```python
token_data = get_token_data("successful", "visa")
token = culqi.token.create(data=token_data)

display(token)
```

    {
        "status": 201,
        "data": {
            "object": "token",
            "id": "tkn_test_qW2ETydmZ8CmKZQE",
            "type": "card",
            "creation_date": 1615131587000,
            "email": "richard@piedpiper.com",
            "card_number": "411111******1111",
            "last_four": "1111",
            "active": true,
            "iin": {
                "object": "iin",
                "bin": "411111",
                "card_brand": "Visa",
                "card_type": "credito",
                "card_category": "Clásica",
                "issuer": {
                    "name": "BBVA",
                    "country": "PERU",
                    "country_code": "PE",
                    "website": null,
                    "phone_number": null
                },
                "installments_allowed": [
                    2,
                    4,
                    6,
                    8,
                    10,
                    12,
                    3,
                    5,
                    7,
                    9,
                    24,
                    48
                ]
            },
            "client": {
                "ip": "191.98.182.73",
                "ip_country": "Peru",
                "ip_country_code": "PE",
                "browser": "UNKNOWN",
                "device_fingerprint": null,
                "device_type": "Escritorio"
            },
            "metadata": {}
        }
    }


### Leer


```python
token_id = token["data"]["id"]
token = culqi.token.read(id_=token_id)

display(token)
```

    {
        "status": 200,
        "data": {
            "object": "token",
            "id": "tkn_test_qW2ETydmZ8CmKZQE",
            "type": "card",
            "creation_date": 1615131587000,
            "email": "richard@piedpiper.com",
            "card_number": "411111******1111",
            "last_four": "1111",
            "active": true,
            "iin": {
                "object": "iin",
                "bin": "411111",
                "card_brand": "Visa",
                "card_type": "credito",
                "card_category": "Clásica",
                "issuer": {
                    "name": "BBVA",
                    "country": "PERU",
                    "country_code": "PE",
                    "website": null,
                    "phone_number": null
                },
                "installments_allowed": [
                    2,
                    4,
                    6,
                    8,
                    10,
                    12,
                    3,
                    5,
                    7,
                    9,
                    24,
                    48
                ]
            },
            "client": {
                "ip": "191.98.182.73",
                "ip_country": "Peru",
                "ip_country_code": "PE",
                "browser": "UNKNOWN",
                "device_fingerprint": null,
                "device_type": "Escritorio"
            },
            "metadata": {}
        }
    }


### Actualizar


```python
token_id = token["data"]["id"]
token_metadata = {
    "metadata": {
        "orderId": "1234567890"
    }
}
token = culqi.token.update(id_=token_id, data=token_metadata)

display(token)
```

    {
        "status": 200,
        "data": {
            "object": "token",
            "id": "tkn_test_qW2ETydmZ8CmKZQE",
            "type": "card",
            "creation_date": 1615131587000,
            "email": "richard@piedpiper.com",
            "card_number": "411111******1111",
            "last_four": "1111",
            "active": true,
            "iin": {
                "object": "iin",
                "bin": "411111",
                "card_brand": "Visa",
                "card_type": "credito",
                "card_category": "Clásica",
                "issuer": {
                    "name": "BBVA",
                    "country": "PERU",
                    "country_code": "PE",
                    "website": null,
                    "phone_number": null
                },
                "installments_allowed": [
                    2,
                    4,
                    6,
                    8,
                    10,
                    12,
                    3,
                    5,
                    7,
                    9,
                    24,
                    48
                ]
            },
            "client": {
                "ip": "191.98.182.73",
                "ip_country": "Peru",
                "ip_country_code": "PE",
                "browser": "UNKNOWN",
                "device_fingerprint": null,
                "device_type": "Escritorio"
            },
            "metadata": {
                "orderId": "1234567890"
            }
        }
    }


## Cargos

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/cargos`](https://apidocs.culqi.com/#/cargos)


```python
def get_charge_data(code, provider):
    token_data = deepcopy(Data.CARD[code][provider])
    token = culqi.token.create(data=token_data)

    charge_data = deepcopy(Data.CHARGE)
    charge_data["source_id"] = token["data"]["id"]

    return charge_data
```

### Listar


```python
charge_list = culqi.charge.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(charge_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/charges?limit=1&before=chr_test_XC0vjjYHs9PKwqKj",
                "next": "https://api.culqi.com/v2/charges?limit=1&after=chr_test_XC0vjjYHs9PKwqKj",
                "cursors": {
                    "before": "chr_test_XC0vjjYHs9PKwqKj",
                    "after": "chr_test_XC0vjjYHs9PKwqKj"
                },
                "remaining_items": 338
            },
            "items": [
                {
                    "duplicated": null,
                    "object": "charge",
                    "id": "chr_test_XC0vjjYHs9PKwqKj",
                    "creation_date": 1615131590000,
                    "amount": 100,
                    "amount_refunded": 0,
                    "current_amount": 100,
                    "installments": 0,
                    "installments_amount": null,
                    "currency_code": "PEN",
                    "email": null,
                    "description": "Validacion de tarjeta",
                    "source": {
                        "object": "token",
                        "id": "tkn_test_8SSSqy9swCHbfZ1F",
                        "type": "card",
                        "creation_date": 1615131588000,
                        "email": "richardbfc3@piedpiper.com",
                        "card_number": "400002******0000",
                        "last_four": "0000",
                        "active": true,
                        "iin": {
                            "object": "iin",
                            "bin": "400002",
                            "card_brand": "Visa",
                            "card_type": "credito",
                            "card_category": null,
                            "issuer": {
                                "name": "RIVER VALLEY C.U.",
                                "country": "PERU",
                                "country_code": null,
                                "website": null,
                                "phone_number": null
                            },
                            "installments_allowed": null
                        },
                        "client": {
                            "ip": "191.98.182.73",
                            "ip_country": null,
                            "ip_country_code": "PE",
                            "browser": null,
                            "device_fingerprint": null,
                            "device_type": null
                        },
                        "metadata": {}
                    },
                    "outcome": {
                        "type": "card_error",
                        "code": "card_declined",
                        "decline_code": "stolen_card",
                        "merchant_message": "Tarjeta robada. La tarjeta fue bloqueada y reportada al banco emisor como una tarjeta robada.",
                        "user_message": "Su tarjeta está vencida. Verifica la fecha de vencimiento de tu tarjeta e ingrésalos correctamente. Si es denegada nuevamente, contáctate con el banco emisor de tu tarjeta."
                    },
                    "fraud_score": null,
                    "antifraud_details": {
                        "first_name": "Richard",
                        "last_name": "Piedpiper",
                        "address": "Avenida Lima 123213",
                        "address_city": "LIMA",
                        "country_code": "PE",
                        "phone": "51998989789",
                        "object": "client"
                    },
                    "dispute": false,
                    "capture": null,
                    "reference_code": "LxqYIoLTFG",
                    "authorization_code": "zdXUZU",
                    "metadata": {},
                    "total_fee": null,
                    "fee_details": {
                        "fixed_fee": null,
                        "variable_fee": null
                    },
                    "total_fee_taxes": null,
                    "transfer_amount": null,
                    "paid": false,
                    "statement_descriptor": null,
                    "transfer_id": null,
                    "operations": [],
                    "capture_date": null
                }
            ]
        }
    }


### Crear


```python
charge_data = get_charge_data("successful", "visa")
charge = culqi.charge.create(data=charge_data)

display(charge)
```

    {
        "status": 201,
        "data": {
            "duplicated": false,
            "object": "charge",
            "id": "chr_test_M4efNkiZX9jszJQA",
            "creation_date": 1615131596000,
            "amount": 1000,
            "amount_refunded": 0,
            "current_amount": 1000,
            "installments": 1,
            "installments_amount": 1000,
            "currency_code": "PEN",
            "email": "richard@piedpiper.com",
            "description": "Venta de prueba",
            "source": {
                "object": "token",
                "id": "tkn_test_by2icDaZJGAAYY00",
                "type": "card",
                "creation_date": 1615131594000,
                "email": "richard@piedpiper.com",
                "card_number": "411111******1111",
                "last_four": "1111",
                "active": true,
                "iin": {
                    "object": "iin",
                    "bin": "411111",
                    "card_brand": "Visa",
                    "card_type": "credito",
                    "card_category": "Clásica",
                    "issuer": {
                        "name": "BBVA",
                        "country": "PERU",
                        "country_code": "PE",
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": [
                        2,
                        4,
                        6,
                        8,
                        10,
                        12,
                        3,
                        5,
                        7,
                        9,
                        24,
                        48
                    ]
                },
                "client": {
                    "ip": "191.98.182.73",
                    "ip_country": "Peru",
                    "ip_country_code": "PE",
                    "browser": "UNKNOWN",
                    "device_fingerprint": null,
                    "device_type": "Escritorio"
                },
                "metadata": {}
            },
            "outcome": {
                "type": "venta_exitosa",
                "code": "AUT0000",
                "merchant_message": "La operación de venta ha sido autorizada exitosamente",
                "user_message": "Su compra ha sido exitosa."
            },
            "fraud_score": 56.0,
            "dispute": false,
            "capture": false,
            "reference_code": "bYYXVQ7bfh",
            "authorization_code": "qnXJW5",
            "metadata": {},
            "total_fee": 47,
            "fee_details": {
                "fixed_fee": {},
                "variable_fee": {
                    "currency_code": "PEN",
                    "commision": 0.0399,
                    "total": 40
                }
            },
            "total_fee_taxes": 7,
            "transfer_amount": 953,
            "paid": false,
            "statement_descriptor": "CULQI*",
            "transfer_id": null,
            "capture_date": null
        }
    }


### Capturar


```python
charge_id = charge["data"]["id"]
captured_charge = culqi.charge.capture(id_=charge_id)

display(captured_charge)
```

    {
        "status": 201,
        "data": {
            "duplicated": false,
            "object": "charge",
            "id": "chr_test_M4efNkiZX9jszJQA",
            "creation_date": 1615131596000,
            "amount": 1000,
            "amount_refunded": 0,
            "current_amount": 1000,
            "installments": 1,
            "installments_amount": 1000,
            "currency_code": "PEN",
            "email": "richard@piedpiper.com",
            "description": "Venta de prueba",
            "source": {
                "object": "token",
                "id": "tkn_test_by2icDaZJGAAYY00",
                "type": "card",
                "creation_date": 1615131594000,
                "email": "richard@piedpiper.com",
                "card_number": "411111******1111",
                "last_four": "1111",
                "active": true,
                "iin": {
                    "object": "iin",
                    "bin": "411111",
                    "card_brand": "Visa",
                    "card_type": "credito",
                    "card_category": null,
                    "issuer": {
                        "name": "BBVA",
                        "country": "PERU",
                        "country_code": null,
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": null
                },
                "client": {
                    "ip": "191.98.182.73",
                    "ip_country": null,
                    "ip_country_code": null,
                    "browser": null,
                    "device_fingerprint": null,
                    "device_type": null
                },
                "metadata": {}
            },
            "outcome": {
                "type": "venta_exitosa",
                "code": "AUT0000",
                "merchant_message": "La operación de venta ha sido autorizada exitosamente",
                "user_message": "Su compra ha sido exitosa."
            },
            "fraud_score": 56.0,
            "dispute": false,
            "capture": true,
            "reference_code": "bYYXVQ7bfh",
            "authorization_code": "qnXJW5",
            "metadata": {},
            "total_fee": 47,
            "fee_details": {
                "fixed_fee": {},
                "variable_fee": {
                    "currency_code": "PEN",
                    "commision": 0.0399,
                    "total": 40
                }
            },
            "total_fee_taxes": 7,
            "transfer_amount": 953,
            "paid": false,
            "statement_descriptor": "CULQI*",
            "transfer_id": null,
            "operations": [],
            "capture_date": null
        }
    }


### Leer


```python
charge_id = captured_charge["data"]["id"]
charge = culqi.charge.read(id_=charge_id)

display(charge)
```

    {
        "status": 200,
        "data": {
            "duplicated": false,
            "object": "charge",
            "id": "chr_test_M4efNkiZX9jszJQA",
            "creation_date": 1615131596000,
            "amount": 1000,
            "amount_refunded": 0,
            "current_amount": 1000,
            "installments": 1,
            "installments_amount": 1000,
            "currency_code": "PEN",
            "email": "richard@piedpiper.com",
            "description": "Venta de prueba",
            "source": {
                "object": "token",
                "id": "tkn_test_by2icDaZJGAAYY00",
                "type": "card",
                "creation_date": 1615131594000,
                "email": "richard@piedpiper.com",
                "card_number": "411111******1111",
                "last_four": "1111",
                "active": true,
                "iin": {
                    "object": "iin",
                    "bin": "411111",
                    "card_brand": "Visa",
                    "card_type": "credito",
                    "card_category": null,
                    "issuer": {
                        "name": "BBVA",
                        "country": "PERU",
                        "country_code": null,
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": null
                },
                "client": {
                    "ip": "191.98.182.73",
                    "ip_country": null,
                    "ip_country_code": null,
                    "browser": null,
                    "device_fingerprint": null,
                    "device_type": null
                },
                "metadata": {}
            },
            "outcome": {
                "type": "venta_exitosa",
                "code": "AUT0000",
                "merchant_message": "La operación de venta ha sido autorizada exitosamente",
                "user_message": "Su compra ha sido exitosa."
            },
            "fraud_score": 56.0,
            "dispute": false,
            "capture": true,
            "reference_code": "bYYXVQ7bfh",
            "authorization_code": "qnXJW5",
            "metadata": {},
            "total_fee": 47,
            "fee_details": {
                "fixed_fee": {},
                "variable_fee": {
                    "currency_code": "PEN",
                    "commision": 0.0399,
                    "total": 40
                }
            },
            "total_fee_taxes": 7,
            "transfer_amount": 953,
            "paid": false,
            "statement_descriptor": "CULQI*",
            "transfer_id": null,
            "operations": [],
            "capture_date": 1615131600000
        }
    }


### Actualizar


```python
charge_id = charge["data"]["id"]
charge_metadata = {
    "metadata": {
        "orderId": 1234567890
    }
}
charge = culqi.charge.update(id_=charge_id, data=charge_metadata)

display(charge)
```

    {
        "status": 200,
        "data": {
            "duplicated": false,
            "object": "charge",
            "id": "chr_test_M4efNkiZX9jszJQA",
            "creation_date": 1615131596000,
            "amount": 1000,
            "amount_refunded": 0,
            "current_amount": 1000,
            "installments": 1,
            "installments_amount": 1000,
            "currency_code": "PEN",
            "email": "richard@piedpiper.com",
            "description": "Venta de prueba",
            "source": {
                "object": "token",
                "id": "tkn_test_by2icDaZJGAAYY00",
                "type": "card",
                "creation_date": 1615131594000,
                "email": "richard@piedpiper.com",
                "card_number": "411111******1111",
                "last_four": "1111",
                "active": true,
                "iin": {
                    "object": "iin",
                    "bin": "411111",
                    "card_brand": "Visa",
                    "card_type": "credito",
                    "card_category": "Clásica",
                    "issuer": {
                        "name": "BBVA",
                        "country": "PERU",
                        "country_code": "PE",
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": [
                        2,
                        4,
                        6,
                        8,
                        10,
                        12,
                        3,
                        5,
                        7,
                        9,
                        24,
                        48
                    ]
                },
                "client": {
                    "ip": "191.98.182.73",
                    "ip_country": "Peru",
                    "ip_country_code": "PE",
                    "browser": "UNKNOWN",
                    "device_fingerprint": null,
                    "device_type": "Escritorio"
                },
                "metadata": {}
            },
            "outcome": {
                "type": "venta_exitosa",
                "code": "AUT0000",
                "merchant_message": "La operación de venta ha sido autorizada exitosamente",
                "user_message": "Su compra ha sido exitosa."
            },
            "fraud_score": 56.0,
            "dispute": false,
            "capture": true,
            "reference_code": "bYYXVQ7bfh",
            "authorization_code": "qnXJW5",
            "metadata": {
                "orderId": "1234567890"
            },
            "total_fee": 47,
            "fee_details": {
                "fixed_fee": {},
                "variable_fee": {
                    "currency_code": "PEN",
                    "commision": 0.0399,
                    "total": 40
                }
            },
            "total_fee_taxes": 7,
            "transfer_amount": 953,
            "paid": false,
            "statement_descriptor": "CULQI*",
            "transfer_id": null,
            "capture_date": 1615131600000
        }
    }


## Devoluciones

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/devoluciones`](https://apidocs.culqi.com/#/devoluciones)


```python
def get_refund_data(kind, provider):
    token_data = deepcopy(Data.CARD[kind][provider])
    token = culqi.token.create(data=token_data)

    charge_data = deepcopy(Data.CHARGE)
    charge_data["source_id"] = token["data"]["id"]
    charge = culqi.charge.create(data=charge_data)

    refund_data = deepcopy(Data.REFUND)
    refund_data["charge_id"] = charge["data"]["id"]

    return refund_data
```

### Listar


```python
refund_list = culqi.refund.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(refund_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/refunds?limit=1&before=ref_test_NIKAx4LD0hRx8tv3",
                "next": "https://api.culqi.com/v2/refunds?limit=1&after=ref_test_NIKAx4LD0hRx8tv3",
                "cursors": {
                    "before": "ref_test_NIKAx4LD0hRx8tv3",
                    "after": "ref_test_NIKAx4LD0hRx8tv3"
                },
                "remaining_items": null
            },
            "items": [
                {
                    "object": "refund",
                    "id": "ref_test_NIKAx4LD0hRx8tv3",
                    "charge_id": "chr_test_pmmqoIHBNpxTPLQk",
                    "creation_date": 1615131607000,
                    "amount": 100,
                    "reason": "Devolución solicitada por el comercio",
                    "metadata": {}
                }
            ]
        }
    }


### Crear


```python
refund_data = get_refund_data("successful", "visa")
refund = culqi.refund.create(data=refund_data)

display(refund)
```

    {
        "status": 201,
        "data": {
            "object": "refund",
            "id": "ref_test_Bot8onvJGFK2D0zX",
            "charge_id": "chr_test_sT8485Ik7QBskbvl",
            "creation_date": 1615131614000,
            "amount": 100,
            "reason": "Devolución solicitada por el comercio",
            "metadata": {}
        }
    }


### Leer


```python
refund_id = refund["data"]["id"]
refund = culqi.refund.read(id_=refund_id)

display(refund)
```

    {
        "status": 200,
        "data": {
            "object": "refund",
            "id": "ref_test_Bot8onvJGFK2D0zX",
            "charge_id": "chr_test_sT8485Ik7QBskbvl",
            "creation_date": 1615131614000,
            "amount": 100,
            "reason": "Devolución solicitada por el comercio",
            "metadata": {}
        }
    }


### Actualizar


```python
refund_id = refund["data"]["id"]
refund_metadata = {
    "metadata": {
        "orderId": 1234567890
    }
}
refund = culqi.refund.update(id_=refund_id, data=refund_metadata)

display(refund)
```

    {
        "status": 200,
        "data": {
            "object": "refund",
            "id": "ref_test_Bot8onvJGFK2D0zX",
            "charge_id": "chr_test_sT8485Ik7QBskbvl",
            "creation_date": 1615131614000,
            "amount": 100,
            "reason": "Devolución solicitada por el comercio",
            "metadata": {
                "orderId": "1234567890"
            }
        }
    }


## Clientes

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/clientes`](https://apidocs.culqi.com/#/clientes)


```python
def get_customer_data():
    customer_data = deepcopy(Data.CUSTOMER)
    customer_data["email"] = f"richard{uuid4().hex[:4]}@piedpiper.com"

    return customer_data
```

### Listar


```python
customer_list = culqi.customer.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(customer_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/customers?limit=1&before=cus_test_f4l7UKPuYrORPvyP",
                "next": "https://api.culqi.com/v2/customers?limit=1&after=cus_test_f4l7UKPuYrORPvyP",
                "cursors": {
                    "before": "cus_test_f4l7UKPuYrORPvyP",
                    "after": "cus_test_f4l7UKPuYrORPvyP"
                },
                "remaining_items": null
            },
            "items": [
                {
                    "object": "customer",
                    "id": "cus_test_f4l7UKPuYrORPvyP",
                    "creation_date": 1615131609000,
                    "email": "richard50be@piedpiper.com",
                    "antifraud_details": {
                        "first_name": "Richard",
                        "last_name": "Piedpiper",
                        "address": "Avenida Lima 123213",
                        "address_city": "LIMA",
                        "country_code": "PE",
                        "phone": "+51998989789",
                        "object": "client"
                    },
                    "cards": [
                        {
                            "object": "card",
                            "id": "crd_test_yAPm5rwlF3aTGVHa",
                            "active": true,
                            "creation_date": 1615131614000,
                            "customer_id": "cus_test_f4l7UKPuYrORPvyP",
                            "source": {
                                "object": "token",
                                "id": "tkn_test_mw7AQicjlOII6Y5u",
                                "type": "card",
                                "creation_date": 1615131608000,
                                "email": "richard50be@piedpiper.com",
                                "card_number": "511111******1118",
                                "last_four": "1118",
                                "active": true,
                                "iin": {
                                    "object": "iin",
                                    "bin": "511111",
                                    "card_brand": "MasterCard",
                                    "card_type": "debito",
                                    "card_category": "Clásica",
                                    "issuer": {
                                        "name": "INTERBANK",
                                        "country": "PERU",
                                        "country_code": "PE",
                                        "website": null,
                                        "phone_number": null
                                    },
                                    "installments_allowed": [
                                        24,
                                        2,
                                        3,
                                        4,
                                        5,
                                        6,
                                        7,
                                        8,
                                        9,
                                        12,
                                        48
                                    ]
                                },
                                "client": {
                                    "ip": "191.98.182.73",
                                    "ip_country": "Peru",
                                    "ip_country_code": "PE",
                                    "browser": "UNKNOWN",
                                    "device_fingerprint": null,
                                    "device_type": "Escritorio"
                                },
                                "metadata": {}
                            },
                            "metadata": {}
                        }
                    ],
                    "metadata": {}
                }
            ]
        }
    }


### Crear


```python
customer_data = get_customer_data()
customer = culqi.customer.create(data=customer_data)

display(customer)
```

    {
        "status": 201,
        "data": {
            "object": "customer",
            "id": "cus_test_xHxfvWLS9lInzdqE",
            "creation_date": 1615131616908,
            "email": "richard8f52@piedpiper.com",
            "antifraud_details": {
                "first_name": "Richard",
                "last_name": "Piedpiper",
                "address": "Avenida Lima 123213",
                "address_city": "LIMA",
                "country_code": "PE",
                "phone": "+51998989789",
                "object": "client"
            },
            "metadata": {}
        }
    }


### Leer


```python
customer_id = customer["data"]["id"]
customer = culqi.customer.read(id_=customer_id)

display(customer)
```

    {
        "status": 200,
        "data": {
            "object": "customer",
            "id": "cus_test_xHxfvWLS9lInzdqE",
            "creation_date": 1615131616000,
            "email": "richard8f52@piedpiper.com",
            "antifraud_details": {
                "first_name": "Richard",
                "last_name": "Piedpiper",
                "address": "Avenida Lima 123213",
                "address_city": "LIMA",
                "country_code": "PE",
                "phone": "+51998989789",
                "object": "client"
            },
            "cards": [],
            "metadata": {}
        }
    }


### Actualizar


```python
customer_id = customer["data"]["id"]
customer_metadata = {
    "metadata": {
        "orderId": 1234567890
    }
}
customer = culqi.customer.update(
    id_=customer_id, data=customer_metadata
)

display(customer)
```

    {
        "status": 200,
        "data": {
            "object": "customer",
            "id": "cus_test_xHxfvWLS9lInzdqE",
            "creation_date": 1615131616000,
            "email": "richard8f52@piedpiper.com",
            "antifraud_details": {
                "first_name": "Richard",
                "last_name": "Piedpiper",
                "address": "Avenida Lima 123213",
                "address_city": "LIMA",
                "country_code": "PE",
                "phone": "+51998989789",
                "object": "client"
            },
            "metadata": {
                "orderId": "1234567890"
            }
        }
    }


### Eliminar


```python
customer_id = customer["data"]["id"]
deleted_customer = culqi.customer.delete(id_=customer_id)

display(deleted_customer)
```

    {
        "status": 200,
        "data": {
            "id": "cus_test_xHxfvWLS9lInzdqE",
            "deleted": true,
            "merchant_message": "Se eliminó el cliente con ID cus_test_xHxfvWLS9lInzdqE exitosamente."
        }
    }


## Tarjetas

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/tarjetas`](https://apidocs.culqi.com/#/tarjetas)


```python
def get_card_data(code, provider):
    email = f"richard{uuid4().hex[:4]}@piedpiper.com"

    token_data = deepcopy(Data.CARD[code][provider])
    token_data["email"] = email
    token = culqi.token.create(data=token_data)

    customer_data = deepcopy(Data.CUSTOMER)
    customer_data["email"] = email
    customer = culqi.customer.create(data=customer_data)

    return {
        "token_id": token["data"]["id"],
        "customer_id": customer["data"]["id"],
    }
```

### Listar


```python
card_list = culqi.card.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(card_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/cards?limit=1&before=crd_test_yAPm5rwlF3aTGVHa",
                "next": "https://api.culqi.com/v2/cards?limit=1&after=crd_test_yAPm5rwlF3aTGVHa",
                "cursors": {
                    "before": "crd_test_yAPm5rwlF3aTGVHa",
                    "after": "crd_test_yAPm5rwlF3aTGVHa"
                },
                "remaining_items": 83
            },
            "items": [
                {
                    "object": "card",
                    "id": "crd_test_yAPm5rwlF3aTGVHa",
                    "active": true,
                    "creation_date": 1615131614000,
                    "customer_id": "cus_test_f4l7UKPuYrORPvyP",
                    "source": {
                        "object": "token",
                        "id": "tkn_test_mw7AQicjlOII6Y5u",
                        "type": "card",
                        "creation_date": 1615131608000,
                        "email": "richard50be@piedpiper.com",
                        "card_number": "511111******1118",
                        "last_four": "1118",
                        "active": true,
                        "iin": {
                            "object": "iin",
                            "bin": "511111",
                            "card_brand": "MasterCard",
                            "card_type": "debito",
                            "card_category": "Clásica",
                            "issuer": {
                                "name": "INTERBANK",
                                "country": "PERU",
                                "country_code": "PE",
                                "website": null,
                                "phone_number": null
                            },
                            "installments_allowed": [
                                24,
                                2,
                                3,
                                4,
                                5,
                                6,
                                7,
                                8,
                                9,
                                12,
                                48
                            ]
                        },
                        "client": {
                            "ip": "191.98.182.73",
                            "ip_country": "Peru",
                            "ip_country_code": "PE",
                            "browser": "UNKNOWN",
                            "device_fingerprint": null,
                            "device_type": "Escritorio"
                        },
                        "metadata": {}
                    },
                    "metadata": {}
                }
            ]
        }
    }


### Crear


```python
card_data = get_card_data("successful", "visa")
card = culqi.card.create(data=card_data)

display(card)
```

    {
        "status": 201,
        "data": {
            "object": "card",
            "id": "crd_test_3HS06nwaWNH7GJv9",
            "active": true,
            "creation_date": 1615131630282,
            "customer_id": "cus_test_357GTykK2sAJymJB",
            "source": {
                "object": "token",
                "id": "tkn_test_46FxFV1t3eF7anVP",
                "type": "card",
                "creation_date": 1615131624000,
                "email": "richard0640@piedpiper.com",
                "card_number": "411111******1111",
                "last_four": "1111",
                "active": true,
                "iin": {
                    "object": "iin",
                    "bin": "411111",
                    "card_brand": "Visa",
                    "card_type": "credito",
                    "card_category": "Clásica",
                    "issuer": {
                        "name": "BBVA",
                        "country": "PERU",
                        "country_code": "PE",
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": [
                        2,
                        4,
                        6,
                        8,
                        10,
                        12,
                        3,
                        5,
                        7,
                        9,
                        24,
                        48
                    ]
                },
                "client": {
                    "ip": "191.98.182.73",
                    "ip_country": "Peru",
                    "ip_country_code": "PE",
                    "browser": "UNKNOWN",
                    "device_fingerprint": null,
                    "device_type": "Escritorio"
                },
                "metadata": {}
            },
            "metadata": {
                "ZDA": true
            }
        }
    }


### Leer


```python
card_id = card["data"]["id"]
card = culqi.card.read(id_=card_id)

display(card)
```

    {
        "status": 200,
        "data": {
            "object": "card",
            "id": "crd_test_3HS06nwaWNH7GJv9",
            "active": true,
            "creation_date": 1615131630000,
            "customer_id": "cus_test_357GTykK2sAJymJB",
            "source": {
                "object": "token",
                "id": "tkn_test_46FxFV1t3eF7anVP",
                "type": "card",
                "creation_date": 1615131624000,
                "email": "richard0640@piedpiper.com",
                "card_number": "411111******1111",
                "last_four": "1111",
                "active": true,
                "iin": {
                    "object": "iin",
                    "bin": "411111",
                    "card_brand": "Visa",
                    "card_type": "credito",
                    "card_category": "Clásica",
                    "issuer": {
                        "name": "BBVA",
                        "country": "PERU",
                        "country_code": "PE",
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": [
                        2,
                        4,
                        6,
                        8,
                        10,
                        12,
                        3,
                        5,
                        7,
                        9,
                        24,
                        48
                    ]
                },
                "client": {
                    "ip": "191.98.182.73",
                    "ip_country": "Peru",
                    "ip_country_code": "PE",
                    "browser": "UNKNOWN",
                    "device_fingerprint": null,
                    "device_type": "Escritorio"
                },
                "metadata": {}
            },
            "metadata": {}
        }
    }


### Actualizar


```python
card_id = card["data"]["id"]
card_metadata = {
    "metadata": {
        "orderId": 1234567890
    }
}
card = culqi.card.update(
    id_=card_id, data=card_metadata
)

display(card)
```

    {
        "status": 200,
        "data": {
            "object": "card",
            "id": "crd_test_3HS06nwaWNH7GJv9",
            "active": true,
            "creation_date": 1615131630000,
            "customer_id": "cus_test_357GTykK2sAJymJB",
            "source": {
                "object": "token",
                "id": "tkn_test_46FxFV1t3eF7anVP",
                "type": "card",
                "creation_date": 1615131624000,
                "email": "richard0640@piedpiper.com",
                "card_number": "411111******1111",
                "last_four": "1111",
                "active": true,
                "iin": {
                    "object": "iin",
                    "bin": "411111",
                    "card_brand": "Visa",
                    "card_type": "credito",
                    "card_category": "Clásica",
                    "issuer": {
                        "name": "BBVA",
                        "country": "PERU",
                        "country_code": "PE",
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": [
                        2,
                        4,
                        6,
                        8,
                        10,
                        12,
                        3,
                        5,
                        7,
                        9,
                        24,
                        48
                    ]
                },
                "client": {
                    "ip": "191.98.182.73",
                    "ip_country": "Peru",
                    "ip_country_code": "PE",
                    "browser": "UNKNOWN",
                    "device_fingerprint": null,
                    "device_type": "Escritorio"
                },
                "metadata": {}
            },
            "metadata": {
                "orderId": "1234567890"
            }
        }
    }


### Eliminar


```python
card_id = card["data"]["id"]
deleted_card = culqi.card.delete(id_=card_id)

display(deleted_card)
```

    {
        "status": 200,
        "data": {
            "id": "crd_test_3HS06nwaWNH7GJv9",
            "deleted": true,
            "merchant_message": "Se eliminó la tarjeta con ID crd_test_3HS06nwaWNH7GJv9 exitosamente."
        }
    }


## Planes

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/planes`](https://apidocs.culqi.com/#/planes)


```python
def get_plan_data():
    plan_data = deepcopy(Data.PLAN)
    plan_data["name"] = f"plan-{uuid4().hex[:4]}"

    return plan_data
```

### Listar


```python
plan_list = culqi.plan.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(plan_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/plans?limit=1&before=pln_test_QIFyiFRhv4wuhMxZ",
                "next": "https://api.culqi.com/v2/plans?limit=1&after=pln_test_QIFyiFRhv4wuhMxZ",
                "cursors": {
                    "before": "pln_test_QIFyiFRhv4wuhMxZ",
                    "after": "pln_test_QIFyiFRhv4wuhMxZ"
                },
                "remaining_items": 51
            },
            "items": [
                {
                    "object": "plan",
                    "id": "pln_test_QIFyiFRhv4wuhMxZ",
                    "creation_date": 1615129728000,
                    "name": "plan-7274",
                    "amount": 1000,
                    "currency_code": "PEN",
                    "interval_count": 2,
                    "interval": "Días",
                    "limit": 10,
                    "trial_days": 30,
                    "total_subscriptions": 1,
                    "metadata": {}
                }
            ]
        }
    }


### Crear


```python
plan_data = get_plan_data()
plan = culqi.plan.create(data=plan_data)

display(plan)
```

    {
        "status": 201,
        "data": {
            "object": "plan",
            "id": "pln_test_uXQck7r2kIOuPZL8",
            "creation_date": 1615131633000,
            "name": "plan-6b3f",
            "amount": 1000,
            "currency_code": "PEN",
            "interval_count": 2,
            "interval": "Días",
            "limit": 10,
            "trial_days": 30,
            "total_subscriptions": 0,
            "metadata": {}
        }
    }


### Leer


```python
plan_id = plan["data"]["id"]
plan = culqi.plan.read(id_=plan_id)

display(plan)
```

    {
        "status": 200,
        "data": {
            "object": "plan",
            "id": "pln_test_uXQck7r2kIOuPZL8",
            "creation_date": 1615131633000,
            "name": "plan-6b3f",
            "amount": 1000,
            "currency_code": "PEN",
            "interval_count": 2,
            "interval": "Días",
            "limit": 10,
            "trial_days": 30,
            "total_subscriptions": 0,
            "metadata": {}
        }
    }


### Actualizar


```python
plan_id = plan["data"]["id"]
plan_metadata = {
    "metadata": {
        "orderId": 1234567890
    }
}
plan = culqi.plan.update(
    id_=plan_id, data=plan_metadata
)

display(plan)
```

    {
        "status": 200,
        "data": {
            "object": "plan",
            "id": "pln_test_uXQck7r2kIOuPZL8",
            "creation_date": 1615131633000,
            "name": "plan-6b3f",
            "amount": 1000,
            "currency_code": "PEN",
            "interval_count": 2,
            "interval": "Días",
            "limit": 10,
            "trial_days": 30,
            "total_subscriptions": 0,
            "metadata": {
                "orderId": "1234567890"
            }
        }
    }


### Eliminar


```python
plan_id = plan["data"]["id"]
deleted_plan = culqi.plan.delete(id_=plan_id)

display(deleted_plan)
```

    {
        "status": 200,
        "data": {
            "id": "pln_test_uXQck7r2kIOuPZL8",
            "deleted": true,
            "merchant_message": "Se eliminó el plan con ID pln_test_uXQck7r2kIOuPZL8 exitosamente."
        }
    }


## Suscripciones

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/suscripciones`](https://apidocs.culqi.com/#/suscripciones)


```python
def get_subscription_data(code, provider):
    email = f"richard{uuid4().hex[:4]}@piedpiper.com"

    token_data = deepcopy(Data.CARD[code][provider])
    token_data["email"] = email
    token = culqi.token.create(data=token_data)

    customer_data = deepcopy(Data.CUSTOMER)
    customer_data["email"] = email
    customer = culqi.customer.create(data=customer_data)

    card_data = {
        "token_id": token["data"]["id"],
        "customer_id": customer["data"]["id"],
    }
    card = culqi.card.create(data=card_data)

    plan_data = deepcopy(Data.PLAN)
    plan_data["name"] = f"plan-{uuid4().hex[:4]}"
    plan = culqi.plan.create(data=plan_data)

    return {
        "card_id": card["data"]["id"],
        "plan_id": plan["data"]["id"],
    }
```

### Listar


```python
subscription_list = culqi.subscription.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(subscription_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/subscriptions?limit=1&before=sub_test_utqKrxgouUh0IL76",
                "next": "https://api.culqi.com/v2/subscriptions?limit=1&after=sub_test_utqKrxgouUh0IL76",
                "cursors": {
                    "before": "sub_test_utqKrxgouUh0IL76",
                    "after": "sub_test_utqKrxgouUh0IL76"
                },
                "remaining_items": 30
            },
            "items": [
                {
                    "object": "subscription",
                    "id": "sub_test_utqKrxgouUh0IL76",
                    "creation_date": 1615129729000,
                    "status": "Activa",
                    "current_period": 0,
                    "total_period": 10,
                    "current_period_start": 1617685200000,
                    "current_period_end": 1617858000000,
                    "cancel_at_period_end": false,
                    "cancel_at": null,
                    "ended_at": 1619413200000,
                    "next_billing_date": 1617685200000,
                    "trial_start": 1615129729000,
                    "trial_end": 1617721729000,
                    "charges": [],
                    "plan": {
                        "object": "plan",
                        "id": "pln_test_QIFyiFRhv4wuhMxZ",
                        "creation_date": 1615129728000,
                        "name": "plan-7274",
                        "amount": 1000,
                        "currency_code": "PEN",
                        "interval_count": 2,
                        "interval": "Días",
                        "limit": 10,
                        "trial_days": 30,
                        "total_subscriptions": 1,
                        "metadata": {}
                    },
                    "card": {
                        "object": "card",
                        "id": "crd_test_tiP6jsig6txtNlK9",
                        "active": true,
                        "creation_date": 1615129727000,
                        "customer_id": "cus_test_atem3d4M6YsKrrW7",
                        "source": {
                            "object": "token",
                            "id": "tkn_test_FCVsMz64M0YXU5R4",
                            "type": "card",
                            "creation_date": 1615129722000,
                            "email": "richard8b67@piedpiper.com",
                            "card_number": "411111******1111",
                            "last_four": "1111",
                            "active": true,
                            "iin": {
                                "object": "iin",
                                "bin": "411111",
                                "card_brand": "Visa",
                                "card_type": "credito",
                                "card_category": "Clásica",
                                "issuer": {
                                    "name": "BBVA",
                                    "country": "PERU",
                                    "country_code": "PE",
                                    "website": null,
                                    "phone_number": null
                                },
                                "installments_allowed": [
                                    2,
                                    4,
                                    6,
                                    8,
                                    10,
                                    12,
                                    3,
                                    5,
                                    7,
                                    9,
                                    24,
                                    48
                                ]
                            },
                            "client": {
                                "ip": "191.98.182.73",
                                "ip_country": "Peru",
                                "ip_country_code": "PE",
                                "browser": "UNKNOWN",
                                "device_fingerprint": null,
                                "device_type": "Escritorio"
                            },
                            "metadata": {}
                        },
                        "metadata": {}
                    },
                    "metadata": {
                        "order_id": "0001"
                    }
                }
            ]
        }
    }


### Crear


```python
subscription_data = get_subscription_data("successful", "visa")
subscription = culqi.subscription.create(data=subscription_data)

display(subscription)
```

    {
        "status": 201,
        "data": {
            "object": "subscription",
            "id": "sub_test_fcGyWEQTh83qcZyS",
            "creation_date": 1615131643000,
            "status": "Activa",
            "current_period": 0,
            "total_period": 10,
            "current_period_start": 1617685200000,
            "current_period_end": 1617858000000,
            "cancel_at_period_end": false,
            "cancel_at": null,
            "ended_at": 1619413200000,
            "next_billing_date": 1617685200000,
            "trial_start": 1615131643000,
            "trial_end": 1617723643000,
            "charges": [],
            "plan": {
                "object": "plan",
                "id": "pln_test_wPdNqlSBErDW9vbS",
                "creation_date": 1615131642000,
                "name": "plan-035c",
                "amount": 1000,
                "currency_code": "PEN",
                "interval_count": 2,
                "interval": "Días",
                "limit": 10,
                "trial_days": 30,
                "total_subscriptions": 1,
                "metadata": {}
            },
            "card": {
                "object": "card",
                "id": "crd_test_yjsrR87YeJ1lLwk5",
                "active": true,
                "creation_date": 1615131642000,
                "customer_id": "cus_test_dPj41BFoNfZ1Uzjd",
                "source": {
                    "object": "token",
                    "id": "tkn_test_JEGrRw0E6DwWwjwV",
                    "type": "card",
                    "creation_date": 1615131637000,
                    "email": "richard5f26@piedpiper.com",
                    "card_number": "411111******1111",
                    "last_four": "1111",
                    "active": true,
                    "iin": {
                        "object": "iin",
                        "bin": "411111",
                        "card_brand": "Visa",
                        "card_type": "credito",
                        "card_category": "Clásica",
                        "issuer": {
                            "name": "BBVA",
                            "country": "PERU",
                            "country_code": "PE",
                            "website": null,
                            "phone_number": null
                        },
                        "installments_allowed": [
                            2,
                            4,
                            6,
                            8,
                            10,
                            12,
                            3,
                            5,
                            7,
                            9,
                            24,
                            48
                        ]
                    },
                    "client": {
                        "ip": "191.98.182.73",
                        "ip_country": "Peru",
                        "ip_country_code": "PE",
                        "browser": "UNKNOWN",
                        "device_fingerprint": null,
                        "device_type": "Escritorio"
                    },
                    "metadata": {}
                },
                "metadata": {}
            },
            "metadata": {}
        }
    }


### Leer


```python
subscription_id = subscription["data"]["id"]
subscription = culqi.subscription.read(id_=subscription_id)

display(subscription)
```

    {
        "status": 200,
        "data": {
            "object": "subscription",
            "id": "sub_test_fcGyWEQTh83qcZyS",
            "creation_date": 1615131643000,
            "status": "Activa",
            "current_period": 0,
            "total_period": 10,
            "current_period_start": 1617685200000,
            "current_period_end": 1617858000000,
            "cancel_at_period_end": false,
            "cancel_at": null,
            "ended_at": 1619413200000,
            "next_billing_date": 1617685200000,
            "trial_start": 1615131643000,
            "trial_end": 1617723643000,
            "charges": [],
            "plan": {
                "object": "plan",
                "id": "pln_test_wPdNqlSBErDW9vbS",
                "creation_date": 1615131642000,
                "name": "plan-035c",
                "amount": 1000,
                "currency_code": "PEN",
                "interval_count": 2,
                "interval": "Días",
                "limit": 10,
                "trial_days": 30,
                "total_subscriptions": 1,
                "metadata": {}
            },
            "card": {
                "object": "card",
                "id": "crd_test_yjsrR87YeJ1lLwk5",
                "active": true,
                "creation_date": 1615131642000,
                "customer_id": "cus_test_dPj41BFoNfZ1Uzjd",
                "source": {
                    "object": "token",
                    "id": "tkn_test_JEGrRw0E6DwWwjwV",
                    "type": "card",
                    "creation_date": 1615131637000,
                    "email": "richard5f26@piedpiper.com",
                    "card_number": "411111******1111",
                    "last_four": "1111",
                    "active": true,
                    "iin": {
                        "object": "iin",
                        "bin": "411111",
                        "card_brand": "Visa",
                        "card_type": "credito",
                        "card_category": "Clásica",
                        "issuer": {
                            "name": "BBVA",
                            "country": "PERU",
                            "country_code": "PE",
                            "website": null,
                            "phone_number": null
                        },
                        "installments_allowed": [
                            2,
                            4,
                            6,
                            8,
                            10,
                            12,
                            3,
                            5,
                            7,
                            9,
                            24,
                            48
                        ]
                    },
                    "client": {
                        "ip": "191.98.182.73",
                        "ip_country": "Peru",
                        "ip_country_code": "PE",
                        "browser": "UNKNOWN",
                        "device_fingerprint": null,
                        "device_type": "Escritorio"
                    },
                    "metadata": {}
                },
                "metadata": {}
            },
            "metadata": {}
        }
    }


### Actualizar


```python
subscription_id = subscription["data"]["id"]
subscription_metadata = {
    "metadata": {
        "orderId": 1234567890
    }
}
subscription = culqi.subscription.update(
    id_=subscription_id, data=subscription_metadata
)

display(subscription)
```

    {
        "status": 200,
        "data": {
            "object": "subscription",
            "id": "sub_test_fcGyWEQTh83qcZyS",
            "creation_date": 1615131643000,
            "status": "Activa",
            "current_period": 0,
            "total_period": 10,
            "current_period_start": 1617685200000,
            "current_period_end": 1617858000000,
            "cancel_at_period_end": false,
            "cancel_at": null,
            "ended_at": 1619413200000,
            "next_billing_date": 1617685200000,
            "trial_start": 1615131643000,
            "trial_end": 1617723643000,
            "charges": [],
            "plan": {
                "object": "plan",
                "id": "pln_test_wPdNqlSBErDW9vbS",
                "creation_date": 1615131642000,
                "name": "plan-035c",
                "amount": 1000,
                "currency_code": "PEN",
                "interval_count": 2,
                "interval": "Días",
                "limit": 10,
                "trial_days": 30,
                "total_subscriptions": 1,
                "metadata": {}
            },
            "card": {
                "object": "card",
                "id": "crd_test_yjsrR87YeJ1lLwk5",
                "active": true,
                "creation_date": 1615131642000,
                "customer_id": "cus_test_dPj41BFoNfZ1Uzjd",
                "source": {
                    "object": "token",
                    "id": "tkn_test_JEGrRw0E6DwWwjwV",
                    "type": "card",
                    "creation_date": 1615131637000,
                    "email": "richard5f26@piedpiper.com",
                    "card_number": "411111******1111",
                    "last_four": "1111",
                    "active": true,
                    "iin": {
                        "object": "iin",
                        "bin": "411111",
                        "card_brand": "Visa",
                        "card_type": "credito",
                        "card_category": "Clásica",
                        "issuer": {
                            "name": "BBVA",
                            "country": "PERU",
                            "country_code": "PE",
                            "website": null,
                            "phone_number": null
                        },
                        "installments_allowed": [
                            2,
                            4,
                            6,
                            8,
                            10,
                            12,
                            3,
                            5,
                            7,
                            9,
                            24,
                            48
                        ]
                    },
                    "client": {
                        "ip": "191.98.182.73",
                        "ip_country": "Peru",
                        "ip_country_code": "PE",
                        "browser": "UNKNOWN",
                        "device_fingerprint": null,
                        "device_type": "Escritorio"
                    },
                    "metadata": {}
                },
                "metadata": {}
            },
            "metadata": {
                "orderId": "1234567890"
            }
        }
    }


### Eliminar


```python
subscription_id = subscription["data"]["id"]
deleted_subscription = culqi.subscription.delete(id_=subscription_id)

display(deleted_subscription)
```

    {
        "status": 200,
        "data": {
            "id": "sub_test_fcGyWEQTh83qcZyS",
            "deleted": true,
            "merchant_message": "Se eliminó la suscripcion con ID sub_test_fcGyWEQTh83qcZyS exitosamente."
        }
    }


## Órdenes

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/orders`](https://apidocs.culqi.com/#/orders)


```python
def get_order_data():
    order_data = deepcopy(Data.ORDER)
    order_data["order_number"] = f"order-{uuid4().hex[:4]}"

    return order_data
```

### Listar


```python
order_list = culqi.order.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(order_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/orders?limit=1&before=ord_test_mpgi4pJYVcpPljv6",
                "next": "https://api.culqi.com/v2/orders?limit=1&after=ord_test_mpgi4pJYVcpPljv6",
                "cursors": {
                    "before": "ord_test_mpgi4pJYVcpPljv6",
                    "after": "ord_test_mpgi4pJYVcpPljv6"
                },
                "remaining_items": 35
            },
            "items": [
                {
                    "object": "order",
                    "id": "ord_test_mpgi4pJYVcpPljv6",
                    "amount": 1000,
                    "payment_code": null,
                    "currency_code": "PEN",
                    "description": "Venta de prueba",
                    "order_number": "order-a39b",
                    "state": "deleted",
                    "total_fee": null,
                    "net_amount": null,
                    "fee_details": null,
                    "creation_date": 1615131475,
                    "expiration_date": 1893474000,
                    "updated_at": 1615131475,
                    "paid_at": null,
                    "available_on": null,
                    "metadata": {}
                }
            ]
        }
    }


### Crear


```python
order_data = get_order_data()
order = culqi.order.create(data=order_data)

display(order)
```

    {
        "status": 201,
        "data": {
            "object": "order",
            "id": "ord_test_RR6XRh6IXDmFhKlC",
            "amount": 1000,
            "payment_code": null,
            "currency_code": "PEN",
            "description": "Venta de prueba",
            "order_number": "order-c825",
            "state": "created",
            "total_fee": null,
            "net_amount": null,
            "fee_details": null,
            "creation_date": 1615131647,
            "expiration_date": 1893474000,
            "updated_at": 1615131647,
            "paid_at": null,
            "available_on": null,
            "metadata": {}
        }
    }


### Confirmar


```python
order_id = order["data"]["id"]
order = culqi.order.confirm(id_=order_id)

display(order)
```

    {
        "status": 201,
        "data": {
            "object": "order",
            "id": "ord_test_RR6XRh6IXDmFhKlC",
            "amount": 1000,
            "payment_code": "013117141",
            "currency_code": "PEN",
            "description": "Venta de prueba",
            "order_number": "order-c825",
            "state": "pending",
            "total_fee": null,
            "net_amount": null,
            "fee_details": null,
            "creation_date": 1615131647,
            "expiration_date": 1893474000,
            "updated_at": 1615131647,
            "paid_at": null,
            "available_on": null,
            "metadata": {}
        }
    }


### Leer


```python
order_id = order["data"]["id"]
order = culqi.order.read(id_=order_id)

display(order)
```

    {
        "status": 200,
        "data": {
            "object": "order",
            "id": "ord_test_RR6XRh6IXDmFhKlC",
            "amount": 1000,
            "payment_code": "013117141",
            "currency_code": "PEN",
            "description": "Venta de prueba",
            "order_number": "order-c825",
            "state": "pending",
            "total_fee": null,
            "net_amount": null,
            "fee_details": null,
            "creation_date": 1615131647,
            "expiration_date": 1893474000,
            "updated_at": 1615131648,
            "paid_at": null,
            "available_on": null,
            "metadata": {}
        }
    }


### Actualizar


```python
order_id = order["data"]["id"]
order_metadata = {
    "metadata": {
        "orderId": 1234567890
    }
}
order = culqi.order.update(
    id_=order_id, data=order_metadata
)

display(order)
```

    {
        "status": 200,
        "data": {
            "object": "order",
            "id": "ord_test_RR6XRh6IXDmFhKlC",
            "amount": 1000,
            "payment_code": "013117141",
            "currency_code": "PEN",
            "description": "Venta de prueba",
            "order_number": "order-c825",
            "state": "pending",
            "total_fee": null,
            "net_amount": null,
            "fee_details": null,
            "creation_date": 1615131647,
            "expiration_date": 1893474000,
            "updated_at": 1615131648,
            "paid_at": null,
            "available_on": null,
            "metadata": {
                "orderId": "1234567890"
            }
        }
    }


### Eliminar


```python
order_id = order["data"]["id"]
deleted_order = culqi.order.delete(id_=order_id)

display(deleted_order)
```

    {
        "status": 204,
        "data": {}
    }


## Eventos

Consulta la documentación de Culqi en [`https://apidocs.culqi.com/#/eventos`](https://apidocs.culqi.com/#/eventos)

### Listar


```python
event_list = culqi.event.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(event_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": null,
                "next": null,
                "cursors": {
                    "before": null,
                    "after": null
                },
                "remaining_items": 0
            },
            "items": []
        }
    }


### Leer


```python
event_id = "sample_event_id"
event = culqi.event.read(id_=event_id)

display(event)
```

    {
        "status": 400,
        "data": {
            "object": "error",
            "type": "parameter_error",
            "merchant_message": "No existe el evento que intentas consultar: 'sample_event_id' o tiene un formato inválido."
        }
    }


## IINs

Actualmente no hay documentación sobre los IINs en la web oficial de Culqi

### Listar


```python
iin_list = culqi.iin.list(
    data={
        "limit": 1,
    },
    headers={
        "Accept-Encoding": "identity",
    },
)

display(iin_list)
```

    {
        "status": 200,
        "data": {
            "paging": {
                "previous": "https://api.culqi.com/v2/iins?limit=1&before=533958",
                "next": "https://api.culqi.com/v2/iins?limit=1&after=533958",
                "cursors": {
                    "before": "533958",
                    "after": "533958"
                },
                "remaining_items": null
            },
            "items": [
                {
                    "object": "iin",
                    "bin": "533958",
                    "card_brand": "MasterCard",
                    "card_type": "credito",
                    "card_category": null,
                    "issuer": {
                        "name": "FINANCIERA OH, S.A.",
                        "country": "PERU",
                        "country_code": "PE",
                        "website": null,
                        "phone_number": null
                    },
                    "installments_allowed": []
                }
            ]
        }
    }


### Leer


```python
iin_id = "sample_event_id"
iin = culqi.iin.read(id_=iin_id)

display(iin)
```

    {
        "status": 401,
        "data": {
            "object": "error",
            "type": "authentication_error",
            "merchant_message": "Has utilizado la llave equivocada para realizar la operación. Dirígete al Panel de Integracion para usar las llaves correctas."
        }
    }
