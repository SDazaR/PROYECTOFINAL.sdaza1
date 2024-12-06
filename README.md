# PROYECTO FINAL - Heladería

Este repositorio corresponde al segundo proyecto del curso de Backend con Python, impartido por la Universidad de los Andes en el semestre 2024-2.

## Descripción general
Este proyecto implementa una aplicación web de gestión para una heladería utilizando Flask. El sistema permite manejar la creación de heladerías, sus productos y la venta de estos productos.

## Ejecución de la aplicación

Para ejecutar la aplicación se debe ejecutar:

```console
flask run
```
## Funcionalidades principales

1. **Creación de Heladería en la Base de Datos:**
   Al ejecutar `flask run`, se inicializa una heladería en la base de datos con productos e ingredientes predeterminados.

2. **Lista de Heladerías:**
   Accediendo a la URL [http://127.0.0.1:5000/](http://127.0.0.1:5000/), se muestra la lista de heladerías almacenadas en la base de datos (por defecto, habrá una heladería).

3. **Menú de la Heladería:**
   En la página de lista de heladerías, al seleccionar una heladería (por ejemplo, con ID `1`), el sistema redirige a [http://127.0.0.1:5000/parlor/1](http://127.0.0.1:5000/parlor/1), donde se muestra el menú de productos disponibles de esa heladería.

4. **Compra de Productos:**
   Al hacer clic en cualquier producto del menú, se realiza la compra de ese producto. La acción se ejecuta a través de la URL [http://127.0.0.1:5000/parlor/1/makeSale/Copa%20Vainilla](http://127.0.0.1:5000/parlor/1/makeSale/Copa%20Vainilla), y se muestra un mensaje de confirmación en la parte superior de la página.

5. **Mejor Producto:**
   También hay un botón de mejor producto en la parte derecha, el cuál redirige a la URL [http://127.0.0.1:5000/parlor/1/bestProduct](http://127.0.0.1:5000/parlor/1/bestProduct). Aparecerá un mensaje en la parte superior con el nombre del mejor producto de la heladería con el ID especificado (por ejemplo, `1`).

## Test

Para hacer pruebas de los métodos de la heladería se puede ejecutar:

```console
python -m unittest .\tests\test_parlor.py
```

## Documentación de los Endpoints de la API

Los controladores de Producto e Ingrediente fueron añadidos con las funciones para la API. Permanecen las funciones con interfaz. Las respuestas están en formato JSON, incluyendo mensajes de error en caso tal.

1. **Heladería**

   - **Vender un producto**  
     - Endpoint: POST /parlor/<int:id>/makeSale/<int:product_id>  
     - Método: POST  
     - Descripción: Registra la venta de un producto en una heladería con el ID especificado, utilizando el ID del producto.

2. **Productos**

   - **Obtener todos los productos**  
     - Endpoint: GET /product/  
     - Método: GET  
     - Descripción: Devuelve una lista de todos los productos disponibles.

   - **Obtener un producto por ID**  
     - Endpoint: GET /product/<int:product_id>  
     - Método: GET  
     - Descripción: Devuelve los detalles de un producto específico basado en su ID.

   - **Obtener un producto por nombre**  
     - Endpoint: GET /product/name/<string:name>  
     - Método: GET  
     - Descripción: Devuelve el producto que coincida con el nombre proporcionado.

   - **Obtener las calorías de un producto**  
     - Endpoint: GET /product/<int:product_id>/calories  
     - Método: GET  
     - Descripción: Devuelve la cantidad de calorías de un producto basado en su ID.

   - **Obtener la rentabilidad de un producto**  
     - Endpoint: GET /product/<int:product_id>/profitability  
     - Método: GET  
     - Descripción: Devuelve la rentabilidad estimada del producto basado en su ID.

   - **Obtener el costo de un producto**  
     - Endpoint: GET /product/<int:product_id>/cost  
     - Método: GET  
     - Descripción: Devuelve el costo de un producto específico basado en su ID.

3. **Ingredientes**

   - **Obtener todos los ingredientes**  
     - Endpoint: GET /ingredient/  
     - Método: GET  
     - Descripción: Devuelve una lista de todos los ingredientes disponibles.

   - **Obtener un ingrediente por ID**  
     - Endpoint: GET /ingredient/<int:ingredient_id>  
     - Método: GET  
     - Descripción: Devuelve los detalles de un ingrediente específico basado en su ID.

   - **Obtener un ingrediente por nombre**  
     - Endpoint: GET /ingredient/name/<string:name>  
     - Método: GET  
     - Descripción: Devuelve un ingrediente que coincida con el nombre proporcionado.

   - **Verificar si un ingrediente es saludable**  
     - Endpoint: GET /ingredient/<int:ingredient_id>/is_healthy  
     - Método: GET  
     - Descripción: Devuelve un valor booleano indicando si un ingrediente es saludable basado en su ID.

   - **Reabastecer un ingrediente**  
     - Endpoint: PUT /ingredient/<int:ingredient_id>/replenish  
     - Método: PUT  
     - Descripción: Reabastece un ingrediente específico basado en su ID.

   - **Restablecer el inventario de un ingrediente**  
     - Endpoint: PUT /ingredient/<int:ingredient_id>/reset  
     - Método: PUT  
     - Descripción: Restaura el inventario de un ingrediente a su cantidad inicial basada en su ID.

## Despliegue

La aplicación se desplegó a través de Vercel con los siguientes endpoints
