# type: ignore
import asyncio
import weakref


try:
    import nats
    _HAVE_NATS = True
except ModuleNotFoundError:
    _HAVE_NATS = False
else:
    import nats.errors
    import nats.aio.msg
    import nats.js.client
    import nats.aio.client
    import nats.aio.subscription
    from yarl import URL

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from datetime import datetime, timedelta
from collections import deque

from typing_extensions import Self

from communica.utils import (
    NULL_CHAR,
    HasLoopMixin,
    json_dumpb,
    json_loadb,
    exc_log_callback,
)
from communica.connectors.base import (
    Handshaker,
    BaseConnector,
    HandshakeFail,
    BaseConnection,
    ClientConnectedCB,
    RequestReceivedCB,
)


_DEFAULT_PREFIX = 'communica'


class _MessageType(str, Enum):
    CONNECT_REQUEST = 'communica_client_connect'
    CONNECT_RESPONSE = 'communica_client_connect_ok'

    HS_NEXT = 'communica_handshake_next'
    HS_FAIL = 'communica_handshake_fail'
    HS_DONE = 'communica_handshake_done'

    CLOSE = 'close'
    MESSAGE = 'message'
    LISTENING = 'listening'


_clients: '''dict[
    tuple[asyncio.AbstractEventLoop, tuple[str, ...]],
    nats.aio.client.Client | asyncio.Future[nats.aio.client.Client]
]''' = {}


def _not_ready_exceptions():
    return (  # XXX: по семантике первое от второго и третьего слишком отличается
        nats.errors.ConnectionClosedError,  # pyright: ignore[reportUnboundVariable]
        nats.errors.ConnectionDrainingError,  # pyright: ignore[reportUnboundVariable]
        nats.errors.ConnectionReconnectingError  # pyright: ignore[reportUnboundVariable]
    )


async def _publish(
        client: 'nats.aio.client.Client | nats.js.client.JetStreamContext',
        msg_type: str,
        subject: str,
        body: 'bytes' = b'',
        reply: 'str | None' = None
):
    print('PUB', msg_type, body)
    headers = {'message_type': msg_type}
    if reply:
        headers['reply'] = reply
    return await client.publish(
        subject=subject,
        payload=body,
        headers=headers
    )


class Message:
    __slots__ = ('msg')

    def __init__(self, msg: 'nats.aio.msg.Msg') -> None:
        self.msg = msg

    @property
    def body(self) -> bytes:
        return self.msg.data

    @property
    def type(self) -> str:
        return self.msg.headers['message_type']  # type: ignore

    @property
    def reply(self) -> 'str | None':
        return self.msg.headers.get('reply')  # type: ignore



class MessageWaiter(HasLoopMixin):
    __slots__ = ('_waiter', '_messages', '_timeout', '_subscription')

    _waiter: 'asyncio.Future[Message] | None'
    _timeout: 'float | None'
    _messages: 'deque[Message]'
    _subscription: 'nats.aio.subscription.Subscription'

    @classmethod
    async def new(
            cls,
            client: 'nats.aio.client.Client | nats.js.client.JetStreamContext',
            subject: str,
            *,
            no_ack: bool = False, # XXX
            timeout: 'float | None' = None
    ):
        inst = cls()
        inst._waiter = None
        inst._timeout = timeout
        inst._messages = deque()

        inst._subscription = \
            await client.subscribe(subject, cb=inst._callback)

        return inst

    async def _callback(self, message: 'nats.aio.msg.Msg'):
        print('GOT', message.header, message.data)

        if not self._waiter or self._waiter.done():
            self._messages.append(Message(message))
        else:
            self._waiter.set_result(Message(message))
            self._waiter = None

    def set_timeout_duration(self, timeout: int):
        if self._waiter and not self._waiter.done():
            raise RuntimeError('Waiter not completed')
        self._timeout = timeout

    def _set_timeout(self, fut: asyncio.Future):
        if not fut.done():
            fut.set_exception(asyncio.TimeoutError)

    def interrupt(self):
        if self._waiter:
            self._waiter.set_exception(asyncio.TimeoutError)

    async def unsubscribe(self):
        await self._subscription.unsubscribe()

    async def wait(self) -> 'Message':
        if self._messages:
            return self._messages.popleft()

        if self._waiter and not self._waiter.done():
            raise RuntimeError(f'Duplicate .wait() call on {self!r}')

        self._waiter = self._get_loop().create_future()

        if self._timeout:
            self._get_loop().call_later(
                self._timeout, self._set_timeout, self._waiter)

        return await self._waiter


class ConnectionCheckPolicy(HasLoopMixin, ABC):
    period: float
    _handle: 'asyncio.TimerHandle | None'

    def message_sent(self):
        pass

    def message_received(self):
        pass

    @abstractmethod
    def _trigger(self):
        raise NotImplementedError

    @abstractmethod
    def _cancel(self):
        raise NotImplementedError

    @abstractmethod
    def replace_conn(self, conn: 'NATSConnection') -> Self:
        raise NotImplementedError

    def _set_handle(self, period: 'float | None' = None):
        if period is None:
            self._last_message = self._get_loop().time()
            period = self.period
        self._handle = self._get_loop().call_later(period, self._trigger)


class ServerCheckPolicy(ConnectionCheckPolicy):
    def __init__(self, conn: 'NATSConnection', period: float) -> None:
        self._get_loop()

        self.period = period
        self._waiter = self._get_loop().create_future()

        self._set_handle()

        self._send_task = self._get_loop().create_task(self._sender())
        self._send_task.add_done_callback(exc_log_callback)
        self._conn = weakref.ref(conn, self._conn_died)

    def replace_conn(self, conn: 'NATSConnection'):
        conn._check_policy._cancel()
        self._conn = weakref.ref(conn, self._conn_died)
        return self

    def _cancel(self):
        if self._handle is not None:
            self._handle.cancel()
        self._conn_died(None)

    def _conn_died(self, _):
        if not self._waiter.done():
            self._waiter.set_result(False)

    def _trigger(self):
        if self._waiter.done():
            return

        time_diff = self._get_loop().time() - self._last_message
        if time_diff < self.period:
            self._set_handle(self.period - time_diff)
            return

        self._handle = None
        self._waiter.set_result(True)
        self._waiter = self._get_loop().create_future()

    async def _sender(self):
        while (await self._waiter):
            if (conn := self._conn()) is None:
                return
            await conn._send(_MessageType.LISTENING, b'')
            del(conn)  # deleting reference
            if self._handle is None:
                self._set_handle()

    def message_sent(self):
        if self._handle is None:
            self._set_handle()
        else:
            self._last_message = self._get_loop().time()


class ClientCheckPolicy(ConnectionCheckPolicy):
    def __init__(self, conn: 'NATSConnection', period: float) -> None:
        self._get_loop()

        self.period = period
        self._set_handle()

        self._conn = weakref.ref(conn)
        self._close_task = None

    def replace_conn(self, conn: 'NATSConnection'):
        conn._check_policy._cancel()
        self._conn = weakref.ref(conn)
        return self

    def _cancel(self):
        if self._handle is not None:
            self._handle.cancel()

    def _trigger(self):
        if (conn := self._conn()) is None or not conn.is_alive:
            return

        time_diff = self._get_loop().time() - self._last_message
        if time_diff < self.period:
            self._set_handle(self.period - time_diff)
            return

        self._close_task = self._get_loop().create_task(conn.close())

    def message_received(self):
        if self._close_task is None:
            self._last_message = self._get_loop().time()


class NATSConnection(BaseConnection):
    __slots__ = ('_connector', '_js_context', '_ready', '_closing',
                 '_recv_subject', '_send_subject', '_check_policy',
                 '_message_waiter', '__weakref__')

    _ready: asyncio.Event
    _closing: 'asyncio.Future | None'
    _connector: 'NATSConnector'
    _js_context: 'nats.js.client.JetStreamContext'
    _message_waiter: 'MessageWaiter | None'

    @property
    def is_alive(self):
        return self._ready.is_set()

    @classmethod
    async def _do_handshake_and_create_connection(
            cls,
            js_context: 'nats.js.client.JetStreamContext',
            connector: 'NATSConnector',
            handshaker: Handshaker,
            resp_waiter: MessageWaiter,
            send_subject: str
    ) -> Self:
        inst = cls()

        async def send_message(data: bytes):
            await _publish(
                js_context,
                msg_type=_MessageType.HS_NEXT,
                body=data,
                subject=send_subject
            )

        async def recv_message():
            message = await resp_waiter.wait()
            if message.type == _MessageType.HS_FAIL:
                raise HandshakeFail.loadb(message.body)
            elif message.type != _MessageType.HS_NEXT:
                raise ValueError('Unknown message on handshake subject')
            return message.body

        try:
            await inst._run_handshaker(handshaker, send_message, recv_message)
        except HandshakeFail as fail:
            await _publish(
                js_context,
                msg_type=_MessageType.HS_FAIL,
                body=fail.dumpb(),
                subject=send_subject
            )
            raise

        inst._ready = asyncio.Event()
        inst._ready.set()
        inst._closing = None
        inst._connector = connector
        inst._js_context = js_context
        inst._message_waiter = None

        return inst

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        if self._ready:
            state = f'on {self._js_context}'
        else:
            state = 'not ready'
        return f'<{cls_name} {state}>'

    def _set_run_data(
            self,
            policy: ConnectionCheckPolicy,
            recv_subject: str,
            send_subject: str
    ):
        self._check_policy = policy
        self._recv_subject, self._send_subject = recv_subject, send_subject

    def update(self, connection: Self) -> None:
        if self._connector._connect_id != connection._connector._connect_id:
            raise ValueError('Got connection with different connect_id')
        # if connection._js_context.:
            raise ValueError('Got connection with closed client')

        self._ready.set()
        self._closing = None
        self._js_context = connection._js_context
        self._check_policy = connection._check_policy.replace_conn(self)

    async def send(self, metadata: Any, raw_data: bytes):
        body = json_dumpb(metadata) + NULL_CHAR + raw_data
        try:
            await self._send(_MessageType.MESSAGE, body)
        except _not_ready_exceptions():
            self._ready.clear()
            await self._send(_MessageType.MESSAGE, body)  # retry once after channel opened
        # except aiormq.exceptions.AMQPError:
        #     self._ready.clear()
        #     raise
        self._check_policy.message_sent()

    async def _send(self, msg_type: _MessageType, body: bytes):
        await self._ready.wait()
        await _publish(
            self._js_context,
            msg_type=msg_type,
            body=body,
            subject=self._send_subject
        )

    async def run_until_fail(
            self,
            request_received_cb: RequestReceivedCB
    ) -> None:
        self._message_waiter = await MessageWaiter.new(
            self._js_context,
            self._recv_subject,
            no_ack=False
        )
        try:
            await self._run_until_fail(request_received_cb)
        except asyncio.TimeoutError:
            return
        finally:
            self._message_waiter = None
            self._ready.clear()

    async def _run_until_fail(self, request_received_cb):
        while self._message_waiter:
            message = await self._message_waiter.wait()

            self._check_policy.message_received()

            if message.type == _MessageType.MESSAGE:
                null_pos = message.body.find(NULL_CHAR)
                if null_pos == -1:
                    # await ack_message(message)
                    await self._close(True)
                    raise ValueError('Got message without metadata separator')

                metadata = json_loadb(message.body[:null_pos])
                request_received_cb(metadata, message.body[null_pos+1:])
                # await ack_message(message)

            elif message.type == _MessageType.LISTENING:
                # await ack_message(message)
                continue

            elif message.type == _MessageType.CLOSE:
                # await ack_message(message)
                await self._close(False)
                return

            else:
                # await ack_message(message)
                await self._close(True)
                raise ValueError('Unknown message on message subject, '
                                f'got type {message.type!r}')

    async def close(self) -> None:
        await self._close(True)

    async def _close(self, send_close_request: bool):
        if self._closing:
            return await self._closing

        if not self._ready.is_set():
            return

        self._ready.clear()

        if self._message_waiter:
            self._message_waiter.interrupt()
            self._message_waiter = None

        if self._js_context.is_closed:
            return

        self._closing = asyncio.get_running_loop().create_future()
        try:
            if send_close_request:
                await _publish(
                    self._js_context,
                    msg_type=_MessageType.CLOSE,
                    subject=self._send_subject
                )
        except _not_ready_exceptions() + (asyncio.CancelledError,):
            return
        finally:
            await self._connector._check_connection_use()
            self._closing.set_result(None)


class NATSServer(asyncio.AbstractServer):
    @property
    def exchange(self):
        return self._connector._exchange

    def __init__(
            self,
            connector: 'NATSConnector',
            nats_client: 'nats.aio.client.Client',
            handshaker: Handshaker,
            client_connected_cb: ClientConnectedCB
    ) -> None:
        self._closing = None
        self._connector = connector
        self._handshaker = handshaker
        self._nats_client = nats_client
        self._client_connected_cb = client_connected_cb

    def is_serving(self):
        """Return True if the server is accepting connections."""
        return not self._nats_client.is_closed

    def close(self):
        async def close_channel():
            # ну типа надо придумать
            return

        if not self._closing or self._closing.done():
            self._closing = asyncio.create_task(close_channel())

    async def wait_closed(self):
        if not self._closing or self._closing.done():
            raise RuntimeError('wait_closed() should be '
                               'called right after close() method')
        await self._closing

    async def _on_connect(self, raw_message: 'nats.aio.msg.Msg'):
        message = Message(raw_message)

        if message.type != _MessageType.CONNECT_REQUEST:
            # await self._connector._ack_message(self._chan, message)
            raise ValueError('Unknown message on connect request subject')

        if message.reply is None:
            # await self._connector._ack_message(self._chan, message)
            raise ValueError('Reply subject not specified in connect request')

        hs_to_cli_subject = message.reply
        connect_id = json_loadb(message.body)

        hs_to_srv_subject = self._nats_client.new_inbox()

        await _publish(
            self._nats_client,
            msg_type=_MessageType.CONNECT_RESPONSE,
            subject=hs_to_cli_subject,
            reply=hs_to_srv_subject
        )

        # await self._connector._ack_message(self._chan, message)

        resp_waiter = await MessageWaiter.new(
            self._nats_client,
            hs_to_srv_subject,
            no_ack=True,
            timeout=10
        )

        try:
            conn = await NATSConnection._do_handshake_and_create_connection(
                self._nats_client,
                self._connector,
                self._handshaker,
                resp_waiter,
                hs_to_cli_subject
            )
        except HandshakeFail:
            return
        finally:
            if not self._nats_client.is_closed:
                await resp_waiter.unsubscribe()

        to_cli_subject, to_srv_subject = \
            self._connector._get_transport_subject_names(connect_id)

        await _publish(
            self._nats_client,
            msg_type=_MessageType.HS_DONE,
            subject=hs_to_cli_subject
        )

        policy = \
            ServerCheckPolicy(conn, self._connector.CONNECTION_CHECK_PERIOD)
        conn._set_run_data(policy, to_srv_subject, to_cli_subject)

        self._client_connected_cb(conn)

    async def start_serving(self):
        subject_name = self._connector._get_connect_subject_name()
        await self._nats_client.subscribe(subject_name, cb=self._on_connect)

    def get_loop(self):
        raise NotImplementedError

    async def serve_forever(self):
        raise NotImplementedError


class NATSConnector(BaseConnector):
    """
    Uses RabbitMQ for communication. Theoretically can be used
    with any AMQP-compatible server, but this wasn't tested.

    WARNING:
        For this connector to work properly, only one client
        with same address and connect_id must be connected at same time.

        For those, who connect, connect_id must be set explicitly
        and persist between service restarts.

        Failure to comply with these rules
        leads to unclosed subjects growth and message loss.
    """

    _TYPE = 'RABBITMQ'

    CONNECTION_CHECK_PERIOD = 20
    """every X seconds server sends message to client,
    if client did not got any message in (this period * 1.5),
    it closes connection"""

    __slots__ = ('_urls', '_address', '_connect_id',
                 '_exchange', '_exchange_declared')

    @property
    def exchange(self):
        return self._exchange

    def __init__(
            self,
            urls: 'str | list[str]',
            address: str,
            connect_id: 'str | None' = None,
    ) -> None:
        """
        Max summary length of address and connect_id is 224 characters

        Args:
            urls (str): used to create connection with NATS servers.
              Format specified at https://www.rabbitmq.com/uri-spec.html.
            address (str): unique identifier for client-server pair.
              If more than one server with same address bound to same exchange,
              behaviour undefined.
            connect_id (str): unique identifier of connecting process.
              Must be set for clients.
        """
        if not _HAVE_NATS:
            raise ImportError('NATSConnector requires nats library. '
                              'Install communica with [nats] extra.')

        if connect_id is not None and len(address + connect_id) > 224:
            raise ValueError('Max address + connect_id length is 224 characters')

        if isinstance(urls, str):
            urls = [urls]
        self._urls = tuple(urls)
        self._address = address
        self._connect_id = connect_id

    def _get_connect_subject_name(self):
        return self._fmt_subject_name('connect', 'server')

    def _get_transport_subject_names(self, connect_id: str):
        return (
            self._fmt_subject_name('toClient', connect_id),
            self._fmt_subject_name('toServer', connect_id)
        )

    def _fmt_subject_name(self, *parts):
        return f'communica.{self._address}.' + '.'.join(parts)

    def repr_address(self) -> str:
        urls: 'list[URL]' = []
        for raw_url in self._urls:
            url = URL(raw_url)
            if url.password is not None:
                url = url.with_password("[PASSWORD]")
            urls.append(url)
        return ','.join([url.human_repr() for url in urls])

    async def server_start(
            self,
            handshaker: Handshaker,
            client_connected_cb: ClientConnectedCB,
    ) -> asyncio.AbstractServer:
        nats_client = await self._get_client()

        server = NATSServer(self, nats_client, handshaker, client_connected_cb)
        await server.start_serving()
        return server

    async def _client_connect(
            self,
            handshaker: Handshaker,
            nats_client: 'nats.aio.client.Client'
    ):
        hs_to_cli_subject = nats_client.new_inbox()

        await _publish(
            nats_client,
            msg_type=_MessageType.CONNECT_REQUEST,
            body=json_dumpb(self._connect_id),
            subject=self._get_connect_subject_name(),
            reply=hs_to_cli_subject
        )

        resp_waiter = \
            await MessageWaiter.new(nats_client, hs_to_cli_subject, no_ack=True)

        message = await resp_waiter.wait()
        if message.type != _MessageType.CONNECT_RESPONSE:
            raise ValueError('Unknown message on connect response subject')

        if message.reply is None:
            raise ValueError('Server subject not specified in connect response')
        hs_to_srv_subject = message.reply

        resp_waiter.set_timeout_duration(10)

        try:
            conn = await NATSConnection._do_handshake_and_create_connection(
                nats_client,
                self,
                handshaker,
                resp_waiter,
                hs_to_srv_subject
            )
        except Exception:
            if nats_client.is_connected:
                await resp_waiter.unsubscribe()
            raise

        message = await resp_waiter.wait()
        await resp_waiter.unsubscribe()

        if message.type != _MessageType.HS_DONE:
            raise ValueError(f'Got message with "{message.type}" type '
                              'instead of handshake confirmation')

        to_cli_subject, to_srv_subject = \
            self._get_transport_subject_names(self._connect_id)  # type: ignore
        policy = ClientCheckPolicy(conn, self.CONNECTION_CHECK_PERIOD * 1.5)
        conn._set_run_data(policy, to_cli_subject, to_srv_subject)

        return conn

    async def client_connect(self, handshaker: Handshaker) -> BaseConnection:
        if self._connect_id is None:
            raise TypeError('Cannot connect to server. For those, who connect, '
                            'connect_id parameter must be set. '
                            'Check NATSConnector docs for details.')

        client = await self._get_client()
        return await self._client_connect(handshaker, client)

    async def cleanup(self):
        """
        Drop all pending messages and
        delete subjects with connector's connect_id

        If connect_id is None, noop
        """
        return

    def dump_state(self) -> str:
        """Unsupported for this connector"""
        raise TypeError('This method unsupported cause user and password '
                        'are not encrypted in dump, which is insecure')

    @classmethod
    def from_state(cls, state: str) -> Self:
        """Unsupported for this connector"""
        raise TypeError('This method unsupported cause user and password '
                        'are not encrypted in dump, which is insecure')

    async def _ack_message(self, nats_client, message):
        await nats_client.basic_ack(message.delivery_tag)

    async def _get_client(self):
        key = (asyncio.get_running_loop(), self._urls)

        if (client := _clients.get(key)) is None:
            fut = asyncio.get_running_loop().create_future()
            _clients[key] = fut
            try:
                client = await nats.connect(list(self._urls))
            except Exception as e:
                fut.set_exception(e)
                del(_clients[key])
                raise
            else:
                fut.set_result(client)
                _clients[key] = client

        elif isinstance(client, asyncio.Future):
            client = await client

        elif client.is_closed:
            del(_clients[key])
            return await self._get_client()

        return client

    async def _check_connection_use(self):
        return  # закрытие соединения, если оно больше никому не нужно
