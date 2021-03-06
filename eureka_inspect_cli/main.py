import click
import sys
import requests
from operator import attrgetter

from .__init__ import __version__
from .node import Node


def parse_eureka_info_json(json):
    application_root = json['applications']

    parsed_nodes = []

    # app -> [up-instances], [down-instances]
    all_nodes = {}
    if application_root['application']:
        for application in application_root['application']:
            app_name = application['name']

            if app_name not in all_nodes:
                all_nodes[app_name] = {
                    'UP': [],
                    'DOWN': []
                }

            for node in application['instance']:
                instance_id = node.get('instanceId')
                if instance_id is None:
                    instance_id = '{}:{} (missing instanceId)'.format(node['hostName'], node['port']['$'])
                status = node['status']

                instances = all_nodes[app_name][status]

                instances.append(instance_id)

    for known_name, known_instances in all_nodes.items():
        known_instances['UP'].sort()
        known_instances['DOWN'].sort()
        parsed_nodes.append(Node(
            name=known_name, up_instances=known_instances['UP'], down_instances=known_instances['DOWN']))

    return sorted(parsed_nodes, key=attrgetter('name'))


def get_eureka_info(url, verbose):
    """[summary]

    Arguments:
        url {str} -- eureka server, e.g. 'http://localhost:8761/eureka'

    Returns:
        Array of Node -- parsed eureka instances
    """
    actual_url = url + '/apps/'
    if verbose:
        click.echo('actual url: ' + click.style(actual_url,
                                                fg='yellow', underline=True))
        click.echo('---------------------')
    r = requests.get(actual_url, headers={'Accept': 'application/json'})
    return parse_eureka_info_json(r.json())


@click.command('eureka_inspect')
@click.option('-h', '--host', default='localhost', help='Eureka host', show_default=True)
@click.option('-p', '--port', default=8761, help='Eureka port', show_default=True)
@click.option('-v', '--version', default=False, is_flag=True, help='Display version.')
@click.option('-V', '--verbose', default=False, is_flag=True, help='Display more info.')
def cli(host, port, version, verbose):
    """inspect eureka server and display registered nodes
    """
    if verbose:
        click.secho('eureka_inspect')

    if version:
        click.secho(__version__, fg='yellow')
        sys.exit(0)

    if verbose:
        click.echo('host: ' + click.style(host, fg='yellow', underline=True))
        click.echo(
            'port: ' + click.style('{}'.format(port), fg='yellow', underline=True))

        click.echo('---------------------')

    eureka_url = 'http://{}:{}/eureka'.format(host, port)

    if verbose:
        click.echo('eureka: ' + click.style(eureka_url,
                                            fg='yellow', underline=True))

        click.echo('---------------------')

    try:
        parsed_nodes = get_eureka_info(eureka_url, verbose)

        if parsed_nodes and len(parsed_nodes):
            for node in parsed_nodes:
                node.display()
        else:
            click.secho('No nodes fetched from Eureka', fg='yellow')
    except requests.exceptions.ConnectionError:
        click.secho('Error, can not connect to Eureka', fg='red')
    except Exception as identifier:
        print("unknown exception: ", identifier)
        click.secho('Error, can not retrive Eureka info', fg='red')


if __name__ == '__main__':
    cli()
