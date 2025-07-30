import asyncio
import itertools
import logging
import smtplib
import ssl
import time
from argparse import Namespace
from collections import deque
from datetime import datetime, timedelta
from email.message import EmailMessage
from enum import StrEnum
from typing import ClassVar, Self, Literal

import ovh
import phonenumbers
import tweepy.asynchronous
from phonenumbers import PhoneNumber
from pydantic import BaseModel, NameEmail, field_validator, ValidationError, Field

from gcn_manager import (
    ClientInfo,
    datetime_tz,
    AppError,
    NotificationError,
    datetime_system_tz,
)
from gcn_manager.constants import *

KNOWN_REGION_CODES = set(
    itertools.chain(
        *phonenumbers.phonenumberutil.COUNTRY_CODE_TO_REGION_CODE.values())
)


class Recipient:
    @classmethod
    def from_string(cls, value: str) -> Self:
        raise NotImplementedError()

    @classmethod
    def set_provider(cls, provider: "Provider") -> None:
        cls._PROVIDER = provider

    async def send_notification(self, notification: "Notification") -> None:
        logging.debug(
            f"Sending notification {repr(notification)} to {repr(self)}")
        if self._PROVIDER is None:
            logging.warning(
                f"No provider available for {self.__class__.__name__} for sending {notification.__class__}"
            )
            return
        await self._PROVIDER.send_notification_to_recipient(notification, self)


class EmailRecipient(Recipient, BaseModel):
    _PROVIDER: ClassVar["SmtpProvider"] = None

    address: NameEmail

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(**{"address": value})


class SmsRecipient(Recipient, BaseModel):
    class Config:
        arbitrary_types_allowed = True

    _PROVIDER: ClassVar["OvhSmsProvider"] = None
    RE_VALIDATOR_NUMBER_E164: ClassVar[re.Pattern] = re.compile(r"^\+[0-9]+$")
    number: phonenumbers.PhoneNumber

    # noinspection PyMethodParameters
    @field_validator("number", mode="before")
    def validate_number_e164(cls, value) -> PhoneNumber:
        """Expects https://en.wikipedia.org/wiki/E.164 ie. +123456..."""
        value = str(value)
        result = cls.RE_VALIDATOR_NUMBER_E164.fullmatch(value)
        if result is None:
            raise ValueError(
                f"Invalid international phone number {value} : should match "
                f"E.164 number regex {cls.RE_VALIDATOR_NUMBER_E164.pattern}"
            )
        try:
            result = phonenumbers.parse(result.group(0))
        except phonenumbers.NumberParseException as e:
            raise ValueError(
                f"Cannot parse {result.group(0)} phone number : {e}")
        if not phonenumbers.is_possible_number(result):
            raise ValueError(f"Impossible {result} phone number {value}")
        if not phonenumbers.is_valid_number(result):
            raise ValueError(f"Invalid {result} phone number {value}")
        return result

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(**{"number": value})


class TwitterRecipient(Recipient, BaseModel):
    _PROVIDER: ClassVar["TwitterProvider"] = None
    RE_VALIDATOR_USERNAME: ClassVar[re.Pattern] = re.compile(
        r"^@([A-Za-z0-9_]{4,15})$")

    username: str

    # noinspection PyMethodParameters
    @field_validator("username", mode="after")
    def validate_username(cls, value: str) -> str:
        result = cls.RE_VALIDATOR_USERNAME.fullmatch(value)
        if result is None:
            raise ValueError(
                f"Invalid Twitter/X username {value} : "
                f"should match python regex {cls.RE_VALIDATOR_USERNAME.pattern}"
            )
        return result.group(1)

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(**{"username": value})


class Notification(BaseModel):
    _RECIPIENT_CLASSES: ClassVar[tuple[Recipient, ...]] = (
        EmailRecipient,
        SmsRecipient,
        TwitterRecipient,
    )
    _RECIPIENTS: ClassVar[list[Recipient]] = list()

    moment: datetime = Field(default_factory=datetime_system_tz)

    @classmethod
    def set_recipients(cls, comma_separated_ids: str) -> None:
        cls._RECIPIENTS = list()
        logging.debug(
            f"Setting {cls.__name__} recipients from : {comma_separated_ids}")
        if comma_separated_ids is None:
            return
        tokens = set(
            token.strip()
            for token in comma_separated_ids.split(",")
            if len(token.strip()) > 0
        )
        for token in tokens:
            for try_class in cls._RECIPIENT_CLASSES:
                logging.debug(
                    f"Trying {try_class.__name__} recipients for {token}")
                try:
                    recipient = try_class.from_string(token)
                except ValidationError as e:
                    logging.debug(
                        f"Parsing recipient {token} did not succeed for {try_class.__name__}: "
                        f"{' '.join(str(e).splitlines())}"
                    )
                    continue
                logging.debug(
                    f"Adding {repr(recipient)} to recipient list for {try_class.__name__}"
                )
                cls._RECIPIENTS.append(recipient)
                break
            else:
                raise AppError(f"Could not detect recipient type from {token}")

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def to_raw_text(self) -> str:
        raise NotImplementedError()

    async def send(self) -> None:
        if len(self._RECIPIENTS) == 0:
            logging.debug(f"{self.__class__.__name__} has no recipients")
            return
        coro = [recipient.send_notification(self)
                for recipient in self._RECIPIENTS]
        results = await asyncio.gather(*coro, return_exceptions=True)
        success = errors = 0
        for recipient, result in zip(self._RECIPIENTS, results):
            if isinstance(result, Exception):
                errors += 1
                logging.warning(f"Error sending to {recipient} : {result=}")
            else:
                success += 1
                logging.debug(f"Success sending to {recipient} : {result=}")
        logging.info(
            f"{self.__class__.__name__} send report : {success} ok and {errors} failed"
        )


class ManagerStartingNotification(Notification):
    id: str

    def to_raw_text(self) -> str:
        return f"Manager {self.id} starting on {self.moment}"


class ManagerExitingNotification(Notification):
    id: str
    run_duration: timedelta

    def to_raw_text(self) -> str:
        return f"Manager {self.id} exiting on {self.moment} after running for {self.run_duration}"


class MqttStillConnectingNotification(Notification):
    id: str
    server: str
    elapsed_seconds: float

    def to_raw_text(self) -> str:
        return f"Manager {self.id} at {self.moment} still connecting to MQTT {self.server} after {self.elapsed_seconds} seconds"


class MqttConnectedNotification(Notification):
    id: str
    server: str

    def to_raw_text(self) -> str:
        return (
            f"Manager {self.id} connected to MQTT server {self.server} at {self.moment}"
        )


class MqttDisconnectedNotification(Notification):
    id: str
    server: str

    def to_raw_text(self) -> str:
        return f"Manager {self.id} disconnected from MQTT server {self.server} at {self.moment}"


class GcnHeartbeatSkewed(Notification):
    client: ClientInfo
    skew: float
    max_skew: float

    def to_raw_text(self) -> str:
        return (
            f"GCN client {self.client.id} ({self.client.status}) received heartbeat {self.client.heartbeat} "
            f"at {self.moment} skew {timedelta(seconds=self.skew)} from manager exceeds {self.max_skew} seconds"
        )


class GcnHeartbeatMissed(Notification):
    client: ClientInfo
    elapsed_seconds: float

    def to_raw_text(self) -> str:
        return (
            f"GCN client {self.client.id} ({self.client.status}) not received in the last {self.elapsed_seconds} "
            f"seconds, latest heartbeat {self.client.heartbeat} is {datetime_tz(self.client.heartbeat)} at {self.moment}"
        )


class GcnDroppedItems(Notification):
    client: ClientInfo

    def to_raw_text(self) -> str:
        return f"GCN client {self.client.id} dropped item reached {self.client.buffer_total_dropped_item} at {self.moment}"


class GcnStatusChangeOnline(Notification):
    client: ClientInfo

    def to_raw_text(self) -> str:
        return f"GCN client {self.client.id} status is {self.client.status} at {self.moment}"


class GcnStatusChangeOffline(Notification):
    client: ClientInfo

    def to_raw_text(self) -> str:
        return f"GCN client {self.client.id} status is {self.client.status} at {self.moment}"


class GcnGpioChangeUp(Notification):
    client: ClientInfo
    gpio_name: str

    def to_raw_text(self) -> str:
        return (
            f"GCN client {self.client.id} gpio {self.gpio_name} is UP at {self.moment}"
        )


class GcnGpioChangeDown(Notification):
    client: ClientInfo
    gpio_name: str

    def to_raw_text(self) -> str:
        return f"GCN client {self.client.id} gpio {self.gpio_name} is DOWN at {self.moment}"


class Provider:

    async def send_notification_to_recipient(
        self, notification: Notification, recipient: Recipient
    ) -> None:
        raise NotImplementedError()


class SmtpProvider(BaseModel, Provider):
    host: str
    port: int
    username: str | None = None
    password: str | None = None
    starttls: bool = False
    sender: NameEmail = None
    debug: bool = False
    timeout_sec: float = DEFAULT_GCN_EMAIL_SMTP_TIMEOUT_SEC
    disable_tls13: bool = False  # TODO: make configurable ?
    report_entries: deque | None = None

    def decode_response(self, response: bytes) -> str:
        try:
            return response.decode()
        except UnicodeDecodeError:
            raise NotificationError(
                f"Could not decode SMTP EHLO response from {self.host}:{self.port},"
                f"got {response=}"
            )

    def get_ehlo_parameters(self, smtp: smtplib.SMTP | smtplib.SMTP_SSL) -> list[str]:
        code, response = smtp.ehlo()
        if code != 250:
            raise NotificationError(
                f"Could not get SMTP EHLO from {self.host}:{self.port} "
                f"({code=}) : {response=}"
            )
        return self.decode_response(response).splitlines()

    def _get_ssl_context(self) -> ssl.SSLContext:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        if not self.disable_tls13:
            ssl_ctx.minimum_version = ssl.TLSVersion.TLSv1_3
        return ssl_ctx

    def _starttls(self, smtp: smtplib.SMTP | smtplib.SMTP_SSL) -> None:
        parameters = self.get_ehlo_parameters(smtp)
        if "STARTTLS" not in parameters:
            raise NotificationError(
                f"STARTTLS not advertised for SMTP {self.host}:{self.port}, "
                f"aborting to protect password : {parameters=}"
            )
        code, response = smtp.starttls(context=self._get_ssl_context())
        if code != 220:
            raise NotificationError(
                f"Could not STARTTLS for SMTP {self.host}:{self.port}, "
                f"aborting to protect password : {response=}"
            )

    def _authenticate(self, smtp: smtplib.SMTP | smtplib.SMTP_SSL) -> None:
        parameters = self.get_ehlo_parameters(smtp)
        for parameter in parameters:
            if parameter.startswith("AUTH "):
                break
        else:
            raise NotificationError(
                f"SMTP {self.host}:{self.port} does not support AUTH : {parameters=}"
            )
        code, response = smtp.login(self.username, self.password)
        if code != 235:
            raise NotificationError(
                f"Could not authenticate to SMTP {self.host}:{self.port} : {response=}"
            )

    def _send_message_starttls(self, message: EmailMessage, email_addr: str) -> None:
        logging.debug(
            f"Submitting to {self.host}:{self.port} with timeout={self.timeout_sec} using StartTLS"
        )
        with smtplib.SMTP(self.host, self.port, timeout=self.timeout_sec) as smtp:
            smtp.set_debuglevel(int(self.debug))
            self._starttls(smtp)
            self._authenticate(smtp)
            smtp.send_message(message, self.sender.email, email_addr)

    def _send_message_tls(self, message: EmailMessage, email_addr: str) -> None:
        logging.debug(
            f"Submitting to {self.host}:{self.port} with timeout={self.timeout_sec} using TLS"
        )
        with smtplib.SMTP_SSL(
            self.host,
            self.port,
            timeout=self.timeout_sec,
            context=self._get_ssl_context(),
        ) as smtp:
            smtp.set_debuglevel(int(self.debug))
            self._authenticate(smtp)
            smtp.send_message(message, self.sender.email, email_addr)

    async def send_notification_to_recipient(
        self, notification: Notification, recipient: EmailRecipient
    ) -> None:
        if not isinstance(recipient, EmailRecipient):
            raise NotificationError(
                f"Provider {self.__class__.__name__} only supports {EmailRecipient.__name__}"
            )
        text = notification.to_raw_text()
        if self.report_entries is not None:
            self.report_entries.append(text)
            text = "\n".join(reversed(self.report_entries))
        message = EmailMessage()
        message["Subject"] = (
            f"Notification for Brain/GCN : {notification.__class__.__name__} at {datetime_system_tz()}"
        )
        message["From"] = self.sender
        message["To"] = recipient.address
        message.set_content(text)
        try:
            await asyncio.to_thread(
                (
                    self._send_message_starttls
                    if self.starttls
                    else self._send_message_tls
                ),
                message,
                recipient.address.email,
            )
        except smtplib.SMTPException as e:
            raise NotificationError(
                f"Could not send {notification.__class__.__name__} to {recipient} "
                f"via SMTP {self.host}:{self.port}: {e}"
            )


class TwitterProvider(BaseModel, Provider):
    MAX_TEXT_LENGTH: ClassVar[int] = 280

    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str

    async def send_notification_to_recipient(
        self, notification: Notification, recipient: TwitterRecipient
    ) -> None:
        if not isinstance(recipient, TwitterRecipient):
            raise NotificationError(
                f"Provider {self.__class__.__name__} only supports {TwitterRecipient.__name__}"
            )
        try:
            client = tweepy.asynchronous.AsyncClient(**self.model_dump())
            text = notification.to_raw_text()
            if len(text) > self.MAX_TEXT_LENGTH + 1:
                logging.warning(
                    f"Twitter provider had to crop {notification.__class__.__name__} from "
                    f"{len(text)} to {self.MAX_TEXT_LENGTH} as it was too long"
                )
                text = text[0: self.MAX_TEXT_LENGTH]
            result: tweepy.Response = await client.create_tweet(
                text=text, user_auth=True
            )
            # Response is a namedtuple:
            # .data={'edit_history_tweet_ids': ['integer'], 'text': '...', 'id': 'integer'},
            # .includes={}
            # .errors=[]
            # .meta={})
            logging.debug(
                f"Posted tweet to twitter account with id {result.data['id']}"
            )
        except tweepy.errors.TooManyRequests as e:
            # you try to query more often than allowed
            raise NotificationError(
                f"Could not send {notification.__class__.__name__} to {recipient} : {e}"
            )
        except tweepy.errors.Forbidden as e:
            # Your client app is not configured with the appropriate oauth1 app permissions for this endpoint.
            # or you try to post longer tweets than you are allowed
            raise NotificationError(
                f"Could not send {notification.__class__.__name__} to {recipient} : {e}"
            )
        except tweepy.errors.TweepyException as e:
            raise NotificationError(
                f"Could not send {notification.__class__.__name__} to {recipient} : {e}"
            )


class OvhSmsEstimation(BaseModel):
    characters: int
    charactersClass: Literal["7bits", "unicode"]
    maxCharactersPerPart: int
    parts: int


class OvhSmsService(BaseModel):
    creditsLeft: int


class OvhSmsServiceStatus(StrEnum):
    AUTO_RENEW_IN_PROGRESS = "autorenewInProgress"
    EXPIRED = "expired"
    IN_CREATION = "inCreation"
    OK = "ok"
    PENDING_DEBT = "pendingDebt"
    UNPAID = "unPaid"


class OvhSmsServiceInfos(BaseModel):
    status: OvhSmsServiceStatus


class OvhSmsServiceUserQuotaStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class OvhSmsServiceUserQuota(BaseModel):
    quotaLeft: int
    quotaStatus: OvhSmsServiceUserQuotaStatus


class OvhSmsServiceUser(BaseModel):
    quotaInformations: OvhSmsServiceUserQuota
    ipRestrictions: list[str]


class OvhSmsServiceSenderStatus(StrEnum):
    ENABLE = "enable"
    DISABLE = "disable"
    REFUSED = "refused"
    WAITING_VALIDATION = "waitingValidation"


class OvhSmsServiceSenderType(StrEnum):
    ALPHA = "alpha"
    NUMERIC = "numeric"
    SHORT_CODE = "shortcode"
    VIRTUAL = "virtual"


class OvhSmsServiceSender(BaseModel):
    status: OvhSmsServiceSenderStatus
    type: OvhSmsServiceSenderType


class OvhSmsServiceUserIncomingId(BaseModel):
    creationDatetime: datetime
    credits: int
    id: int
    message: str
    sender: str
    tag: str


class OvhSmsServiceUserJob(BaseModel):
    creationDatetime: datetime
    credits: int
    deliveredAt: datetime | None
    deliveryReceipt: int
    differedDelivery: int  # 0
    id: int
    message: str
    messageLength: int
    numberOfSms: int
    ptt: int  # 1000
    receiver: str
    sender: str
    sentAt: datetime | None


class OvhSmsServiceUserJobPost(BaseModel):
    message: str
    sender: str
    receivers: list[str]
    charset: str = "UTF-8"
    coding: Literal["7bit", "8bit"] = "7bit"
    differedPeriod: int = 0  # minutes
    noStopClause: bool = True
    priority: Literal["high", "medium", "low", "veryLow"] = "medium"
    senderForResponse: bool = True
    tag: str | None = None
    validityPeriod: int = 60  # minutes


class OvhSmsServiceUserJobPostResult(BaseModel):
    validReceivers: list[str]  # E.164
    ids: list[int]
    totalCreditsRemoved: int
    tag: str


class OvhSmsProvider(BaseModel, Provider):
    api_sender_name: str
    api_service_name: str
    api_user_name: str
    api_endpoint: str
    api_app_key: str
    api_app_secret: str
    api_consumer_key: str
    api_timeout_sec: float
    allowed_region_codes: set[str] = KNOWN_REGION_CODES

    def _get_client(self) -> ovh.Client:
        return ovh.Client(
            endpoint=self.api_endpoint,
            application_key=self.api_app_key,
            application_secret=self.api_app_secret,
            consumer_key=self.api_consumer_key,
            timeout=self.api_timeout_sec,
        )

    @staticmethod
    def _check_time_skew(client: ovh.Client) -> None:
        current_time = client.get("/auth/time")  # unauthenticated
        try:
            current_time = int(current_time)  # possible ValueError
        except ValueError as e:
            raise Exception(f"Couldn't get current time from API: {e}")
        time_skew = abs(time.time() - current_time)
        if time_skew > OVH_API_MAX_TIME_SKEW:
            raise Exception(
                f"Time skew ({time_skew}) from host to OVH api "
                f"is greater than acceptable {OVH_API_MAX_TIME_SKEW}"
            )
        logging.debug(
            f"OVH api time skew compared to host is {time_skew} seconds")

    @staticmethod
    def _estimate_message(client: ovh.Client, text: str) -> OvhSmsEstimation:
        # stop clause = 11 characters
        # senderType: alpha|numeric|shortcode|virtual
        result = client.post(
            "/sms/estimate", message=text, noStopClause=True, senderType="alpha"
        )
        logging.debug(f"OVH api estimation result : {result}")
        return OvhSmsEstimation(**result)

    # todo: thread pool executor

    def _get_service(self, client: ovh.Client) -> OvhSmsService:
        result = client.get(f"/sms/{self.api_service_name}")
        logging.debug(f"OVH api service result : {result}")
        return OvhSmsService(**result)

    def _get_service_infos(self, client: ovh.Client) -> OvhSmsServiceInfos:
        result = client.get(f"/sms/{self.api_service_name}/serviceInfos")
        logging.debug(f"OVH api service infos result : {result}")
        return OvhSmsServiceInfos(**result)

    def _get_user(self, client: ovh.Client) -> OvhSmsServiceUser:
        result = client.get(
            f"/sms/{self.api_service_name}/users/{self.api_user_name}")
        logging.debug(f"OVH api service user result : {result}")
        return OvhSmsServiceUser(**result)

    def _get_sender(self, client: ovh.Client) -> OvhSmsServiceSender:
        result = client.get(
            f"/sms/{self.api_service_name}/senders/{self.api_sender_name}"
        )
        logging.debug(f"OVH api service sender result : {result}")
        return OvhSmsServiceSender(**result)

    def _get_incoming_ids(self, client: ovh.Client) -> list[int]:
        result = client.get(
            f"/sms/{self.api_service_name}/users/{self.api_user_name}/incoming"
        )
        logging.debug(f"OVH api service user incoming IDs result : {result}")
        return result

    def _get_incoming_id(
        self, client: ovh.Client, incoming_id: int
    ) -> OvhSmsServiceUserIncomingId:
        result = client.get(
            f"/sms/{self.api_service_name}/users/{self.api_user_name}/incoming/{incoming_id}"
        )
        logging.debug(
            f"OVH api service user incoming ID {incoming_id} result : {result}"
        )
        return OvhSmsServiceUserIncomingId(**result)

    def _get_jobs(self, client: ovh.Client) -> list[int]:
        result = client.get(
            f"/sms/{self.api_service_name}/users/{self.api_user_name}/jobs"
        )
        logging.debug(f"OVH api service user jobs : {result}")
        return result

    def _get_job(self, client: ovh.Client, job_id: int) -> OvhSmsServiceUserJob:
        result = client.get(
            f"/sms/{self.api_service_name}/users/{self.api_user_name}/jobs/{job_id}"
        )
        logging.debug(
            f"OVH api service user job ID {job_id} result : {result}")
        return result

    def _post_job(
        self, client: ovh.Client, post: OvhSmsServiceUserJobPost
    ) -> OvhSmsServiceUserJobPostResult:
        result = client.post(
            f"/sms/{self.api_service_name}/users/{self.api_user_name}/jobs",
            **post.model_dump(),
        )
        logging.debug(
            f"OVH api service user post job ID {post} result : {result}")
        return OvhSmsServiceUserJobPostResult(**result)

    def _check_recipient_country(self, number: PhoneNumber) -> None:
        number_region_codes = set(
            phonenumbers.region_codes_for_country_code(number.country_code)
        )
        unauthorized_region_codes = number_region_codes.difference(
            self.allowed_region_codes
        )
        if len(unauthorized_region_codes) > 0:
            raise NotificationError(
                f"Refusing to send SMS to unauthorized region codes : {unauthorized_region_codes}"
            )

    def _send_notification_to_recipient(
        self, notification: Notification, recipient: SmsRecipient
    ) -> None:
        client = self._get_client()
        # verifications
        self._check_time_skew(client)
        service = self._get_service(client)
        # todo: raise provider resource error and trigger another (email?) notification if present
        if service.creditsLeft == 0:
            raise NotificationError(
                f"OVH api service {self.api_service_name} does not have any credit left"
            )
        if service.creditsLeft < 3:
            logging.warning(
                f"OVH api service {self.api_service_name} has only {service.creditsLeft} credits left"
            )
        else:
            logging.info(
                f"OVH api service {self.api_service_name} has {service.creditsLeft} credits left"
            )
        service_infos = self._get_service_infos(client)
        if service_infos.status != OvhSmsServiceStatus.OK:
            raise NotificationError(
                f"OVH api service {self.api_service_name} has status "
                f"{service_infos.status}, should be {OvhSmsServiceStatus.OK}"
            )
        user = self._get_user(client)
        if user.quotaInformations.quotaStatus != OvhSmsServiceUserQuotaStatus.ACTIVE:
            raise NotificationError(
                f"OVH api service {self.api_service_name} user {self.api_user_name} "
                f"has quota status {user.quotaInformations.quotaStatus}, "
                f"should be {OvhSmsServiceUserQuotaStatus.ACTIVE}"
            )
        if user.quotaInformations.quotaLeft == 0:
            raise NotificationError(
                f"OVH api service {self.api_service_name} user {self.api_user_name} "
                f"does not have any quota left"
            )
        if user.quotaInformations.quotaLeft < 3:
            logging.warning(
                f"OVH api service {self.api_service_name} user {self.api_user_name} "
                f"has only {user.quotaInformations.quotaLeft} quota left"
            )
        else:
            logging.info(
                f"OVH api service {self.api_service_name} user {self.api_user_name} "
                f"has {user.quotaInformations.quotaLeft} quota left"
            )
        sender = self._get_sender(client)
        if sender.status != OvhSmsServiceSenderStatus.ENABLE:
            raise NotificationError(
                f"OVH api service {self.api_service_name} sender {self.api_sender_name} "
                f"has sender status {sender.status}, "
                f"should be {OvhSmsServiceSenderStatus.ENABLE}"
            )
        if sender.type != OvhSmsServiceSenderType.ALPHA:
            raise NotificationError(
                f"OVH api service {self.api_service_name} sender {self.api_sender_name} "
                f"has sender type {sender.type}, "
                f"should be {OvhSmsServiceSenderType.ALPHA}"
            )
        # incoming
        incoming_ids = self._get_incoming_ids(client)
        for incoming_id in incoming_ids:
            incoming = self._get_incoming_id(client, incoming_id)
            logging.critical(f"Incoming message: {incoming}")
        # TODO: incoming messages do not get automatically deleted, delete them manually
        # jobs
        job_ids = self._get_jobs(client)
        for job_id in job_ids:
            job = self._get_job(client, job_id)
            logging.critical(f"Job : {job}")  # TODO: do something better
        # notify
        text = notification.to_raw_text()
        estimation = self._estimate_message(client, text)
        if estimation.charactersClass != "7bits":
            raise NotificationError(
                f"Refusing to send SMS notification that are not 7-bit characters, "
                f"{estimation=} for text : {text.encode('utf-8')}"
            )
        if estimation.parts > 1:
            raise NotificationError(
                f"Refusing to send more than one SMS per notification, "
                f"{estimation=} for text : {text.encode('utf-8')}"
            )

        # post
        self._check_recipient_country(recipient.number)
        receivers = [
            phonenumbers.format_number(
                recipient.number, phonenumbers.PhoneNumberFormat.E164
            )
        ]
        post = OvhSmsServiceUserJobPost(
            sender=self.api_sender_name, receivers=receivers, message=text
        )
        result = self._post_job(client, post)

        # track returned job ids until they all disappear (complete)
        retry_http_errors = 5
        while len(result.ids) > 0:
            time.sleep(1)
            jobs: dict[int, OvhSmsServiceUserJob] = dict()
            found_job_ids = []
            for job_id in result.ids:
                try:
                    job = self._get_job(client, job_id)
                except ovh.ResourceNotFoundError:
                    logging.debug(
                        f"SMS job {job_id} not found (i.e. should have completed)"
                    )
                    continue
                except ovh.HTTPError as e:
                    logging.warning(
                        f"HTTP error while getting job {job_id} ({retry_http_errors} retries left) : {e}"
                    )
                    retry_http_errors -= 1
                    if retry_http_errors > 0:
                        continue
                    raise
                found_job_ids.append(job_id)
                # FIXME: unnecessary except for debugging (and untested as job disappears upon sending) ?
                try:
                    previous_job = jobs[job_id]
                except KeyError:
                    previous_job = job
                if previous_job != job:
                    logging.critical(
                        f"Job {job_id} updated : {previous_job} -> {job}")
                jobs[job_id] = job
            # update until completion
            result.ids = found_job_ids

    async def send_notification_to_recipient(
        self, notification: Notification, recipient: SmsRecipient
    ) -> None:
        try:
            await asyncio.to_thread(
                self._send_notification_to_recipient, notification, recipient
            )
        except ovh.HTTPError as e:
            raise NotificationError(f"Could not connect to OVH api : {e}")
        except ovh.InvalidKey as e:
            raise NotificationError(f"Could query OVH sms api : {e}")
        except ovh.ResourceNotFoundError as e:
            raise NotificationError(f"OVH sms api resource not found: {e}")
        except ovh.APIError as e:
            raise NotificationError(f"OVH sms api error: {e}")


def setup_notification_recipients(args: Namespace) -> None:
    ManagerStartingNotification.set_recipients(
        args.notify_manager_starting_recipients)
    MqttStillConnectingNotification.set_recipients(
        args.notify_manager_still_connecting_recipients
    )
    MqttConnectedNotification.set_recipients(
        args.notify_manager_connected_recipients)
    MqttDisconnectedNotification.set_recipients(
        args.notify_manager_disconnected_recipients
    )
    ManagerExitingNotification.set_recipients(
        args.notify_manager_exiting_recipients)
    GcnHeartbeatSkewed.set_recipients(
        args.notify_client_skewed_heartbeat_recipients)
    GcnHeartbeatMissed.set_recipients(
        args.notify_client_missed_heartbeat_recipients)
    GcnDroppedItems.set_recipients(args.notify_client_dropped_items_recipients)
    GcnStatusChangeOnline.set_recipients(
        args.notify_client_status_change_online_recipients
    )
    GcnStatusChangeOffline.set_recipients(
        args.notify_client_status_change_offline_recipients
    )
    GcnGpioChangeUp.set_recipients(
        args.notify_client_gpio_change_up_recipients)
    GcnGpioChangeDown.set_recipients(
        args.notify_client_gpio_change_down_recipients)

    if not args.enable_email_notifications:
        logging.info("Email notifications disabled")
    else:
        smtp_config = {
            "host": args.email_smtp_host,
            "port": args.email_smtp_port,
            "username": args.email_username,
            "password": args.email_password,
            "starttls": args.email_smtp_starttls,
            "sender": args.email_from,
            "debug": args.email_smtp_debug,
            "disable_tls13": args.email_smtp_disable_tls13,
            "report_entries": deque() if args.email_smtp_send_as_report else None,
            "timeout_sec": args.email_smtp_timeout,
        }
        try:
            provider = SmtpProvider(**smtp_config)
        except ValidationError as e:
            raise AppError(
                f"Could not configure SMTP : {' '.join(str(e).splitlines())}"
            )
        EmailRecipient.set_provider(provider)

    if not args.enable_sms_notifications:
        logging.info("SMS notifications disabled")
    else:
        allowed_region_codes = KNOWN_REGION_CODES
        if args.sms_allow_country is not None:
            allowed_region_codes = set(
                c.strip().upper()
                for c in args.sms_allow_country.split(",")
                if len(c.strip()) > 0
            )
            if len(allowed_region_codes) == 0:
                raise AppError(
                    f"A least one country code must be allowed when SMS notification is enabled"
                )
            refused_codes = allowed_region_codes.difference(KNOWN_REGION_CODES)
            if len(refused_codes) > 0:
                raise AppError(
                    f"These country codes are unknown from phonenumbers : {', '.join(refused_codes)}"
                )
        ovh_sms_config = {
            "allowed_region_codes": allowed_region_codes,
            "api_sender_name": args.sms_ovh_sender_name,
            "api_service_name": args.sms_ovh_service_name,
            "api_user_name": args.sms_ovh_user_name,
            "api_endpoint": args.sms_ovh_endpoint,
            "api_app_key": args.sms_ovh_app_key,
            "api_app_secret": args.sms_ovh_app_secret,
            "api_consumer_key": args.sms_ovh_consumer_key,
            "api_timeout_sec": args.sms_ovh_api_timeout,
        }
        try:
            provider = OvhSmsProvider(**ovh_sms_config)
        except ValidationError as e:
            raise AppError(
                f"Could not configure SMS : {' '.join(str(e).splitlines())}")
        SmsRecipient.set_provider(provider)

    if not args.enable_twitter_notifications:
        logging.info("Twitter notifications disabled")
    else:
        twitter_config = {
            "consumer_key": args.twitter_app_consumer_key,
            "consumer_secret": args.twitter_app_consumer_secret,
            "access_token": args.twitter_user_access_token,
            "access_token_secret": args.twitter_user_access_token_secret,
        }
        try:
            provider = TwitterProvider(**twitter_config)
        except ValidationError as e:
            raise AppError(
                f"Could not configure Twitter/X : {' '.join(str(e).splitlines())}"
            )
        TwitterRecipient.set_provider(provider)
