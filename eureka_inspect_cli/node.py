import click

APP_ID_LEN = 26
STATUS_TEXT_LEN = 4
STATUS_COUNT_LEN = 5


def _app_id_text(name, status):
    if status == 'UP':
        return click.style(name.lower().rjust(APP_ID_LEN), fg='yellow')
    else:
        return click.style(name.lower().rjust(APP_ID_LEN), fg='red')


def _status_text(count, status):
    color = 'red'
    if status == 'UP':
        color = 'green'

    return click.style(status.rjust(STATUS_TEXT_LEN), fg=color) + click.style(' ({})'.format(count).ljust(STATUS_COUNT_LEN), fg=color)


class Node(object):
    name = ''
    up_instances = []
    down_instances = []

    def __init__(self, name='', up_instances=[], down_instances=[]):
        self.name = name
        self.up_instances = up_instances
        self.down_instances = down_instances

    def display(self):
        name = self.name
        up_instances = self.up_instances
        down_instances = self.down_instances

        name_text = _app_id_text(name, 'UP')
        name_text_down = _app_id_text(name, 'DOWN')

        style_text_up = _status_text(len(up_instances), 'UP')
        style_text_down = _status_text(len(down_instances), 'DOWN')

        up_instances_text = click.unstyle(', ').join(
            [click.style(ins, fg='yellow') for ins in up_instances])

        down_instances_text = click.unstyle(', ').join(
            [click.style(ins, fg='red') for ins in down_instances])

        if len(up_instances):
            click.echo(name_text + '\t' + style_text_up +
                       '\t' + up_instances_text)
        if len(down_instances):
            click.echo(name_text_down + '\t' + style_text_down +
                       '\t' + down_instances_text)
