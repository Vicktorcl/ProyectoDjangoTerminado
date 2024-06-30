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
        username='jdoe',
        tipo='Cliente', 
        nombre='John', 
        apellido='Doe', 
        correo=test_user_email if test_user_email else 'jdoe@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.111.111-1',	
        direccion='123 Elm Street, Springfield, \nIllinois 62701 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/jdoe.jpg')

    crear_usuario(
        username='asmith',
        tipo='Cliente', 
        nombre='Alice', 
        apellido='Smith', 
        correo=test_user_email if test_user_email else 'asmith@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='22.222.222-2', 
        direccion='456 Oak Avenue, Chicago, \nIllinois 60611 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/asmith.jpg')

    crear_usuario(
        username='bwhite',
        tipo='Cliente', 
        nombre='Bob', 
        apellido='White', 
        correo=test_user_email if test_user_email else 'bwhite@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='33.333.333-3', 
        direccion='789 Pine Road, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/bwhite.jpg')

    crear_usuario(
        username='jblack',
        tipo='Cliente', 
        nombre='Jack', 
        apellido='Black', 
        correo=test_user_email if test_user_email else 'jblack@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='44.444.444-4', 
        direccion='101 Maple Street, Seattle, \nWashington 98101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/jblack.jpg')

    crear_usuario(
        username='mclark',
        tipo='Cliente', 
        nombre='Mary', 
        apellido='Clark', 
        correo=test_user_email if test_user_email else 'mclark@example.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='55.555.555-5', 
        direccion='202 Birch Road, Denver, \nColorado 80201 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/mclark.jpg')

    # Crear superusuario de la tienda
    crear_usuario(
        username='admin',
        tipo='Administrador', 
        nombre='Admin', 
        apellido='User', 
        correo=test_user_email if test_user_email else 'admin@example.com', 
        es_superusuario=True, 
        es_staff=True, 
        rut='99.999.999-9', 
        direccion='Principal Office, Main Street, \nCiudad', 
        subscrito=False, 
        imagen='perfiles/admin.jpg')
    
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
        'nombre': 'Gears 5',
        'descripcion': 'Gears 5 es la última entrega de la famosa saga de disparos en tercera persona. Únete a Kait Diaz en su viaje para descubrir los orígenes de los Locust y proteger a Sera. Disfruta de una campaña épica y modos multijugador innovadores.',
        'precio': 34990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 20,
        'imagen': 'productos/000001.jpg'
    },
    {
        'id': 2,
        'categoria': Categoria.objects.get(id=1),
        'nombre': 'Dying Light 2',
        'descripcion': 'Dying Light 2 te sumerge en una ciudad devastada por el apocalipsis zombi. Explora un vasto mundo abierto, toma decisiones cruciales y usa tus habilidades de parkour para sobrevivir en este emocionante juego de acción y supervivencia.',
        'precio': 59990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 10,
        'imagen': 'productos/000002.jpg'
    },
    {
        'id': 3,
        'categoria': Categoria.objects.get(id=1),
        'nombre': 'Watch Dogs: Legion',
        'descripcion': 'En Watch Dogs: Legion, puedes reclutar y jugar como cualquier personaje que encuentres en las calles de Londres. Únete a la resistencia y lucha contra un régimen opresivo usando hackeo, combate y estrategia en un mundo abierto dinámico.',
        'precio': 49990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 25,
        'imagen': 'productos/000003.jpg'
    },
    {
        'id': 4,
        'categoria': Categoria.objects.get(id=1),
        'nombre': 'Sekiro: Shadows Die Twice',
        'descripcion': 'Sekiro: Shadows Die Twice es un desafiante juego de acción y aventura desarrollado por FromSoftware. Juega como un shinobi en busca de venganza y redención en un mundo feudal japonés lleno de peligros y enemigos formidables.',
        'precio': 59990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 15,
        'imagen': 'productos/000004.jpg'
    },
    {
        'id': 5,
        'categoria': Categoria.objects.get(id=1),
        'nombre': 'Just Cause 4',
        'descripcion': 'Just Cause 4 lleva la acción a nuevas alturas con su mundo abierto lleno de caos y destrucción. Juega como Rico Rodriguez y utiliza un vasto arsenal de armas y gadgets para derrocar a un régimen opresivo en la región de Solís.',
        'precio': 39990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 15,
        'imagen': 'productos/000005.jpg'
    },
    {
        'id': 6,
        'categoria': Categoria.objects.get(id=1),
        'nombre': 'Hitman 3',
        'descripcion': 'Hitman 3 es la conclusión épica de la trilogía World of Assassination. Juega como el Agente 47 y viaja por todo el mundo para eliminar a tus objetivos de manera creativa y sigilosa en algunos de los entornos más detallados y abiertos jamás creados.',
        'precio': 69990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 10,
        'imagen': 'productos/000006.jpg'
    },
    {
        'id': 7,
        'categoria': Categoria.objects.get(id=1),
        'nombre': 'Death Stranding',
        'descripcion': 'En Death Stranding, juegas como Sam Porter Bridges en una misión para reconectar a una sociedad fracturada. Este innovador juego de acción y exploración combina una narrativa profunda con un gameplay único y cautivador.',
        'precio': 59990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 10,
        'imagen': 'productos/000007.jpg'
    },
    {
        'id': 8,
        'categoria': Categoria.objects.get(id=1),
        'nombre': 'Control',
        'descripcion': 'Control es un juego de acción y aventura que te lleva a una realidad cambiante donde nada es lo que parece. Juega como Jesse Faden y explora la misteriosa Oficina Federal de Control, usando tus poderes sobrenaturales para combatir una amenaza de otro mundo.',
        'precio': 19990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 20,
        'imagen': 'productos/000008.jpg'
    },
    # Categoría "Aventura" (4 juegos)
    {
        'id': 9,
        'categoria': Categoria.objects.get(id=2),
        'nombre': 'Ori and the Will of the Wisps',
        'descripcion': 'Ori and the Will of the Wisps es un hermoso juego de aventuras y plataformas. Acompaña a Ori en un emotivo viaje a través de un mundo pintado a mano, lleno de desafíos y secretos por descubrir.',
        'precio': 29990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 20,
        'imagen': 'productos/000009.jpg'
    },
    {
        'id': 10,
        'categoria': Categoria.objects.get(id=2),
        'nombre': 'Hollow Knight',
        'descripcion': 'Hollow Knight es un juego de acción y aventura ambientado en un vasto mundo subterráneo. Explora cavernas, combate criaturas malignas y descubre los secretos de una antigua civilización en este aclamado título de estilo metroidvania.',
        'precio': 19990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 15,
        'imagen': 'productos/000010.jpg'
    },
    {
        'id': 11,
        'categoria': Categoria.objects.get(id=2),
        'nombre': 'The Last of Us Part II',
        'descripcion': 'The Last of Us Part II es una intensa experiencia narrativa de acción y aventura. Sigue a Ellie en su búsqueda de justicia y redención en un mundo postapocalíptico, enfrentando peligros tanto humanos como infectados.',
        'precio': 59990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 10,
        'imagen': 'productos/000011.jpg'
    },
    {
        'id': 12,
        'categoria': Categoria.objects.get(id=2),
        'nombre': 'Tomb Raider',
        'descripcion': 'Tomb Raider es una emocionante aventura de acción que sigue a una joven Lara Croft en su primera expedición. Explora tumbas antiguas, resuelve acertijos y combate enemigos mientras descubres los misterios de una isla olvidada.',
        'precio': 29990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 20,
        'imagen': 'productos/000012.jpg'
    },
    # Categoría "Estrategia" (4 juegos)
    {
        'id': 13,
        'categoria': Categoria.objects.get(id=3),
        'nombre': 'Starcraft II',
        'descripcion': 'Starcraft II es un juego de estrategia en tiempo real donde compites en batallas épicas en el universo de Starcraft. Elige entre tres razas únicas y utiliza tácticas avanzadas para derrotar a tus oponentes en este clásico de la estrategia.',
        'precio': 39990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 5,
        'imagen': 'productos/000013.jpg'
    },
    {
        'id': 14,
        'categoria': Categoria.objects.get(id=3),
        'nombre': 'Company of Heroes 2',
        'descripcion': 'Company of Heroes 2 es un juego de estrategia en tiempo real que te pone en el frente oriental de la Segunda Guerra Mundial. Lidera a tus tropas en intensas batallas y utiliza el entorno a tu favor para conseguir la victoria.',
        'precio': 19990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 15,
        'imagen': 'productos/000014.jpg'
    },
    {
        'id': 15,
        'categoria': Categoria.objects.get(id=3),
        'nombre': 'Command & Conquer Remastered',
        'descripcion': 'Command & Conquer Remastered Collection reúne dos de los juegos más emblemáticos de estrategia en tiempo real con gráficos mejorados y una jugabilidad modernizada. Revive la guerra entre GDI y NOD con características nuevas y clásicas.',
        'precio': 59990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 10,
        'imagen': 'productos/000015.jpg'
    },
    {
        'id': 16,
        'categoria': Categoria.objects.get(id=3),
        'nombre': 'Age of Empires IV',
        'descripcion': 'Age of Empires IV es un juego de estrategia en tiempo real que abarca la historia humana desde la Edad Media hasta la era moderna. Construye tu imperio, dirige ejércitos y expande tu civilización en este nuevo capítulo de la legendaria serie.',
        'precio': 69990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 10,
        'imagen': 'productos/000016.jpg'
    },
    # Categoría "Rol" (4 juegos)
    {
        'id': 17,
        'categoria': Categoria.objects.get(id=4),
        'nombre': 'The Witcher 3: Wild Hunt',
        'descripcion': 'The Witcher 3: Wild Hunt es un juego de rol de mundo abierto aclamado por la crítica. Juega como Geralt de Rivia y embarca en una épica búsqueda para encontrar a tu hija adoptiva, enfrentando monstruos y tomando decisiones que afectan la historia.',
        'precio': 19990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 25,
        'imagen': 'productos/000017.jpg'
    },
    {
        'id': 18,
        'categoria': Categoria.objects.get(id=4),
        'nombre': 'Final Fantasy XV',
        'descripcion': 'Final Fantasy XV es un juego de rol de acción que sigue al príncipe Noctis y sus amigos en una misión para recuperar su reino. Explora un vasto mundo abierto, combate enemigos formidables y disfruta de una historia conmovedora y épica.',
        'precio': 29990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 20,
        'imagen': 'productos/000018.jpg'
    },
    {
        'id': 19,
        'categoria': Categoria.objects.get(id=4),
        'nombre': 'Persona 5',
        'descripcion': 'Persona 5 es un juego de rol japonés que combina simulación de vida y exploración de mazmorras. Juega como un estudiante de secundaria que lidera un grupo de vigilantes con la capacidad de invocar personas, luchando contra la corrupción en la sociedad.',
        'precio': 59990,
        'descuento_subscriptor': 5,
        'descuento_oferta': 10,
        'imagen': 'productos/000019.jpg'
    },
    {
        'id': 20,
        'categoria': Categoria.objects.get(id=4),
        'nombre': 'Dark Souls III',
        'descripcion': 'Dark Souls III es un desafiante juego de rol de acción conocido por su dificultad y diseño de mundo interconectado. Explora un reino oscuro lleno de enemigos formidables y secretos ocultos, mientras intentas restaurar el fuego y salvar el mundo de la oscuridad.',
        'precio': 29990,
        'descuento_subscriptor': 10,
        'descuento_oferta': 20,
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

