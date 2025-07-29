# Manager (in Python) for "Gpio Change Notifier (GCN)" clients

Usage:

    python3 -m gcn_manager --help
    options:
      -h, --help            show this help message and exit
      --trace
      --log-level LVL
      --print-env-then-exit
      --mqtt-host HOST
      --mqtt-port PORT
      --mqtt-user-name STR
      --mqtt-user-password STR
      --mqtt-keep-alive SEC
      --mqtt-connect-timeout SEC
      --mqtt-reconnect
      --mqtt-still-connecting-alert SEC
      --mqtt-transport STR
      --mqtt-client-id-random-bytes N
      --mqtt-tls-min-version VER
      --mqtt-tls-max-version VER
      --mqtt-tls-ciphers STR
      --mqtt-socket-send-buffer-size N
      --idle-loop-sleep SEC
      --client-heartbeat-max-skew SEC
      --client-heartbeat-watchdog SEC
      --enable-email-notifications
      --enable-sms-notifications
      --enable-twitter-notifications
      --notify-manager-starting-recipients A,B,C
      --notify-manager-still-connecting-recipients A,B,C
      --notify-manager-connected-recipients A,B,C
      --notify-manager-disconnected-recipients A,B,C
      --notify-manager-exiting-recipients A,B,C
      --notify-client-skewed-heartbeat-recipients A,B,C
      --notify-client-missed-heartbeat-recipients A,B,C
      --notify-client-dropped-items-recipients A,B,C
      --notify-client-status-change-online-recipients A,B,C
      --notify-client-status-change-offline-recipients A,B,C
      --notify-client-gpio-change-up-recipients A,B,C
      --notify-client-gpio-change-down-recipients A,B,C
      --email-from FROM
      --email-smtp-host HOST
      --email-smtp-port PORT
      --email-username NAME
      --email-password PASS
      --email-smtp-starttls
      --email-smtp-debug
      --sms-allow-country CODE
      --sms-ovh-sender-name NAME
      --sms-ovh-service-name NAME
      --sms-ovh-user-name USERNAME
      --sms-ovh-endpoint URL
      --sms-ovh-app-key SECRET
      --sms-ovh-app-secret SECRET
      --sms-ovh-consumer-key SECRET
      --sms-ovh-api-timeout SEC
      --twitter-app-consumer-key SECRET
      --twitter-app-consumer-secret SECRET
      --twitter-user-access-token SECRET
      --twitter-user-access-token-secret SECRET

Or use environment variables, see `constants.py`

## Features

- ENV
  - recipients
    - email -> DONE
    - sms -> DONE
    - twitter -> DONE

- MQTT
  - tls
    - mandatory -> DONE
    - mandatory verification -> DONE
  - auth
    - login/password -> DONE
  - errors
    - retryable
      - dns resolution -> DONE
      - host unreachable -> DONE
      - port unreachable -> DONE
    - fatal
      - auth failed -> DONE
      - tls failed -> DONE

- notifications
  - manager
    - starting -> DONE
    - exiting -> DONE
  - mqtt connection
    - failing -> DONE
    - established -> DONE
  - client
    - status
      - offline -> DONE
      - online -> DONE
    - heartbeat
      - skewed -> DONE
      - missed -> DONE
    - dropped item -> DONE
  - gpio
    - raising -> DONE
    - falling -> DONE

- brain
  - monitored gpio -> DONE
  - gpio initial -> DONE
  - gpio changed -> DONE
  - untracked -> DONE

## TODO

- implement a safeguard regarding notifications : max N/day

- external monitor for the manager, to ensure it is running

## development

python asyncio debug

    export PYTHONASYNCIODEBUG=1

install make on windows (for docker images) then restart powershell

    winget install --id ezwinports.make

## twitter-credentials

developer portal <https://developer.x.com/en>

project / app / keys and token

- Consumer Keys / API Key and Secret : `regenerate`
- Authentication Tokens
  - Bearer Token : __not needed__
  - Access Token and Secret : `regenerate`
- OAuth 2.0 Client ID and Client Secret : `regenerate`

project / app / settings

- oauth 1.0 : `Read and write and Direct message`
- type of app : `native app`
- oauth 2.0 / callback uri : `https://localhost` + mandatory website

_**IMPORTANT**: regenerate `Access Token and Secret` each time you modify oauth 1.0 permissions !_
