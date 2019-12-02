import click
import sys
from requests_html import HTMLSession
import requests

from __init__ import __version__

from node import Node


def display(node):
    """display a node

    Keyword Arguments:
        name {str} -- Name of the node (default: {''})
        status {str} -- Status of the node ('UP', 'DOWN') (default: {'UP'})
        instances {Array of String} -- Known instances (default: {''})
    """
    name = node.name
    status = node.status
    instances = node.instances
    print(f'display(name={name}, status={status}, instances={instances})')

    name_text = click.style(name.lower(), fg='yellow')

    style_text = ''
    if status == 'UP':
        style_text = click.style(status, fg='green')
    else:
        style_text = click.style(status, fg='red')

    instances_text = ''

    click.echo(name_text + '\t' + style_text + '\t' + click.style(instances))


def parse_eureka_info(r):
    """Parse http response

    Arguments:
        r {[type]} -- [description]
    """
    nodes = []
    for node in r.html.find('.list-group+h1+table tbody tr'):
        node_name = node.find('td')[0].text
        node_status_text = node.find('td')[3].text
        status_parts = node_status_text.split()
        node_status = status_parts[0]
        node_instances = status_parts[3]

        nodes.append(Node(name=node_name, status=node_status,
                          instances=node_instances))

    return nodes


def get_eureka_info(url):
    """HTTP requests

    Arguments:
        url {str} -- [description]
    """

    session = HTMLSession()
    r = session.get(url)

    return parse_eureka_info(r)


@click.command()
@click.option('-h', '--host', default='localhost', help='Eureka host', show_default=True)
@click.option('-p', '--port', default=8761, help='Eureka port', show_default=True)
@click.option('-v', '--version', default=False, is_flag=True, help='Display version.')
@click.option('-V', '--verbose', default=False, is_flag=True, help='Display more info.')
def cli(host, port, version, verbose):
    """[summary]

    Arguments:
        host {str} -- [description]
        port {int} -- [description]
        version {True} -- [description]
    """
    if verbose:
        click.secho('eureka-inspect-cli')

    if version:
        click.secho(__version__, fg='yellow')
        sys.exit(0)

    if verbose:
        click.echo('host: ' + click.style(host, fg=f'yellow', underline=True))
        click.echo(
            'port: ' + click.style(f'{port}', fg='yellow', underline=True))

        click.echo('---------------------')

    eureka_url = f'http://{host}:{port}/'

    if verbose:
        click.echo('eureka: ' + click.style(eureka_url,
                                            fg='yellow', underline=True))

        click.echo('---------------------')

    parsed_nodes = get_eureka_info(eureka_url)
    for node in parsed_nodes:
        node.print()


if __name__ == '__main__':
    cli()
    # get_eureka_info('http://192.168.1.233:8761/')
