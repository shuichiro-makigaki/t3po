import logging
import os
from typing import List

from slack import WebClient
from fabric import Connection

SLACK_ACCESS_TOKEN = os.environ['SLACK_ACCESS_TOKEN']
SLACK_CHANNEL_NAME = os.environ['SLACK_CHANNEL_NAME']
T3_POINT_NOTIFY_THRESHOLD = int(os.getenv('T3_POINT_NOTIFY_THRESHOLD', 999999))
T3_POINT_NOTIFY_IGNORED_GROUPS = os.getenv('T3_POINT_NOTIFY_IGNORED_GROUPS', '').split(',')

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


class T3Point:
    def __init__(self, gid: int, group_name: str, deposit: int, balance: int):
        self.gid = gid
        self.group_name = group_name
        self.deposit = deposit
        self.balance = balance


def get_t3_point() -> List[T3Point]:
    try:
        result = Connection('login.t3.gsic.titech.ac.jp').run('t3-user-info group point', hide='both')
    except Exception:
        logging.error(result.stderr)
        raise
    points = []
    for l in result.stdout.splitlines()[2:-2]:
        t = l.split()
        points.append(T3Point(int(t[0]), t[1], int(t[2]), int(t[3])))
    return points


def format_topic(points: List[T3Point]) -> str:
    return ' '.join([f'{p.group_name}={p.balance:,}' for p in points])


def is_notified(point: T3Point) -> bool:
    return point.group_name not in T3_POINT_NOTIFY_IGNORED_GROUPS \
           and point.balance < T3_POINT_NOTIFY_THRESHOLD


def t3po():
    cli = WebClient(token=SLACK_ACCESS_TOKEN)
    resp = cli.conversations_list()
    if not resp['ok']:
        logging.error(resp)
        return
    channel = [_ for _ in resp['channels'] if _['name'] == SLACK_CHANNEL_NAME]
    if len(channel) == 0:
        logging.error('Target channel is not found')
        logging.error(resp)
        return
    points = [p for p in get_t3_point() if is_notified(p)]
    if len(points) == 0:
        return
    resp = cli.conversations_setTopic(channel=channel[0]['id'], topic=format_topic(points))
    if not resp['ok']:
        logging.error(resp)


def main():
    t3po()


if __name__ == '__main__':
    main()
