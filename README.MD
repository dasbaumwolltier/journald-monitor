# JournalD Monitor
This is a small package written in Python, which attaches itself to the ``journalctl -f`` command and lets triggers run on every line, and then, if the trigger fires, executes various actions specified in the config. This program can be used to, for example, notify the admin if a particular sign of failure (e.g. Postfix not accepting email) occurs, or to create simple statistics in a database about how many SSH login tries have there been and what is the most tried out username.

## Commandline Options

These are the required commandline options for the monitor:
* ``-c CONFIG``\
The file path to the config file for the monitor.

These are the optional commandline options for the monitor:
* ``-l LOG_CONFIG``\
This is the config for the python logger, the monitor uses. The default config is to log to stdout with severity level INFO.

## List of triggers
* ``regex``: This trigger triggers when the given regex matches the journald line. This trigger replaces all ``$1, $2, ...`` in any action parameter with the value captured by the respective regex group.

## List of actions
### Database
* ``database_insert``: Inserts the ``values`` property into the ``fields`` property of the ``table`` specified.
  * ``table``: The name of the table to insert into
  * ``fields``: For example ``(id, name)`` (just like SQL)
  * ``values``: The string which is used after the ``VALUES`` statement in SQL

### Messenger
* ``send_matrix_message``: Sends the ``message`` to the room specified in the config
* ``send_telegram_message``: Send the ``message`` to the chat specified in the config

## List of configs
* ``database``
  * ``driver``: The name of the ODBC driver. This is specified in ``/etc/odbcinst.ini``.
  * ``server``: The address of the server. (Note that even sqlite must have localhost as a server)
  * ``database``: The name/the path of the database to use
  * ``port (optional)``: The port of the server
  * ``username (optional)``: The username used to authenticate with the database server
  * ``password (optional)``: The password used to authenticate with the database server
* ``matrix``
  * ``server``: The server on which the message should be sent
  * ``token``: The authentication token for sending the message
  * ``room_id``: The room id in which to send the message
* ``telegram``
  * ``token``: The bot token (get one from the [BotFather](https://t.me/botfather)) to authenticate with telegram
  * ``chat_id``: The chat id (can be either a user or a room) to send the message to/in.

## Config File
The config file is a [YAML](https://yaml.org/) config file. It has several options for the journald-monitor itself and the actions, which can be executed.

All standard configuration options are found here:
```yaml
# The configuration for the monitor
monitor:
  journalctl:
    # The command for calling journalctl
    command:
      - "/usr/bin/env"
      - "journalctl"

# The list of rules
rules:
  test_rule:
    triggers:
      - regex: ".*?TEST(.*)"
    # The list of actions to be executed should the regex be matched against a line
    actions:
      - name: "send_matrix_message"
        params:
          message: "JournalD Monitor message: $1"
          config: matrix_one
      - name: "send_telegram_message"
        params:
          message: "Message: $1"
          config: some-config-name-telegram
      - name: "database_insert"
        params:
          config: database
          table: "test_table"
          fields: "(field, type)"
          values: "('$1', 0)"


# A list of configurations for the matrix related actions
configs:
  matrix:
    matrix_one:
      url: "https://chat.example.com"
      token: "ANOTHER_TOKEN"
      room_id: "!another_room:example.com"
    matrix_two:
      url: "https://chat.matrix.org"
      token: "MY_TOKEN"
      room_id: "!some_room_id:matrix.org"

  # A list of configurations for the telegram related actions
  telegram:
    some-config-name-telegram:
      token: "BOT_TOKEN"
      chat_id: "@some_user_or_chat"

# A list of configuratoins for the database related actions
  database:
    database_one:
      driver: "PostgreSQL Unicode"
      server: localhost
      database: test
      username: journaldmonitor
      password: 1234
```

The config file should not be world readable (in other words: it should not have the permissions to be read by everyone), as it will contain secrets.

---

## LICENSE

This work is licensed under the Apache License v2.0.
