#!/usr/bin/env python3

import asyncio
import logging
import os
import random
import signal
import ssl
import sys
from argparse import ArgumentParser, Namespace
from asyncio import AbstractEventLoop

from dotenv import load_dotenv

from gcn_manager import AppError, datetime_system_tz
from gcn_manager.brain import Brain
from gcn_manager.constants import *
from gcn_manager.mqtt import MqttAgent
from gcn_manager.notifiers import (
    ManagerStartingNotification,
    ManagerExitingNotification,
    setup_notification_recipients,
    NotificationError,
)


class App:
    def __init__(self, args: Namespace, loop: AbstractEventLoop) -> None:
        self._args = args
        self._loop = loop
        self._shutdown_requested = asyncio.Event()
        self._brain = Brain(args)
        self._mqtt_client_id = f"{MQTT_APP_MANAGER}_{random.randbytes(args.mqtt_client_id_random_bytes).hex().lower()}"
        self._mqtt_agent = MqttAgent(
            args,
            self._mqtt_client_id,
            processor=self._brain,
            shutdown_requested=self._shutdown_requested,
            event_loop=self._loop,
        )

    @property
    def mqtt_client_id(self) -> str:
        return self._mqtt_client_id

    async def _run_loop(self) -> None:
        while True:
            await self._mqtt_agent.run_once()
            await self._brain.shutdown()
            if not self._args.mqtt_reconnect or self._shutdown_requested.is_set():
                break

    def _graceful_shutdown(self, sig: signal.Signals) -> None:
        logging.info(f"Received signal {sig}, requesting graceful shutdown")
        self._shutdown_requested.set()

    async def run_with_graceful_shutdown(self) -> None:
        for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
            self._loop.add_signal_handler(sig, self._graceful_shutdown, sig)
        try:
            await self._run_loop()
        except asyncio.CancelledError:
            if not self._shutdown_requested.is_set():
                logging.error(
                    "Main task was cancelled but no shutdown had been requested beforehand"
                )
            else:
                logging.warning(
                    "Main task was cancelled while a shut down was requested"
                )

    @staticmethod
    async def run(args: Namespace) -> None:
        random.seed()
        start = datetime_system_tz()
        logging.debug(f"Running on system timezone : {start.tzinfo}")
        loop = asyncio.get_running_loop()
        app = App(args, loop)
        try:
            await ManagerStartingNotification(
                id=app.mqtt_client_id, started_at=start
            ).send()
        except NotificationError as e:
            raise AppError(
                f"Error while sending manager start notification : {e}")
        try:
            await app.run_with_graceful_shutdown()
        except KeyboardInterrupt:
            logging.info("Shutting down due to user interruption")
        finally:
            try:
                await ManagerExitingNotification(
                    id=app.mqtt_client_id, run_duration=datetime_system_tz() - start
                ).send()
            except NotificationError as e:
                logging.error(
                    f"Error while sending manager stop notification : {e}")

            logging.info("Exiting application loop")


def _tls_available_versions() -> tuple[str, ...]:
    return tuple(v for v in vars(ssl.TLSVersion) if not v.startswith("_"))


def _to_tls_version(tls_version: str | None) -> ssl.TLSVersion | None:
    if tls_version is None:
        return None
    if not hasattr(ssl.TLSVersion, tls_version):
        versions = " ".join(_tls_available_versions())
        raise AppError(
            f"Unknown TLS version '{tls_version}', available versions: {versions}"
        )
    return getattr(ssl.TLSVersion, tls_version)


def main_trace() -> None:
    load_dotenv()

    parser = ArgumentParser()
    parser.add_argument(CLI_OPT_TRACE, action="store_true")
    parser.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default=os.environ.get(ENV_GCN_MQTT_LOG_LEVEL,
                               DEFAULT_GCN_MQTT_LOG_LEVEL),
        metavar="LVL",
    )
    parser.add_argument(
        "--print-env-then-exit",
        action="store_true",
    )

    parser.add_argument(
        "--mqtt-host",
        metavar="HOST",
        default=os.environ.get(ENV_GCN_MQTT_SERVER_HOST, None),
    )
    parser.add_argument(
        "--mqtt-port",
        type=int,
        metavar="PORT",
        default=os.environ.get(ENV_GCN_MQTT_SERVER_PORT, None),
    )
    parser.add_argument(
        "--mqtt-user-name",
        metavar="STR",
        default=os.environ.get(ENV_GCN_MQTT_USER_NAME, None),
    )
    parser.add_argument(
        "--mqtt-user-password",
        metavar="STR",
        default=os.environ.get(ENV_GCN_MQTT_USER_PASSWORD, None),
    )
    parser.add_argument(
        "--mqtt-keep-alive",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_MQTT_KEEPALIVE_SECOND, DEFAULT_GCN_MQTT_KEEPALIVE_SECOND
        ),
    )
    parser.add_argument(
        "--mqtt-connect-timeout",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_MQTT_CONNECT_TIMEOUT_SECOND, DEFAULT_GCN_MQTT_CONNECT_TIMEOUT_SECOND
        ),
    )
    parser.add_argument(
        "--mqtt-reconnect",
        action="store_true",
        default=os.environ.get(ENV_GCN_MQTT_RECONNECT,
                               DEFAULT_GCN_MQTT_RECONNECT),
    )
    parser.add_argument(
        "--mqtt-still-connecting-alert",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_MQTT_STILL_CONNECTING_ALERT, DEFAULT_GCN_MQTT_STILL_CONNECTING_ALERT
        ),
    )
    parser.add_argument(
        "--mqtt-transport",
        choices=("tcp", "websocket", "unix"),
        metavar="STR",
        default=os.environ.get(ENV_GCN_MQTT_TRANSPORT,
                               DEFAULT_GCN_MQTT_TRANSPORT),
    )
    parser.add_argument(
        "--mqtt-client-id-random-bytes",
        type=int,
        metavar="N",
        default=os.environ.get(
            ENV_GCN_MQTT_CLIENT_ID_RANDOM_BYTES, DEFAULT_GCN_MQTT_CLIENT_ID_RANDOM_BYTES
        ),
    )
    parser.add_argument(
        "--mqtt-tls-min-version",
        metavar="VER",
        choices=_tls_available_versions(),
        default=_to_tls_version(
            os.environ.get(
                ENV_GCN_MQTT_TLS_MIN_VERSION, DEFAULT_GCN_MQTT_TLS_MIN_VERSION
            )
        ),
    )
    parser.add_argument(
        "--mqtt-tls-max-version",
        metavar="VER",
        choices=_tls_available_versions(),
        default=_to_tls_version(
            os.environ.get(
                ENV_GCN_MQTT_TLS_MAX_VERSION, DEFAULT_GCN_MQTT_TLS_MAX_VERSION
            )
        ),
    )
    parser.add_argument(
        "--mqtt-tls-ciphers",
        default=os.environ.get(ENV_GCN_MQTT_TLS_CIPHERS,
                               DEFAULT_GCN_MQTT_TLS_CIPHERS),
        metavar="STR",
    )
    parser.add_argument(
        "--mqtt-socket-send-buffer-size",
        type=int,
        default=os.environ.get(
            ENV_GCN_MQTT_SOCKET_SEND_BUFFER_SIZE,
            DEFAULT_GCN_MQTT_SOCKET_SEND_BUFFER_SIZE,
        ),
        metavar="N",
    )

    parser.add_argument(
        "--idle-loop-sleep",
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_IDLE_LOOP_SLEEP_SEC, DEFAULT_GCN_IDLE_LOOP_SLEEP_SEC
        ),
    )
    parser.add_argument(
        "--client-heartbeat-max-skew",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_HEARTBEAT_MAX_SKEW_SEC, DEFAULT_GCN_HEARTBEAT_MAX_SKEW_SEC
        ),
    )
    parser.add_argument(
        "--client-heartbeat-watchdog",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_HEARTBEAT_WATCHDOG_SEC, DEFAULT_GCN_HEARTBEAT_WATCHDOG_SEC
        ),
    )
    parser.add_argument(
        "--client-gpio-change-debounce-sec",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_CLIENT_GPIO_CHANGE_DEBOUNCE_SEC,
            DEFAULT_GCN_CLIENT_GPIO_CHANGE_DEBOUNCE_SEC
        ),
    )

    parser.add_argument(
        "--enable-email-notifications",
        action="store_true",
        default=bool(int(os.environ.get(ENV_GCN_ENABLE_NOTIFY_EMAIL, "0"))),
    )
    parser.add_argument(
        "--enable-sms-notifications",
        action="store_true",
        default=bool(int(os.environ.get(ENV_GCN_ENABLE_NOTIFY_SMS, "0"))),
    )
    parser.add_argument(
        "--enable-twitter-notifications",
        action="store_true",
        default=bool(int(os.environ.get(ENV_GCN_ENABLE_NOTIFY_TWITTER, "0"))),
    )

    parser.add_argument(
        "--notify-manager-starting-recipients",
        metavar="A,B,C",
        default=os.environ.get(ENV_GCN_MANAGER_STARTING_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-manager-still-connecting-recipients",
        metavar="A,B,C",
        default=os.environ.get(
            ENV_GCN_MANAGER_STILL_CONNECTING_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-manager-connected-recipients",
        metavar="A,B,C",
        default=os.environ.get(ENV_GCN_MANAGER_CONNECTED_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-manager-disconnected-recipients",
        metavar="A,B,C",
        default=os.environ.get(ENV_GCN_MANAGER_DISCONNECTED_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-manager-exiting-recipients",
        metavar="A,B,C",
        default=os.environ.get(ENV_GCN_MANAGER_EXITING_RECIPIENTS, None),
    )

    parser.add_argument(
        "--notify-client-skewed-heartbeat-recipients",
        metavar="A,B,C",
        default=os.environ.get(
            ENV_GCN_CLIENT_SKEWED_HEARTBEAT_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-client-missed-heartbeat-recipients",
        metavar="A,B,C",
        default=os.environ.get(
            ENV_GCN_CLIENT_MISSED_HEARTBEAT_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-client-dropped-items-recipients",
        metavar="A,B,C",
        default=os.environ.get(ENV_GCN_CLIENT_DROPPED_ITEMS_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-client-status-change-online-recipients",
        metavar="A,B,C",
        default=os.environ.get(
            ENV_GCN_CLIENT_STATUS_CHANGE_ONLINE_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-client-status-change-offline-recipients",
        metavar="A,B,C",
        default=os.environ.get(
            ENV_GCN_CLIENT_STATUS_CHANGE_OFFLINE_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-client-gpio-change-up-recipients",
        metavar="A,B,C",
        default=os.environ.get(ENV_GCN_CLIENT_GPIO_CHANGE_UP_RECIPIENTS, None),
    )
    parser.add_argument(
        "--notify-client-gpio-change-down-recipients",
        metavar="A,B,C",
        default=os.environ.get(
            ENV_GCN_CLIENT_GPIO_CHANGE_DOWN_RECIPIENTS, None),
    )

    parser.add_argument(
        "--email-from", metavar="FROM",
        default=os.environ.get(ENV_GCN_EMAIL_FROM, None)
    )
    parser.add_argument(
        "--email-smtp-host",
        metavar="HOST",
        default=os.environ.get(ENV_GCN_EMAIL_SMTP_HOST, None),
    )
    parser.add_argument(
        "--email-smtp-port",
        type=int,
        metavar="PORT",
        default=os.environ.get(ENV_GCN_EMAIL_SMTP_PORT, None),
    )
    parser.add_argument(
        "--email-username",
        metavar="NAME",
        default=os.environ.get(ENV_GCN_EMAIL_SMTP_USERNAME, None),
    )
    parser.add_argument(
        "--email-password",
        metavar="PASS",
        default=os.environ.get(ENV_GCN_EMAIL_SMTP_PASSWORD, None),
    )
    parser.add_argument(
        "--email-smtp-starttls",
        action="store_true",
        default=bool(int(os.environ.get(ENV_GCN_EMAIL_SMTP_STARTTLS, "0"))),
    )
    parser.add_argument(
        "--email-smtp-debug",
        action="store_true",
        default=bool(int(os.environ.get(ENV_GCN_EMAIL_SMTP_DEBUG, "0"))),
    )
    parser.add_argument(
        "--email-smtp-disable-tls13",
        action="store_true",
        default=bool(
            int(os.environ.get(ENV_GCN_EMAIL_SMTP_DISABLE_TLS13, "0"))),
    )
    parser.add_argument(
        "--email-smtp-send-as-report",
        action="store_true",
        default=bool(
            int(os.environ.get(ENV_GCN_EMAIL_SMTP_SEND_AS_REPORT, "0"))),
    )
    parser.add_argument(
        "--email-smtp-timeout",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_EMAIL_SMTP_TIMEOUT_SEC, DEFAULT_GCN_EMAIL_SMTP_TIMEOUT_SEC
        ),
    )

    parser.add_argument(
        "--sms-allow-country",
        metavar="CODE",
        default=os.environ.get(ENV_GCN_ALLOW_SMS_COUNTRIES, None),
    )
    parser.add_argument(
        "--sms-ovh-sender-name",
        metavar="NAME",
        default=os.environ.get(ENV_GCN_OVH_SMS_SENDER_NAME, None),
    )
    parser.add_argument(
        "--sms-ovh-service-name",
        metavar="NAME",
        default=os.environ.get(ENV_GCN_OVH_SMS_SERVICE_NAME, None),
    )
    parser.add_argument(
        "--sms-ovh-user-name",
        metavar="USERNAME",
        default=os.environ.get(ENV_GCN_OVH_SMS_USER_NAME, None),
    )
    parser.add_argument(
        "--sms-ovh-endpoint",
        metavar="URL",
        choices=KNOWN_OVH_API_ENDPOINT_NAMES,
        default=os.environ.get(ENV_OVH_API_ENDPOINT_NAME, None),
    )
    parser.add_argument(
        "--sms-ovh-app-key",
        metavar="SECRET",
        default=os.environ.get(ENV_OVH_API_APPLICATION_KEY, None),
    )
    parser.add_argument(
        "--sms-ovh-app-secret",
        metavar="SECRET",
        default=os.environ.get(ENV_OVH_API_APPLICATION_SECRET, None),
    )
    parser.add_argument(
        "--sms-ovh-consumer-key",
        metavar="SECRET",
        default=os.environ.get(ENV_OVH_API_CONSUMER_KEY, None),
    )
    parser.add_argument(
        "--sms-ovh-api-timeout",
        type=float,
        metavar="SEC",
        default=os.environ.get(
            ENV_GCN_OVH_API_TIMEOUT_SEC, DEFAULT_GCN_OVH_API_TIMEOUT_SEC
        ),
    )

    parser.add_argument(
        "--twitter-app-consumer-key",
        metavar="SECRET",
        default=os.environ.get(ENV_GCN_TWITTER_APP_CONSUMER_KEY, None),
    )
    parser.add_argument(
        "--twitter-app-consumer-secret",
        metavar="SECRET",
        default=os.environ.get(ENV_GCN_TWITTER_APP_CONSUMER_SECRET, None),
    )
    parser.add_argument(
        "--twitter-user-access-token",
        metavar="SECRET",
        default=os.environ.get(ENV_GCN_TWITTER_USER_ACCESS_TOKEN, None),
    )
    parser.add_argument(
        "--twitter-user-access-token-secret",
        metavar="SECRET",
        default=os.environ.get(ENV_GCN_TWITTER_USER_ACCESS_TOKEN_SECRET, None),
    )

    args = parser.parse_args()
    if args.print_env_then_exit:
        for key, value in sorted(os.environ.items()):
            print(f"{key}={value}")
        return

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(format="%(levelname)s %(message)s", level=log_level)
    logging.getLogger("asyncio").setLevel(log_level)

    # DO NOT log env/args, as they contain sensitive values pulled from environment variables

    setup_notification_recipients(args)

    if args.mqtt_host is None:
        raise AppError("MQTT host is required")
    if args.mqtt_port is None:
        raise AppError("MQTT port is required")

    try:
        asyncio.run(App.run(args))
    except KeyboardInterrupt:
        logging.info("Shutting down due to user interruption")


def main() -> None:
    try:
        main_trace()
    except AppError as e:
        logging.error(f"Application error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    if CLI_OPT_TRACE in sys.argv[1:]:
        main_trace()
    else:
        main()
