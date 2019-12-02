import click
import sys
from requests_html import HTMLSession
import requests

from __init__ import __version__

def display(name='', status='UP', instances=''):
    """display a node
    
    Keyword Arguments:
        name {str} -- Name of the node (default: {''})
        status {str} -- Status of the node ('UP', 'DOWN') (default: {'UP'})
        instances {Array of String} -- Known instances (default: {''})
    """    
    print(f'display(name={name}, status={status}, instances={instances})')
    name_text = click.style(name.lower(), fg='yellow')

    style_text = ''
    if status == 'UP':
        style_text = click.style(style_text, fg='green')
    else:
        style_text = click.style(style_text, fg='red')

    instances_text = ''

    click.echo(name_text + '\t' + style_text + '\t' + click.style(instances))

def parse_eureka_info(r):
    """Parse http response
    
    Arguments:
        r {[type]} -- [description]
    """    
    for node in r.html.find('.list-group+h1+table tbody tr'):
        node_name = node.find('td')[0].text
        node_status_text = node.find('td')[3].text
        status_parts = node_status_text.split()
        node_status = status_parts[0]
        node_instances = status_parts[3]
        display(name=node_name, status=node_status, instances=node_instances)

    return

def get_eureka_info(url):
    """HTTP requests

    Arguments:
        url {str} -- [description]
    """

    session = HTMLSession()    
    r = session.get(url)

    parse_eureka_info(r)

@click.command()
@click.option('-h', '--host', default='localhost', help='Eureka host', show_default=True)
@click.option('-p', '--port', default=8761, help='Eureka port', show_default=True)
@click.option('-v', '--version', is_flag=True, help='Display version.')
def cli(host, port, version):
    """[summary]
    
    Arguments:
        host {str} -- [description]
        port {int} -- [description]
        version {True} -- [description]
    """    
    click.secho('eureka-inspect-cli')
    if version:
        click.secho(__version__, fg='yellow')
        sys.exit(0)
    
    click.echo('host: ' + click.style(host, fg='yellow', underline=True))
    click.echo('port: ' + click.style(f'{port}', fg='yellow', underline=True))

if __name__ == '__main__':
    #cli()
    get_eureka_info('http://192.168.1.233:8761/')