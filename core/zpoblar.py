import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='alice89',
        tipo='Cliente', 
        nombre='Alice', 
        apellido='Johnson', 
        correo=test_user_email if test_user_email else 'alice.johnson@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/alice.jpg')

    crear_usuario(
        username='bob_smith',
        tipo='Cliente', 
        nombre='Bob', 
        apellido='Smith', 
        correo=test_user_email if test_user_email else 'bob.smith@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/bob.jpg')

    crear_usuario(
        username='emma_brown',
        tipo='Cliente', 
        nombre='Emma', 
        apellido='Brown', 
        correo=test_user_email if test_user_email else 'emma.brown@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/emma.jpg')


    crear_usuario(
        username='john_davis',
        tipo='Administrador', 
        nombre='John', 
        apellido='Davis',  
        correo=test_user_email if test_user_email else 'john.davis@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/john.jpg')

    crear_usuario(
        username='sophia_moore',
        tipo='Administrador', 
        nombre='Sophia', 
        apellido='Moore',  
        correo=test_user_email if test_user_email else 'sophia.moore@example.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/sophia.jpg')
    
    crear_usuario(
        username='michael_johnson',
        tipo='Administrador', 
        nombre='Michael', 
        apellido='Johnson', 
        correo=test_user_email if test_user_email else 'michael.johnson@example.com',
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/michael.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Victor',
        apellido='Barrientos',
        correo=test_user_email if test_user_email else 'victorrigocl@gmail.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/victor.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Cyberpunk 2077',
            'descripcion': 'Cyberpunk 2077 es un juego de rol de acción de mundo abierto desarrollado y publicado por CD Projekt Red. El juego se desarrolla en Night City, una megaciudad futurista obsesionada con el poder, el glamour y la modificación corporal. Los jugadores asumen el papel de V, un mercenario que puede ser personalizado en términos de género, apariencia y trasfondo.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000001.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'The Last of Us Part II',
            'descripcion': 'The Last of Us Part II es un juego de acción y aventura desarrollado por Naughty Dog y publicado por Sony Interactive Entertainment. Es la secuela de The Last of Us y sigue la historia de Ellie en un mundo post-apocalíptico lleno de peligros y desafíos.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000002.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Ghost of Tsushima',
            'descripcion': 'Ghost of Tsushima es un juego de acción y aventura desarrollado por Sucker Punch Productions y publicado por Sony Interactive Entertainment. El juego está ambientado en el Japón feudal y sigue la historia de Jin Sakai, un samurái en una misión para proteger Tsushima durante la invasión mongola.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000003.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Marvel\'s Spider-Man: Miles Morales',
            'descripcion': 'Marvel\'s Spider-Man: Miles Morales es un juego de acción y aventura desarrollado por Insomniac Games y publicado por Sony Interactive Entertainment. El juego sigue a Miles Morales, un adolescente que adquiere poderes similares a los de Spider-Man después de ser mordido por una araña genéticamente modificada.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000004.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Death Stranding',
            'descripcion': 'Death Stranding es un juego de acción y aventura desarrollado por Kojima Productions y publicado por Sony Interactive Entertainment. El juego sigue a Sam Bridges en un viaje a través de un paisaje devastado por un evento sobrenatural. Sam debe conectar ciudades y salvar a la humanidad de la extinción.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000005.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Sekiro: Shadows Die Twice',
            'descripcion': 'Sekiro: Shadows Die Twice es un juego de acción y aventura desarrollado por FromSoftware y publicado por Activision. El juego está ambientado en el Japón de finales de 1500 y sigue a un guerrero conocido como "Lobo" en su misión para rescatar a su maestro y vengarse de su némesis.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000006.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Far Cry 6',
            'descripcion': 'Far Cry 6 es un juego de acción y aventura desarrollado por Ubisoft Toronto y publicado por Ubisoft. El juego está ambientado en Yara, una isla ficticia del Caribe gobernada por un dictador. Los jugadores asumen el papel de un guerrillero luchando para liberar Yara del régimen opresivo.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000007.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil Village',
            'descripcion': 'Resident Evil Village es un juego de terror y supervivencia desarrollado y publicado por Capcom. Es la octava entrega principal de la serie Resident Evil y sigue la historia de Ethan Winters en una aldea europea llena de criaturas terroríficas y personajes misteriosos.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000008.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'The Legend of Zelda: Breath of the Wild',
            'descripcion': 'The Legend of Zelda: Breath of the Wild es un videojuego de acción-aventura desarrollado y publicado por Nintendo para las consolas Nintendo Switch y Wii U. El juego es la decimonovena entrega de la serie The Legend of Zelda y fue lanzado mundialmente en marzo de 2017. Breath of the Wild es un juego de mundo abierto que permite a los jugadores explorar libremente el reino de Hyrule.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000009.jpg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Uncharted Collection',
            'descripcion': 'Uncharted Collection es un videojuego de acción-aventura desarrollado por Naughty Dog y publicado por Sony Computer Entertainment para PlayStation 4. El juego fue lanzado en mayo de 2016 y es la cuarta entrega principal de la serie Uncharted. La historia sigue a Nathan Drake, un cazador de tesoros retirado que se ve obligado a volver a su antigua vida cuando su hermano Sam reaparece.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000010.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Assassin\'s Creed Odyssey',
            'descripcion': 'Assassin\'s Creed Odyssey es un videojuego de acción-aventura desarrollado por Ubisoft Quebec y publicado por Ubisoft. Es la undécima entrega principal de la serie Assassin\'s Creed y se desarrolla en la Antigua Grecia durante la Guerra del Peloponeso.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000011.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Horizon Zero Dawn',
            'descripcion': 'Horizon Zero Dawn es un juego de acción y aventura desarrollado por Guerrilla Games y publicado por Sony Interactive Entertainment. El juego está ambientado en un mundo post-apocalíptico donde las máquinas dominan la Tierra y los humanos han vuelto a un estilo de vida tribal. Los jugadores asumen el papel de Aloy, una joven cazadora en una misión para descubrir su pasado y salvar su mundo.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000012.jpg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Command and Conquer Remastered',
            'descripcion': 'Command and Conquer Remastered es un juego de estrategia por turnos en el que los jugadores intentan construir un imperio que resista el paso del tiempo. Explora un nuevo mundo, investiga tecnologías, conquista a tus enemigos y enfréntate a los líderes más famosos de la historia mientras intentas crear la civilización más poderosa que haya existido jamás.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000013.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Company of Heroes 2',
            'descripcion': 'Company of Heroes 2 es un juego de estrategia de guerra histórica desarrollado por Creative Assembly y publicado por Sega. Está ambientado en China durante los tumultuosos años de los Tres Reinos y permite a los jugadores asumir el papel de uno de los líderes de la época mientras luchan por unificar China bajo su dominio.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000014.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Stellaris',
            'descripcion': 'Stellaris es un juego de estrategia 4X desarrollado por Paradox Development Studio y publicado por Paradox Interactive. Los jugadores controlan naves y planetas en su búsqueda por descubrir, colonizar y conquistar nuevos mundos en un vasto universo lleno de civilizaciones alienígenas y misterios cósmicos.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000015.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'FF XV',
            'descripcion': 'FF XV es un juego de estrategia en tiempo real desarrollado por Relic Entertainment y publicado por Xbox Game Studios. El juego continúa la legendaria serie Age of Empires, llevando a los jugadores a través de diferentes épocas mientras construyen imperios, gestionan recursos y luchan en batallas épicas.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000016.jpg'
        },
        # Categoría "Simulación" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'The Sims 4',
            'descripcion': 'The Sims 4 es un juego de simulación de vida desarrollado por Maxis y publicado por Electronic Arts. Los jugadores crean y controlan Sims en diferentes actividades y relaciones en un mundo virtual. Personaliza el aspecto y la personalidad de tus Sims, construye casas y explora sus historias únicas.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000017.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Flight Simulator 2020',
            'descripcion': 'Microsoft Flight Simulator (también conocido como Flight Simulator 2020) es un simulador de vuelo desarrollado por Asobo Studio y publicado por Xbox Game Studios. El juego permite a los jugadores experimentar la sensación de volar aviones en tiempo real sobre paisajes detallados generados por procedimientos que utilizan datos de Bing Maps.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000018.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Cities: Skylines',
            'descripcion': 'Cities: Skylines es un juego de simulación y construcción de ciudades desarrollado por Colossal Order y publicado por Paradox Interactive. El juego permite a los jugadores planificar, construir y gestionar una ciudad desde cero, abordando aspectos como la zonificación, el transporte, las políticas urbanas y el crecimiento económico.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000019.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Planet Zoo',
            'descripcion': 'Planet Zoo es un juego de simulación de gestión de zoológicos desarrollado y publicado por Frontier Developments. Los jugadores diseñan y construyen zoológicos, cuidan de los animales y gestionan el personal para crear hábitats y experiencias auténticas para los visitantes.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000020.jpg'
        },
        # Categoría "Deportes" (4 juegos)
        {
            'id': 21,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'FIFA 22',
            'descripcion': 'FIFA 22 es un videojuego de simulación de deportes desarrollado y publicado por Electronic Arts como parte de la serie FIFA. El juego presenta mejoras en la jugabilidad, gráficos actualizados y modos de juego innovadores, incluido un enfoque en la tecnología HyperMotion para proporcionar movimientos más realistas y auténticos de los jugadores.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000021.jpg'
        },
        {
            'id': 22,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'NBA 2K22',
            'descripcion': 'NBA 2K22 es un videojuego de simulación de baloncesto desarrollado por Visual Concepts y publicado por 2K Sports. El juego presenta mejoras en la jugabilidad, gráficos mejorados y modos de juego populares como MyCareer y MyTeam, ofreciendo una experiencia completa para los aficionados al baloncesto.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000022.jpg'
        },
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

