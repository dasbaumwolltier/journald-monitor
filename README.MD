# JournalD Monitor
This is a small package written in Python, which attaches itself to the ``journalctl -f`` command and matches the lines against a list of regexes. It then executes the actions corresponding to the regexes.

## Commandline Options

These are the required commandline options for the monitor:
* ``-c CONFIG``\
The file path to the config file for the monitor.

These are the optional commandline options for the monitor:
* ``-l LOG_CONFIG``\
This is the config for the python logger, the monitor uses. The default config is to log to stdout with severity level INFO.

## Config File
The config file is a [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) config file. It has several options for the monitor itself and the actions, which can be executed.

All standard configuration options are found here:
```yaml
# The configuration for the monitor
monitor: {
    journalctl: {
        # The command for calling journalctl
        command: [
            "/usr/bin/env",
            "journalctl"
        ]
    },

    # The list of regexes for matching
    match_list: [
        {
            regex: ".*?TEST.*",

            # The list of actions to be executed, should the regex be matched against a line
            actions: [
                {
                    name: "send_matrix_message",
                    params: {
                        message: "JournalD Monitor message: $1",
                        config_number: 1
                    }
                },
                {
                    name: "send_telegram_message",
                    params: {
                        message: "Message: $1",
                        config_number: 0
                    }
                }
            ]
        }
    ]
}

# A list of configurations for the matrix related actions
matrix.configs: [
    {
        url: "https://chat.example.com",
        token: "ANOTHER_TOKEN",
        room_id: "!another_room:example.com"
    }
    {
        url: "https://chat.matrix.org",
        token: "MY_TOKEN",
        room_id: "!some_room_id:matrix.org"
    }
]

# A list of configurations for the telegram related actions
telegram.configs: [
    {
        token: "BOT_TOKEN",
        chat_id: "@some_user_or_chat"
    }
]
```

The config file should not be world readable, as it will contain secrets.

---

## LICENSE

This work is licensed under the Apache License v2.0.