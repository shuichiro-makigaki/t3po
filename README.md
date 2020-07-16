# T3PO: TSUBAME 3.0 POint checker

```
$ cat ~/.ssh/sshkey | docker container run -i --rm --env-file ~/t3po/env makisyu/t3po  
$ crontab -l
0 9,15 * * * cat ~/.ssh/sshkey | docker container run -i --rm --env-file ~/t3po/env makisyu/t3po
```

`env` file example:

```
SLACK_ACCESS_TOKEN=xoxp-hogehoge
SLACK_CHANNEL_NAME=tsubame    # no '#' prefixed
T3_LOGIN_USERNAME=user1
T3_POINT_NOTIFY_THRESHOLD=999999
T3_POINT_NOTIFY_IGNORED_GROUPS=group1,group2    # These groups are not notified.
```
