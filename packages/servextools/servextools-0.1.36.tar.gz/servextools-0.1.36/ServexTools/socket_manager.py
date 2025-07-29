def init():
    from gevent import monkey
    monkey.patch_all()

_socketio_instance = None

# Forma recomendada: usar URL explícita para Redis
REDIS_URL = 'redis://localhost:6379/0'  # Puedes parametrizar esto con variables de entorno

def get_socketio():
    global _socketio_instance
    return _socketio_instance

def init_socketio(app,isProduccion=False,Proyecto="Servex"):
    """
    Inicializa el socketio.
    
    Args:
        app: La aplicación Flask.
        isProduccion: Indica si el entorno es de producción.
        Proyecto: El nombre del proyecto.
    Returns:
        SocketIO: Instancia de SocketIO.
    
    Notas:
        Si no existe el archivo sctkRedis, se crea con un UUID aleatorio.
        Es necesario que importes 
            from gevent import monkey
        y parches al principio de la aplicación antes de las importaciones
            monkey.patch_all()
    Notas:
        Puedes usar la función init() para parchear gevent.
    """
    import uuid
    import ServexTools.Tools as Tools
    from flask_socketio import SocketIO
    global _socketio_instance
    if _socketio_instance is None:
        if not Tools.ExistFile('sctkRedis'):
            Tools.CreateFile(nombre="sctkRedis",datos=uuid.uuid4().hex)
        
        canalredis = Tools.ReadFile("sctkRedis")
        if isProduccion:
            _socketio_instance = SocketIO(app,
                            ping_timeout=25000,
                            ping_interval=10000,
                            cors_allowed_origins="*",
                            async_mode='gevent',
                            message_queue=REDIS_URL,  # <--- URL explícita
                            channel=Proyecto + canalredis,
                            logger=False,
                            engineio_logger=False)
        else:
            _socketio_instance = SocketIO(app,
                        ping_timeout=5000,
                        ping_interval=2000,
                        cors_allowed_origins="*",
                        async_mode='threading')
    return _socketio_instance

# Nota: Puedes usar variables de entorno para REDIS_URL en producción para mayor flexibilidad y seguridad.
