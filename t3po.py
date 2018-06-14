import logging
import os

from slackclient import SlackClient
from fabric import Connection

SLACK_ACCESS_TOKEN = os.environ['SLACK_ACCESS_TOKEN']
SLACK_CHANNEL_NAME = os.environ['SLACK_CHANNEL_NAME']
T3_POINT_NOTIFY_THRESHOLD = int(os.getenv('T3_POINT_NOTIFY_THRESHOLD', 999999999999999))

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def get_t3_point():
    try:
        result = Connection('login.t3.gsic.titech.ac.jp').run('t3-user-info group point', hide='both')
    except Exception:
        [logging.error(l) for l in result.stderr.splitlines()]
        raise
    [logging.debug(l) for l in result.stdout.splitlines()]
    points = {}
    for l in result.stdout.splitlines()[2:]:
        t = l.split()
        points[t[1]] = {'gid': int(t[0]), 'point': int(t[2])}
    return points


def format_topic(points):
    s = None
    for group_name in points.keys():
        point = points[group_name]['point']
        if point < T3_POINT_NOTIFY_THRESHOLD:
            if s is None:
                s = ''
            s += f'{group_name}={point:,} '
    return s


def t3po():
    points = get_t3_point()
    logging.info(points)
    cli = SlackClient(SLACK_ACCESS_TOKEN)
    result = cli.api_call('channels.list')
    logging.debug(result) if result['ok'] else logging.error(result)
    channel = [ch for ch in result['channels'] if ch['name'] == SLACK_CHANNEL_NAME]
    assert len(channel) == 1
    topic = format_topic(points)
    if topic is None:
        return
    result = cli.api_call('channels.setTopic', channel=channel[0]['id'], topic=topic)
    logging.debug(result) if result['ok'] else logging.error(result)


def main():
    t3po()


if __name__ == '__main__':
    main()
