#Notas a los requisitos

1. Al hacer signup, el usuario no queda logueado al sistema porque creo que es mejor  montar el ciclo de validación de correo. No lo construyo, pero obligo al usuario a loguearse manualmente al sistema como recordatorio/simulación de que queda pendiente la validación del correo.
2. Al comenzar me pareció una buena idea montar el sistema de forma que un usuario pueda tener más de un blog (si yo fuera un usuario me gustaría tener dos distintos). Me ha ido dando problemas pero los he ido solventado. Sin embargo he tenido que tomar ciertas decisiones que no sé si van en contra de los requisitos.
	- **API de posts**: _"Un endpoint para crear posts en el cual el usuario deberá estar autenticado. En este endpoint el post quedará **publicado** automáticamente en el blog del usuario autenticado"_
		- Puesto que un usuario puede tener más de un blog. El blog al que va el post debe informarse como parámetro de entrada. La asignación no puede ser automática, pero si que se valida. Un usuario, incluso el adm, sólo puede asignar post a sus propios blogs, lo que obliga a matizar el endpoint de actualización de post (ver más abajo).
		- Este requisito queda entonces como que la publicación será automática si no se informa date_pub y que el post será no público mientras `date_pub > ahora`.
	- **API de posts**: _"Un endpoint de actualización de un post. Sólo podrá acceder al mismo el dueño del post o un administrador."_ **Le añado lo siguiente por compatibilidad con varios blogs:** _El usuario **dueño podrá modificar todo el post**, incluso asignar el post a cualquiera de sus blogs. El usuario **administrador podrá solamente modificar la fecha de publicación y las categorías**. Así podrá vetar su publicación (mientras pide al usuario que lo corrija), e incluso borrarlo (imaginemos que se ha saltado repetidamente la política del sitio). También podrá cambiar su clasificación por categorías, pero nunca podrá censurarlo o modificar su contenido._
		
3. El usuario administrador, si quiere publicar, tiene que dar de alta su propio blog en el administrador de django. Se ha habilidado una direccion en el sitio web para ello `/new-blog`.

#Uso de la API

##API de usuarios

### POST /api/1.0/users/

**Requisito**: "_Endpoint que permita a cualquier usuario registrarse indicando su nombre, apellidos, nombre de usuario, e-mail y contraseña._"

###Parámetros[^1]

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **username** | body | identificador del usuario (debe ser único) | Si | string 
 **email** | body | correo electrónico del usuario | Si | string 
 **password** | body | Contraseña del usuario.| Si | string 
 **first_name** | body | Nombre del usuario.| No | string
 **last_name** | body | Apellidos del usuario| No | string
 
