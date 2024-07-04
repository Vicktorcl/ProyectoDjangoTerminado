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
        username='cevans',
        tipo='Cliente', 
        nombre='Chris', 
        apellido='Evans', 
        correo=test_user_email if test_user_email else 'cevans@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/cevans.jpg')

    crear_usuario(
        username='eolsen',
        tipo='Cliente', 
        nombre='Elizabeth', 
        apellido='Olsen', 
        correo=test_user_email if test_user_email else 'eolsen@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/eolsen.jpg')

    crear_usuario(
        username='tholland',
        tipo='Cliente', 
        nombre='Tom', 
        apellido='Holland', 
        correo=test_user_email if test_user_email else 'tholland@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/tholland.jpg')

    crear_usuario(
        username='sjohansson',
        tipo='Cliente', 
        nombre='Scarlett', 
        apellido='Johansson', 
        correo=test_user_email if test_user_email else 'sjohansson@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/sjohansson.jpg')

    crear_usuario(
        username='cpratt',
        tipo='Administrador', 
        nombre='Chris', 
        apellido='Pratt', 
        correo=test_user_email if test_user_email else 'cpratt@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/cpratt.jpg')
    
    crear_usuario(
        username='mruffalo',
        tipo='Administrador', 
        nombre='Mark', 
        apellido='Ruffalo', 
        correo=test_user_email if test_user_email else 'mruffalo@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/mruffalo.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Robert',
        apellido='Downey Jr.',
        correo=test_user_email if test_user_email else 'rdowneyjr@marvel.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/rdowneyjr.jpg')
    
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
            'nombre': 'Grand Theft Auto V',
            'descripcion': 'Grand Theft Auto V te sumerge en la soleada ciudad de Los Santos y sus alrededores, donde seguirás las historias entrelazadas de tres criminales muy diferentes mientras planean y ejecutan audaces atracos para sobrevivir en una ciudad despiadada. Disfruta de un mundo abierto enorme y detallado, con una gran variedad de misiones, actividades y desafíos, además de un modo online multijugador en constante evolución.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000001.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Red Dead Redemption 2',
            'descripcion': 'Red Dead Redemption 2 es una épica historia sobre la vida en el despiadado corazón de América. El vasto y evocador mundo del juego también proporcionará la base para una nueva experiencia multijugador online.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000002.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Call of Duty: Modern Warfare II',
            'descripcion': 'Call of Duty: Modern Warfare II es la secuela de Modern Warfare (2019) y la decimonovena entrega de la serie Call of Duty. La campaña de Modern Warfare II sigue a la Fuerza Operativa 141 mientras persiguen a un terrorista iraní llamado Hassan Zyani, quien adquirió un misil balístico estadounidense.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000003.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'God of War Ragnarök',
            'descripcion': 'Únete a Kratos y Atreus en un viaje mítico por los Nueve Reinos mientras se preparan para la profetizada batalla que acabará con el mundo. En God of War Ragnarök, explorarás paisajes impresionantes y te enfrentarás a temibles enemigos, tanto dioses como monstruos, mientras buscas respuestas y aliados antes de que llegue el Ragnarök.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000004.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Doom Eternal',
            'descripcion': 'Doom Eternal es un shooter en primera persona desarrollado por id Software y publicado por Bethesda Softworks. El juego continúa la historia de Doom (2016), y sigue al Doom Slayer en su lucha contra las fuerzas del infierno que han invadido la Tierra.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000005.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Elden Ring',
            'descripcion': 'Elden Ring es un juego de rol de acción desarrollado por FromSoftware y publicado por Bandai Namco Entertainment. El juego se desarrolla en un mundo abierto llamado las Tierras Intermedias, donde los jugadores controlan a un personaje conocido como el Sinluz, que debe viajar por el mundo para restaurar el Elden Ring, un poderoso artefacto que ha sido destruido.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000006.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Horizon Forbidden West',
            'descripcion': 'Horizon Forbidden West es la secuela de Horizon Zero Dawn. El juego sigue a Aloy, una joven cazadora en un mundo postapocalíptico gobernado por máquinas. En Forbidden West, Aloy debe viajar a una nueva y peligrosa frontera para investigar una misteriosa plaga que está matando la vida vegetal y animal.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000007.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Spider-Man: Miles Morales',
            'descripcion': 'Spider-Man: Miles Morales es un juego de acción y aventura desarrollado por Insomniac Games y publicado por Sony Interactive Entertainment. El juego sigue a Miles Morales, un adolescente que adquiere poderes similares a los de Spider-Man después de ser mordido por una araña genéticamente modificada.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
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
            'nombre': 'Uncharted 4: A Thief\'s End',
            'descripcion': 'Uncharted 4: A Thief\'s End es un videojuego de acción-aventura desarrollado por Naughty Dog y publicado por Sony Computer Entertainment para PlayStation 4. El juego fue lanzado en mayo de 2016 y es la cuarta entrega principal de la serie Uncharted. La historia sigue a Nathan Drake, un cazador de tesoros retirado que se ve obligado a volver a su antigua vida cuando su hermano Sam reaparece.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000010.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Assassin\'s Creed Valhalla',
            'descripcion': 'Assassin\'s Creed Valhalla es un videojuego de acción-aventura desarrollado por Ubisoft Montreal y publicado por Ubisoft. Es la duodécima entrega principal de la serie Assassin\'s Creed y la sucesora de Assassin\'s Creed Odyssey de 2018. El juego se lanzó en noviembre de 2020 para Microsoft Windows, PlayStation 4, PlayStation 5, Xbox One, Xbox Series X/S y Stadia.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000011.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Star Wars Jedi: Fallen Order',
            'descripcion': 'Star Wars Jedi: Fallen Order es una emocionante aventura de acción en tercera persona ambientada en el universo de Star Wars. Ponte en la piel de Cal Kestis, un padawan que sobrevivió a la Orden 66 y debe completar su entrenamiento, desarrollar nuevas y poderosas habilidades con la Fuerza y dominar el arte del sable láser mientras te mantienes un paso por delante del Imperio y sus mortíferos Inquisidores.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000012.jpg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Civilization VI',
            'descripcion': 'Civilization VI es un juego de estrategia por turnos en el que los jugadores intentan construir un imperio que resista el paso del tiempo. Explora un nuevo mundo, investiga tecnologías, conquista a tus enemigos y enfréntate a los líderes más famosos de la historia mientras intentas construir la civilización más grande jamás conocida.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000013.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'XCOM 2',
            'descripcion': 'XCOM 2 es la secuela del galardonado juego de estrategia XCOM: Enemy Unknown. La Tierra ha cambiado y ahora está bajo control alienígena. Como líder de XCOM, una organización militar secreta, debes reconstruir la base de operaciones, reclutar nuevos soldados y liderar la resistencia para liberar a la humanidad del yugo alienígena.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000014.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Total War: Warhammer III',
            'descripcion': 'Total War: Warhammer III es un juego de estrategia en tiempo real y por turnos ambientado en el mundo de fantasía de Warhammer. El juego presenta cuatro razas jugables: Kislev, Cathay, Khorne y Nurgle, cada una con sus propias unidades, mecánicas y objetivos de campaña. Los jugadores pueden liderar a sus ejércitos en batallas masivas en tiempo real y gestionar sus imperios en un mapa de campaña por turnos.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000015.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Age of Empires IV',
            'descripcion': 'Age of Empires IV es un juego de estrategia en tiempo real desarrollado por Relic Entertainment y publicado por Xbox Game Studios. El juego es la cuarta entrega principal de la serie Age of Empires y fue lanzado en octubre de 2021. El juego presenta ocho civilizaciones jugables, cada una con sus propias unidades, tecnologías y edificios únicos.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000016.jpg'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'The Witcher 3: Wild Hunt',
            'descripcion': 'The Witcher 3: Wild Hunt es un juego de rol de acción de mundo abierto desarrollado y publicado por CD Projekt Red. El juego sigue a Geralt de Rivia, un cazador de monstruos profesional conocido como brujo, mientras busca a su hija adoptiva, Ciri, quien está siendo perseguida por la Cacería Salvaje, una fuerza espectral que busca usar sus poderes para sus propios fines.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000017.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Final Fantasy VII Remake',
            'descripcion': 'Final Fantasy VII Remake es una reimaginación del clásico juego de rol de 1997. El juego sigue a Cloud Strife, un ex-SOLDADO que se une a un grupo eco-terrorista llamado AVALANCHE para luchar contra la megacorporación Shinra, que está drenando la energía vital del planeta.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000018.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Cyberpunk 2077',
            'descripcion': 'Cyberpunk 2077 es un juego de rol de acción de mundo abierto desarrollado y publicado por CD Projekt Red. El juego se desarrolla en Night City, una megaciudad futurista obsesionada con el poder, el glamour y la modificación corporal. Los jugadores asumen el papel de V, un mercenario que puede ser personalizado en términos de género, apariencia y trasfondo.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000019.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Diablo IV',
            'descripcion': 'Diablo IV es un juego de rol de acción de mazmorras desarrollado y publicado por Blizzard Entertainment. Es la cuarta entrega principal de la serie Diablo y fue lanzado en junio de 2023. El juego se desarrolla en un mundo oscuro y gótico llamado Santuario, donde los jugadores luchan contra las fuerzas del infierno.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000020.jpg'
        }
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

