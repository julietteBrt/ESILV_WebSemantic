import platform
import docker


def create_fuseki_container(cli, volume_name):
    host_config = cli.create_host_config(
            port_bindings={3030: 3030},
            volumes_from=[volume_name])
    cli.create_container('stain/jena-fuseki',
                         detach=True,
                         ports=[3030],
                         host_config=host_config,
                         environment={'ADMIN_PASSWORD': 'pw'},
                         name='fuseki')


def create_fuseki_data_volume(cli):
    cli.create_container('busybox', volumes=['/fuseki'], name='fuseki-data')


def setup_fuseki():
    base_url = 'tcp://127.0.0.1:1234' if platform.system() == 'Windows' else 'unix://var/run/docker.sock'
    cli = docker.APIClient(base_url=base_url)
    create_fuseki_data_volume(cli)
    create_fuseki_container(cli, 'fuseki-data')
    cli.start('fuseki')
    cli.exec_create('fuseki', 'apt-get update')
    cli.exec_create('fuseki', 'apt-get install -y --no-install-recommends procps')


setup_fuseki()
