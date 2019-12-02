import click



class Node(object):

    name = ''
    status = ''
    instances = []

    def __init__(self, name='', status='UP', instances=[]):
        self.name = name
        self.status = status
        self.instances = instances

    def print(self):
        name = self.name
        status = self.status
        instances = self.instances
        # print(f'display(name={name}, status={status}, instances={instances})')

        name_text = click.style(name.lower(), fg='yellow')
        name_text = name_text.rjust(36)

        style_text = ''
        if status == 'UP':
            style_text = click.style(status, fg='green')
        else:
            style_text = click.style(status, fg='red')

        style_text = style_text.rjust(6)

        instances_text = ''

        click.echo(name_text + '\t' + style_text +
                   '\t' + click.style(instances))
