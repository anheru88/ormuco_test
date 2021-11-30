import json
from flask import Flask, request
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client as Nova
from glanceclient import Client as Glance

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/flavors/')
def get_flavors():
    request_json = request.get_json()
    validation = validate(request_json)
    if validation is not None:
        return validation

    keystone_session = get_keystone_session(request_json)

    nova = Nova('2', endpoint_type='public', session=keystone_session)

    flavors = list()

    for flavor in nova.flavors.list():
        flavors.append(flavor._info)

    return json.dumps(flavors)


@app.route('/images/')
def get_images():
    request_json = request.get_json()
    validation = validate(request_json)
    if validation is not None:
        return validation

    keystone_session = get_keystone_session(request_json)

    glance = Glance('2', session=keystone_session)

    images = list()

    for image in glance.images.list():
        images.append(image)

    return json.dumps(images)


@app.route('/keys/')
def get_keys():
    request_json = request.get_json()
    validation = validate(request_json)
    if validation is not None:
        return validation

    keystone_session = get_keystone_session(request_json)

    nova = Nova('2', endpoint_type='public', session=keystone_session)

    keys = list()

    for key in nova.keypairs.list():
        keys.append(key._info)

    return json.dumps(keys)


@app.route('/servers')
def get_servers():
    request_json = request.get_json()
    validation = validate(request_json)
    if validation is not None:
        return validation

    keystone_session = get_keystone_session(request_json)

    nova = Nova('2', endpoint_type='public', session=keystone_session)

    servers = list()

    for server in nova.servers.list():
        servers.append(server._info)

    return json.dumps(servers)


@app.route('/servers/create', methods=["POST"])
def create_server():
    request_json = request.get_json()
    validation = validate(request_json, True)
    if validation is not None:
        return validation

    keystone_session = get_keystone_session(request_json)

    nova = Nova('2', endpoint_type='public', session=keystone_session)

    try:
        response = nova.servers.create(
            request_json.get("server_name"),
            request_json.get("image"),
            request_json.get("flavor"),
            key_name=request_json.get("key_name")
        )

        return "Servidor Creado con exito"

    except:
        return "Error al crear el servidor"


def get_keystone_session(request_json):
    auth = v3.Password(auth_url=request_json.get("auth_url"),
                       username=request_json.get('email'),
                       password=request_json.get("password"),
                       project_id=request_json.get("project_id"))
    return session.Session(auth=auth)


def validate(request_json, create_server=False):
    email = request_json.get('email')
    if email is None:
        return "Please give the email"
    password = request_json.get("password")
    if password is None:
        return "Please give the password"
    project_id = request_json.get("project_id")
    if project_id is None:
        return "Please give the project_id"
    auth_url = request_json.get("auth_url")
    if auth_url is None:
        return "Please give the auth_url"
    if create_server is True:
        server_name = request_json.get("server_name")
        if server_name is None:
            return "Please give the server_name"
        flavor = request_json.get("flavor")
        if flavor is None:
            return "Please give the flavor"
        key_name = request_json.get("key_name")
        if key_name is None:
            return "Please give the key_name"
        image = request_json.get("image")
        if image is None:
            return "Please give the image"

    return None
