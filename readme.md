#Notas al desarrollo
Al hacer signup, el usuario no queda logueado al sistema porque habría que montar el ciclo de validación de correo. No lo hago, pero obligo al usuario a loguearse al sistema como recordatorio de que queda pendiente la validación

#Uso de la API
## GET /api/1.0/blogs
Devuelve todos los blogs del sistema con todos sus datos. En función de los parámetros se pueden filtrar, elegir los campos a mostrar, paginar y obtener el total de los anuncios de la consulta

###Parámetros[^1]

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **nombre** | query | Nombre del producto. El literal introducido formará parte del nombre del anuncio (en cualquier parte de él)| No | string 
 **precio** | query | Precio del producto. En forma de rango. `precio=10 ➤ Precio exacto` `precio=-10 ➤ Precio ≤ 10` `precio=10- ➤ Precio ≥ 10` `precio=10-50 ➤ 10 ≤ Precio ≤ 50` | No | number 
 **tags** | query | Tags del producto, separadas por espacio `tags=lifestyle motor ➤ tags contiene LIFESTYLE and MOTOR`.| No | number 
 **esVenta** | query | Indica si el producto se vende (true) o se compra (false) `esVenta=true ➤ Anuncios de productos en venta`.| No | boolean 
 **count** | query | Devuelve el total de registros que cumplen las condiciones de búsqueda.| No | boolean 
 **limit** | query | Número máximo de registros devueltos por la consulta.| No | number 
 **skip** | query | Registros omitidos al inicio una vez realizada la consulta | No | number 
 **sort** | query | Ordena los resultados por los campos indicados aquí. Deben separarse por espacios. Si se desea que el orden sea descendente se antepondrá un guión al nombre. `sort=esVenta -precio ➤ Lista ordenada por esVenta asc y precio desc`| No | boolean 
 **fields** | query | Sólo mostrará los campos que se indiquen en este filtro. Separados por un espacio en blanco. `fields=nombre foto ➤ devolverá una lista con _id, nombre y foto`| No | boolean 

