PLUGIN = {}
IMPORT_HOOKS = {}



DEFINITION = {
    'plugin': [
        ('', 'instrument_plugin'),
    ],
    'standalone': [
        ('', 'instrument_standalone_single'),
        ('', 'instrument_standalone_multiple')
    ],
    'httpc_httplib': [
        ('httplib', 'instrument_httplib'),
        ('http.client', 'instrument_httplib'),
        ('httplib2', 'instrument_httplib2'),
    ],
    'httpc_requests': [
        ('requests.sessions', 'instrument_requests'),
    ],
    'httpc_urllib3': [
        ('urllib3.request', 'instrument_urllib3'),
    ],
    'httpc_django': [
        ('revproxy.views', 'instrument_revproxy_views'),
    ],
    'database_mysql': [
        ('MySQLdb', 'instrument_MySQLdb'),
        ('MySQLdb.cursors', 'instrument_MySQLdb_cursors'),
        ('pymysql', 'instrument_pymysql'),
        ('pymysql.cursors', 'instrument_pymysql_cursors'),
    ],
    'database_postgresql': [
        ('psycopg2', 'instrument_psycopg2'),
        ('psycopg2._psycopg', 'instrument_psycopg2_connection'),
        ('psycopg2.extensions', 'instrument_psycopg2_extensions'),
    ],
    'database_neo4j': [
        ('neo4j', 'instrument_neo4j')
    ],
    'database_toolkit': [
        ('sqlalchemy.orm.session', 'instrument_sqlalchemy'),
        ('sqlalchemy.engine.default', 'instrument_sqlalchemy_engine'),
        ('sqlalchemy.engine.create', 'instrument_sqlalchemy_engine_basic'),
        ('sqlalchemy.engine', 'instrument_sqlalchemy_engine_basic'),
    ],
    'application_starlette' : [
        ('starlette.websockets' , 'instrument_starlette_websocket'),
    ],
    'application_wsgi': [
        ('', ''),
    ],
    'application_bottle': [
        ('bottle', 'instrument'),
    ],
    'application_cherrypy': [
        ('cherrypy', 'instrument'),
    ],
    'application_django': [
        ('django.core.handlers.wsgi', 'instrument'),
        ('django.core.handlers.base', 'instrument_handlers_base'),
        ('django.views.generic.base', 'instrument_generic_base'),
        ('django.contrib.staticfiles.handlers', 'instrument_handlers_static'),
        ('channels.http', 'instrument_handlers_channels'),

        # Django==1.10
        ('django.urls.resolvers', 'instrument_url_resolvers', False),
        ('django.urls.base', 'instrument_urls_base', False),
        ('django.core.handlers.exception', 'instrument_handlers_exception',
         False),

    ],
    'application_django_asgi': [
        ('django.core.handlers.asgi', 'instrument_asgi'),
    ],
    'application_flask': [
        ('flask', 'instrument'),
    ],
    'application_tornado': [
        ('tornado.web', 'instrument'),
    ],
    'application_celery': [
        ('celery.execute.trace', 'instrument_celery_execute_trace'),
        ('celery.task.trace', 'instrument_celery_execute_trace'),
        ('celery.app.trace', 'instrument_celery_execute_trace'),
    ],
    'database_redis':[
        ('redis','instrument_redis_connection'),
    ],
    'email_smtp':[
        ('smtplib','instrument_smtp'),
    ],
    'amqp_pika':[
        ('pika.channel','instrument_pika'),
    ],
    'application_nameko': [
        ('nameko.containers', 'instrument_nameko_spawn_worker'),
        ('spsengine.containers', 'instrument_nameko_spawn_worker'),
    ],
    'application_graphql':[
        #graphen-core 3.x~
        ('graphql.execution.execute','instrument_graphql'),

        #graphen-core 2.x
        ('graphql.execution.executor','instrument_graphql'),
    ],
    'database_mongo':[
        ('pymongo','instrument_mongo_client'),
    ],
    'logging':[
        ('logging.handlers', 'instrument_logging'),
        ('loguru._handler','instrument_loguru'),
    ],
    'application_fastapi': [
        ('fastapi.applications', 'instrument_applications'),
        ('fastapi.routing', 'instrument'),
        ('fastapi.dependencies.utils', 'instrument_util'),

    ],
    'application_frappe': [
        ('frappe.app', 'instrument'),
    ],
    'application_odoo': [
        ('odoo', 'instrument'),
    ],
    'database_cxoracle':[
        ('cx_Oracle', 'instrument_oracle_client'),
    ],
}
