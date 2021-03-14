import sys
import os
import subprocess
import platform
import docker
import argparse
from urllib.request import urlretrieve


def create_neo4j_container(cli):
    print('Create `neo4j_websem` container...')
    host_config = cli.create_host_config(port_bindings={7474: 7474, 7687: 7687})
    cli.create_container('neo4j',
                         ports=[7474, 7687],
                         host_config=host_config,
                         name='neo4j_websem')
    print('    Done!')


def setup_docker():
    print('Set up Neo4j for docker')
    client = docker.from_env()
    cli = docker.APIClient(base_url='unix://var/run/docker.sock')
    images_tags = [im.tags[0] if len(im.tags) > 0 else '' for im in client.images.list()]
    if not any('neo4j' in im for im in images_tags):
        print('No `neo4j` image detected, pull `neo4j:latest`...')
        cli.pull('neo4j', tag='latest')
        print('    Done!')
    create_neo4j_container(cli)
    print('Download neosemantic plugin...')
    link = 'https://github.com/neo4j-labs/neosemantics/releases/download/4.2.0.0/neosemantics-4.2.0.0.jar'
    urlretrieve(link, 'neosemantics-4.2.0.0.jar')
    print('    Done!')
    # Ugly
    print('Copy neosemantic plugin inside container...')
    subprocess.run('docker cp ./neosemantics-4.2.0.0.jar neo4j_websem:/var/lib/neo4j/plugins', shell=True)
    os.remove('./neosemantics-4.2.0.0.jar')
    print('   Done!')
    print('Modify container neo4j conf file...')
    subprocess.run('docker cp neo4j_websem:/var/lib/neo4j/conf/neo4j.conf ./', shell=True)
    with open('neo4j.conf', 'a') as conf_file:
        conf_file.write('dbms.unmanaged_extension_classes=n10s.endpoint=/rdf')
    subprocess.run('docker cp ./neo4j.conf neo4j_websem:/var/lib/neo4j/conf/neo4j.conf', shell=True)
    os.remove('./neo4j.conf')
    print('    Done!')


def setup_local(neo4j_path):
    print('The local setup without docker hasn\'t been implemented yet.')
    print('Either use docker or setup Neo4j by yourself, for the later you can find some instructions in the README')


parser = argparse.ArgumentParser(description='Script to setup neo4j on a local machin')
parser.add_argument('-d', '--docker', action='store_true', default=False)
parser.add_argument('-p', '--path',
                    nargs=1,
                    type=str,
                    default='neo4j:/var/lib/neo4j/')
args = parser.parse_args()
use_docker = args.docker
neo4j_path = args.path
if use_docker:
    setup_docker()
else:
    if neo4j_path is None:
        system = platform.system()
        if system == 'Windows':
            neo4j_path = os.path.expandvars(r'%APPDATA%\Neo4j Community Edition\\')
        elif system in ('Linux', 'Darwin'):
            neo4j_path = '/var/lib/neo4j/'
    setup_local(neo4j_path)
