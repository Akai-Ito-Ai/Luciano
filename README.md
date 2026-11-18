# El baby shower de Luciano

Invitación para **Luciano Mejía Villamizar**, el **sábado 12 de diciembre de 2026**. Hora y lugar pendientes. Invitación infantil pensada para celular, con sobre de bienvenida, dinosaurios animados, reproductor de música, calendario descargable, confirmaciones y reservas de regalos.

## Ver la invitación

Abre `index.html` en el navegador. También puedes servir esta carpeta:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Abre <http://localhost:4173>. No requiere npm ni compilación. El código de la web está en `index.html`, `styles.css`, `app.js`, `services.js`, `decorations.js`, `welcome.js` y `config.js`.

Sin configuración de Supabase funciona como **vista previa**: la franja y los formularios lo indican. Las confirmaciones y reservas de ejemplo se guardan solo en este navegador. No se comparten entre dispositivos. Los seis regalos son ideas de muestra, no la selección de los papás. La música incluida es una pequeña composición instrumental de muestra creada para esta propuesta.

## Personalizar

Edita `config.js` para poner hora, lugar, dirección, enlace a Maps, fecha límite de confirmación y canción. Pon el archivo de audio en `assets/` y cambia `music.url` y su título. La música empieza únicamente al pulsar play. La fecha se interpreta en Colombia. Mientras falte la hora, el calendario guarda un evento de día completo marcado como pendiente.

La primera versión usa 2026 porque el pedido se hizo en octubre de ese año. Cambia `eventDate` si corresponde otro año.

## Revisión de diseño y UX

El contenido vive en una sola columna centrada de hasta 480 píxeles, sin encabezado ni menú. Un sobre verde oliva cubre inicialmente la pantalla y bloquea el desplazamiento. El sello dorado **VER INVITACIÓN** abre el sobre hacia arriba en un segundo; entonces se habilita el contenido, se devuelve el desplazamiento y comienzan las animaciones visibles. `welcome.js` gestiona esta apertura, el foco de teclado y la preferencia de movimiento reducido.

Caveat da el carácter manuscrito a los títulos, al nombre y a los números; Quicksand se usa en los detalles. Los fondos crema y salvia alternan con divisores SVG irregulares que simulan papel rasgado. Los dinosaurios no tienen marcos, bordes ni sombras: el modo de mezcla y un desvanecimiento suave de sus bordes los integran sobre el papel. Los regalos aparecen en una lista vertical sin tarjetas blancas, y los botones son píldoras verdes.

Los campos de formulario tienen texto de 16 píxeles; el mensaje opcional se despliega cuando se necesita. Los formularios indican cuándo están guardando y conservan los datos si hay un error. La apertura del sobre no reproduce música: el invitado elige cuándo pulsar play.

La sección de regalos tiene cuatro pestañas horizontales: **Ropita, Baño, Alimentación y Accesorios**, con contadores y desplazamiento lateral en celular. Solo el panel de la categoría seleccionada es visible. Las pestañas también funcionan con las flechas del teclado, Inicio y Fin. Al actualizar las reservas se conserva la categoría elegida; si queda vacía, aparece un mensaje para explorar otra pestaña.

En la invitación se muestran hasta tres regalos de la categoría elegida. Cuando esa categoría tiene más, **Ver todos los regalos** abre el catálogo en un panel desde abajo, de hasta 480 píxeles de ancho y 80 % de la altura de la pantalla. El catálogo conserva las mismas pestañas, permite ver todos los artículos de cada categoría y mantiene la selección sincronizada con la invitación. El fondo queda bloqueado y el cierre permanece visible. También se puede cerrar con Escape o tocando el fondo oscuro. Al reservar desde el catálogo, el formulario se abre encima; al cerrarlo se conserva la posición de la lista. Las listas y sus contadores se actualizan juntas al reservar o cancelar.

Para clasificar los regalos reales, usa el campo `category` de Supabase: `Ropita`, `Baño`, `Alimentación` o `Accesorios`. Se reconocen también etiquetas como `Hora del baño`, `A comer` y `Dulces sueños`. Si no se reconoce una etiqueta, se usa el icono del regalo para clasificarlo; los demás se agrupan en Accesorios.
Mientras no se defina una hora, la cuenta regresiva muestra días de calendario en Colombia. No presenta una hora de inicio ficticia. Se verificaron 31 días del 11 de noviembre al 12 de diciembre de 2026 y el conteo con hora definida.

Los controles principales tienen al menos 44 píxeles de alto. Hay un control independiente para pausar las animaciones y se respeta la preferencia de movimiento reducido. La revisión visual y funcional no constituye una auditoría completa de conformidad WCAG.

## Dinosaurios animados

Los cuatro videos entregados por los papás se integraron como decoración: `Dino1` en la portada, `Dino4` en el cierre de la invitación, `Dino2` en asistencia y `Dino3` en regalos. Las copias usadas por la web están en `assets/decoraciones/`: MP4 H.264 de 360 × 640, sin audio y con carga progresiva, más imágenes fijas JPG. En total los videos de la web pesan 2.35 MB, aproximadamente 72 % menos que los originales. Los originales `assets/Dino1.mp4` a `assets/Dino4.mp4` se conservan.

`decorations.js` espera a que se abra el sobre y carga cada video al entrar en pantalla, lo reproduce en bucle y lo pausa al salir o al ocultarse la pestaña. El botón **Pausar animaciones** es independiente de la música y guarda la elección en el navegador. Con movimiento reducido activado, inicialmente se muestran las imágenes fijas sin descargar los MP4. La persona puede activar las animaciones con el botón si lo desea. Si el navegador bloquea la reproducción automática, queda la imagen fija.

Los videos se recortan al centro para acercar los personajes al texto y se difuminan sus bordes; los archivos originales no se modifican. Se revisan la portada, la lista de regalos y los formularios en Brave de escritorio y con simulación de celular. También se comprobaron los cuatro archivos y la lógica de apertura, pausa, visibilidad y movimiento reducido. La reproducción en un teléfono físico queda por comprobar. Para regenerar las copias en macOS está el script `scripts/prepare-decoration-videos.swift`; conserva cualquier copia de salida que ya exista.

## Activar Supabase

1. Crea o elige un proyecto Supabase para la invitación.
2. Ejecuta **una sola vez** `supabase/schema.sql` en SQL Editor. Es una transacción: si algo falla, no deja una instalación parcial. No ejecutar de nuevo sobre una instalación existente.
3. En Table Editor, agrega a `invitation_gifts` los regalos elegidos. Usa `event_id = luciano-2026`. Los campos `image_url` y `product_url` aceptan URLs HTTPS opcionales. `sort_order` controla el orden. `icon` acepta `clothes`, `blanket`, `bath`, `book`, `bottle` o `bear`; `color` acepta `sage`, `peach` o `sand`. La imagen es opcional: hay ilustraciones incluidas.
4. Pon la URL del proyecto y su **publishable key** (o anon key) en `config.js > supabase`. Nunca uses una `service_role` key, clave secreta ni contraseña de Postgres. La clave pública se ve en el navegador por diseño.
5. Ejecuta `supabase/verification.sql` y comprueba que RLS está activo y las dos comprobaciones de lectura devuelven `false`.
6. Prueba dos navegadores con invitados ficticios: reserva el mismo regalo simultáneamente. Solo uno debe conseguirlo. El otro recibe un mensaje y puede escoger otro regalo. Cancela desde Mis reservas y comprueba que vuelve a aparecer. Prueba también confirmar y rechazar asistencia.
7. Publica de nuevo los archivos después de cambiar la configuración. La franja de vista previa desaparece cuando están configuradas la URL y la clave. Una conexión fallida muestra un error y **no cambia silenciosamente a vista previa**.

Con Supabase, la lista vuelve a consultarse cada 20 segundos y al regresar a la pestaña. Una reserva se comprueba en la base de datos al enviar: aunque otra pantalla tenga la lista desactualizada, no puede reservar el mismo regalo. No hace falta una suscripción Realtime.

## Datos y privacidad

La lista preliminar del 12 de noviembre de 2026 contiene 16 regalos reales: 2 de Ropita, 4 de Baño, 3 de Alimentación y 7 de Accesorios. Se importó desde `Lista regalos completada.xlsx`, sin modificar ese archivo. Los paquetes de varias piezas cuentan como un regalo reservable. Los enlaces conservan el producto y sus variantes, retirando parámetros de seguimiento. No se proporcionaron fotos; se usan los iconos incluidos. El esterilizador Momcozy quedó sin descripción, tal como venía en el Excel.

Los datos de importación están en `supabase/regalos-luciano.json` y `supabase/regalos-luciano.csv`. La consulta `supabase/importar-regalos-luciano.sql` puede volver a ejecutarse con esta misma lista sin duplicar artículos: conserva los identificadores, las reservas, el estado de visibilidad y las fotos ya agregadas. El script `scripts/prepare-gift-import.py` permite preparar una nueva importación desde un Excel con las mismas columnas. Revisar los cambios antes de ejecutar el SQL.

Las tablas tienen RLS activado, sin acceso directo para visitantes. Cinco funciones con permisos limitados permiten ver regalos libres, confirmar, reservar, consultar las reservas propias mediante un token aleatorio y cancelarlas. Ninguna respuesta pública contiene nombres ni correos de otros invitados. Los tokens de reserva se conservan en el navegador: una persona puede gestionar las reservas realizadas allí. No borres el almacenamiento de ese navegador si quieres conservar esa posibilidad.

Las confirmaciones se pueden corregir desde el mismo navegador. Un correo ya confirmado desde otro dispositivo no puede sobrescribirse sin su token; los papás pueden corregirlo desde Supabase. Un reintento después de un corte de red es idempotente. El nombre y correo se envían a Supabase únicamente al guardar. No hay analítica. Se importan Caveat y Quicksand desde Google Fonts y se incluyen copias locales de respaldo con sus licencias.

En Supabase, los papás pueden ver y exportar `invitation_rsvps` y `invitation_gift_reservations` desde Table Editor. Para ver qué regalo reservó cada persona:

```sql
select g.name as regalo, r.name as invitado, r.email, r.created_at
from public.invitation_gift_reservations r
join public.invitation_gifts g on g.id = r.gift_id
where r.event_id = 'luciano-2026'
order by r.created_at;
```

## Publicar en otro alojamiento

Es un sitio estático: sube `index.html`, `styles.css`, los cinco archivos JavaScript y la carpeta `assets` a un alojamiento HTTPS. Los originales `assets/Dino1.mp4` a `assets/Dino4.mp4` no son necesarios en el alojamiento: la web usa las copias de `assets/decoraciones/`. No subas `supabase/`, `scripts/`, archivos de pruebas ni este README a la carpeta pública. No se necesita un servidor propio; los datos reales van a Supabase. Para Neon se necesitaría una API de servidor adicional para no exponer la contraseña: esta versión implementa Supabase.

## Estado de validación

Supabase quedó conectado y la lista de 16 regalos se cargó el 12 de noviembre de 2026. Se corrigió la URL en `config.js`: debe apuntar a la raíz del proyecto, sin `/rest/v1/`. La clave pública se conserva. La consulta pública devolvió los 16 registros y se compararon nombres, descripciones, categorías y enlaces con la importación.

Se probaron dos reservas simultáneas del mismo artículo contra Supabase real: solo una tuvo éxito. El regalo dejó de aparecer en la lista pública, se consultó la reserva con su token y después se canceló la reserva de prueba. Al finalizar volvieron a estar disponibles los 16 regalos. También se verificó que la clave pública no permite consultar directamente las tablas de asistentes y reservas. El resultado está en `supabase/verificacion-conexion.json`. No se dejaron reservas de prueba. `scripts/verify-supabase.py` repite la comprobación de lectura; `--test-reservations` agrega la prueba temporal y su cancelación.

La portada se verificó en Brave. Los flujos de confirmación y rechazo de asistencia se probaron previamente con almacenamiento de prueba y solicitudes simuladas; aún falta su prueba final contra la base real. Las reservas de regalos sí se verificaron contra Supabase real, como se describe arriba.

La publicación con Sites no se pudo completar: el servicio devolvió `Sites is not yet enabled for this workspace`. No hay un sitio remoto publicado. El servidor local es temporal y se puede volver a iniciar con el comando anterior.

## Recursos

`assets/dinosaurios.png` es una ilustración original creada con la herramienta integrada ImageGen. Prompt: dos dinosaurios bebés (brontosaurio verde salvia y triceratops terracota), un huevito, eucaliptos, helechos y pequeñas flores, acuarela de cuento infantil sobre papel marfil, sin texto. El prompt completo está en `assets/illustration-prompt.txt`.

Tipografías Caveat y Quicksand de Google Fonts: copias locales y licencias SIL Open Font License incluidas en `assets/`. Los archivos de las fuentes anteriores se conservan, pero la página ya no los usa. Los iconos SVG y la melodía de muestra se crearon para esta invitación.
