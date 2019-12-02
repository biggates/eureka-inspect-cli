import click
import sys
from pyquery import PyQuery as pq
import requests
import re

from .__init__ import __version__
from .node import Node

REGEX_STATUS = '<b>(UP|DOWN)</b> \((\d+)\)'


def parse_eureka_info(html):
    """Parse http response

    Arguments:
        html {str} -- [description]
    """

    r = pq(html)

    nodes = []
    for tr in r('.list-group+h1+table tbody tr'):
        node = pq(tr)
        name = node.find('td b')[0].text
        instances_text = pq(node.find('td')[3]).html()
        up_instances = []
        down_instances = []

        # instances = '\n   <b>UP</b> (3) -\n  <a>...'
        current_instance = up_instances
        lines = [line.strip() for line in instances_text.splitlines()]
        lines = list(filter(None, lines))
        lines = list(filter(lambda l: len(l) > 5, lines))
        for line in lines:
            if not len(line):
                continue

            m = re.match(REGEX_STATUS, line)
            if m:
                status = m.group(1)
                count = int(m.group(2))

                if status == 'UP':
                    current_instance = up_instances
                elif status == 'DOWN':
                    current_instance = down_instances

            instance = pq(line, parser='html_fragments')

            if not instance:
                continue
            if not instance.is_('a'):
                continue

            if len(instance.text()):
                current_instance.append(instance.text())

        nodes.append(Node(name, up_instances, down_instances))

    return nodes


def get_eureka_info(url):
    """HTTP requests

    Arguments:
        url {str} -- [description]
    """

    r = requests.get(url)
    return parse_eureka_info(r.text)


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
