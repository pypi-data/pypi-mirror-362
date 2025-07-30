"""Unit tests for server utilities."""

from datetime import datetime
from logging import DEBUG
from socket import AF_UNIX, SOCK_STREAM, socket
from unittest.mock import MagicMock

import pytest
from openpgpcard_x25519_agent.cnf import DEFAULT_SOCKET
from openpgpcard_x25519_agent.msg import (
    ADD_SMARTCARD_KEY,
    ADD_SMARTCARD_KEY_CONSTRAINED,
    DERIVE_SHARED_SECRET,
    FAILURE,
    REMOVE_SMARTCARD_KEY,
    REQUEST_EXTENSION,
    REQUEST_PUBLIC_KEY,
    SUCCESS,
    Message,
)
from openpgpcard_x25519_agent.server import Seat, Server, run_server
from OpenPGPpy import PGPCardException

EXAMPLE_KEY_HEX = "C53201039ADBA14BE71F886DA1D8DBE9EEBDED08CB111B75340078999AA9F038"
TEST_KDF_DO = "81 01 03 82 01 08 83 04 00000001 84 08 7465737473616C74"
TEST_KDF_FOO = "22519901F545BE8C8E52F0F80BEDFF2C5BABAA63564B1DF34FC376F897011F2B"


def test_run_server_when_defaults(mocker):
    mocker.patch("openpgpcard_x25519_agent.server.signal")
    server_mock = mocker.patch("openpgpcard_x25519_agent.server.Server")

    run_server()

    assert server_mock.call_args.args[0] == DEFAULT_SOCKET
    seats = server_mock.call_args.args[1]
    assert len(seats) == 1
    assert not seats[0].id
    assert not seats[0].pin


def test_run_server_when_socket_path_and_card_id(mocker):
    mocker.patch("openpgpcard_x25519_agent.server.signal")
    server_mock = mocker.patch("openpgpcard_x25519_agent.server.Server")

    run_server("test.sock", "123")

    assert server_mock.call_args.args[0] == "test.sock"
    seats = server_mock.call_args.args[1]
    assert len(seats) == 1
    assert seats[0].id == "123"
    assert not seats[0].pin


def test_run_server_when_file_descriptor(mocker):
    mocker.patch("openpgpcard_x25519_agent.server.signal")
    server_mock = mocker.patch("openpgpcard_x25519_agent.server.Server")

    run_server("10")

    assert server_mock.call_args.kwargs["fileno"] == 10
    seats = server_mock.call_args.kwargs["seats"]
    assert len(seats) == 1
    assert not seats[0].id
    assert not seats[0].pin


def test_run_server_when_systemd_listen_env(mocker, monkeypatch):
    monkeypatch.setenv("LISTEN_FDS", "1")
    mocker.patch("openpgpcard_x25519_agent.server.signal")
    server_mock = mocker.patch("openpgpcard_x25519_agent.server.Server")

    run_server()

    assert server_mock.call_args.kwargs["fileno"] == 3
    seats = server_mock.call_args.kwargs["seats"]
    assert len(seats) == 1
    assert not seats[0].id
    assert not seats[0].pin


def test_server_start_when_socket_path(tmp_path):
    server = Server(tmp_path / "test.sock")
    server._listen = MagicMock(
        side_effect=lambda selector: _assert_server_listening(server, selector)
    )

    server.start()

    # assert sever state cleaned up after start exits
    assert not server.listening
    assert not server.path.exists()
    assert not server.fileno
    assert not server.socket
    assert not server.interrupt_sender
    assert not server.interrupt_receiver


def test_server_start_when_fileno(tmp_path):
    sock = socket(AF_UNIX, SOCK_STREAM)
    sock.bind(str(tmp_path / "test.sock"))
    fileno = sock.fileno()

    server = Server(fileno=fileno)
    server._listen = MagicMock(
        side_effect=lambda selector: _assert_server_listening(server, selector, fileno)
    )

    server.start()

    # assert sever state cleaned up after start exits
    assert not server.listening
    assert not server.path
    assert server.fileno == fileno
    assert not server.socket
    assert not server.interrupt_sender
    assert not server.interrupt_receiver


def _assert_server_listening(server, selector, fileno=None):
    assert server.listening
    if fileno:
        assert not server.path
        assert server.fileno == fileno
    else:
        assert server.path.exists()
        assert not server.fileno
    assert server.socket
    assert server.interrupt_sender
    assert server.interrupt_receiver

    assert selector.get_key(server.socket).data == "accept"
    assert selector.get_key(server.interrupt_receiver).data == "interrupt"


def test_server_stop_when_has_interrupt_sender():
    server = Server("test.sock")
    server.interrupt_sender = MagicMock()

    server.stop()

    server.interrupt_sender.send.assert_called()


def test_server_stop_when_no_interrupt_sender(caplog):
    server = Server("test.sock")
    server.interrupt_sender = None

    with caplog.at_level(DEBUG):
        server.stop()

    assert caplog.text.find("not started") >= 0


def test_server_handle_connection_when_success(mocker):
    connection = MagicMock()
    request = MagicMock()
    response = MagicMock()
    mocker.patch(
        "openpgpcard_x25519_agent.server.Message", side_effect=[request, response]
    )

    server = Server("test.sock", seats=[Seat("x"), Seat("y"), Seat("z")])
    request.message_type = ADD_SMARTCARD_KEY
    request.reader_id = "2"
    request.pin = bytearray(b"foo")
    request.constrain_confirm = False

    server.handle_connection(connection)

    assert response.message_type == SUCCESS
    assert server.seats[2].pin == b"foo"

    request.receive.assert_called_once()
    request.zero.assert_called_once()
    response.send.assert_called_once()
    response.zero.assert_called_once()
    connection.close.assert_called_once()


def test_server_handle_connection_when_error_closing_connection(mocker):
    connection = MagicMock()
    request = MagicMock()
    response = MagicMock()
    mocker.patch(
        "openpgpcard_x25519_agent.server.Message", side_effect=[request, response]
    )

    server = Server("test.sock", seats=[Seat("x"), Seat("y"), Seat("z")])
    request.message_type = ADD_SMARTCARD_KEY
    request.reader_id = "2"
    request.pin = bytearray(b"foo")
    request.constrain_confirm = False
    connection.close.side_effect = ConnectionError("test")

    server.handle_connection(connection)

    assert response.message_type == SUCCESS
    assert server.seats[2].pin == b"foo"

    request.receive.assert_called_once()
    request.zero.assert_called_once()
    response.send.assert_called_once()
    response.zero.assert_called_once()
    connection.close.assert_called_once()


def test_server_handle_connection_when_error_sending_response(mocker):
    connection = MagicMock()
    request = MagicMock()
    response = MagicMock()
    mocker.patch(
        "openpgpcard_x25519_agent.server.Message", side_effect=[request, response]
    )

    server = Server("test.sock", seats=[Seat("x"), Seat("y"), Seat("z")])
    request.message_type = ADD_SMARTCARD_KEY
    request.reader_id = "2"
    request.pin = bytearray(b"foo")
    request.constrain_confirm = False
    response.send.side_effect = ConnectionError("test")

    server.handle_connection(connection)

    assert response.message_type == SUCCESS
    assert server.seats[2].pin == b"foo"

    request.receive.assert_called_once()
    request.zero.assert_called_once()
    response.send.assert_called_once()
    response.zero.assert_called_once()
    connection.close.assert_called_once()


def test_server_handle_connection_when_error_handling_request(mocker):
    connection = MagicMock()
    request = MagicMock()
    response = MagicMock()
    mocker.patch(
        "openpgpcard_x25519_agent.server.Message", side_effect=[request, response]
    )
    failure_message = mocker.patch("openpgpcard_x25519_agent.server.FAILURE_MESSAGE")

    # will fail because server has no seats
    server = Server("test.sock")
    request.message_type = ADD_SMARTCARD_KEY
    request.reader_id = "2"
    request.pin = bytearray(b"foo")
    request.constrain_confirm = False

    server.handle_connection(connection)

    failure_message.send.assert_called_once()

    request.receive.assert_called_once()
    request.zero.assert_called_once()
    response.send.assert_not_called()
    response.zero.assert_called_once()
    connection.close.assert_called_once()


def test_server_handle_connection_when_when_error_receiving_request(mocker):
    connection = MagicMock()
    request = MagicMock()
    response = MagicMock()
    mocker.patch(
        "openpgpcard_x25519_agent.server.Message", side_effect=[request, response]
    )
    failure_message = mocker.patch("openpgpcard_x25519_agent.server.FAILURE_MESSAGE")

    server = Server("test.sock", seats=[Seat("x"), Seat("y"), Seat("z")])
    request.message_type = ADD_SMARTCARD_KEY
    request.reader_id = "2"
    request.pin = bytearray(b"foo")
    request.constrain_confirm = False
    request.receive.side_effect = ConnectionError("test")
    response.message_type = 0

    server.handle_connection(connection)

    failure_message.send.assert_called_once()

    request.receive.assert_called_once()
    request.zero.assert_called_once()
    response.send.assert_not_called()
    response.zero.assert_called_once()
    connection.close.assert_called_once()


def test_server_request_public_key(five_cards_mock):
    card = five_cards_mock[3]
    card.serial = 0xF
    card.get_public_key.return_value = bytes.fromhex(f"7F49 22 86 20 {EXAMPLE_KEY_HEX}")

    server = Server("test.sock", seats=[Seat("x"), Seat("y"), Seat("f")])
    request = Message(message_type=REQUEST_EXTENSION, extension_type=REQUEST_PUBLIC_KEY)
    request.reader_id = "2"
    response = Message()

    server.handle_request(request, response)
    request.zero()

    assert response.message_type == SUCCESS
    assert response.extension_type == REQUEST_PUBLIC_KEY
    assert response.public_key == bytearray.fromhex(EXAMPLE_KEY_HEX)


def test_server_derived_shared_secret(five_cards_mock, mocker):
    api_shared_secret = bytearray(b"test")
    x25519_mock = mocker.patch(
        "openpgpcard_x25519_agent.card.calculate_x25519_shared_secret",
        side_effect=[PGPCardException(0x69, 0x82), api_shared_secret],
    )
    verify_pin_mock = mocker.patch("openpgpcard_x25519_agent.card.verify_pin")

    card = five_cards_mock[3]
    card.serial = 0xF

    seat = Seat("f", bytearray(b"foo"), derived=True)
    server = Server("test.sock", seats=[Seat("x"), Seat("y"), seat])
    request = Message(
        message_type=REQUEST_EXTENSION, extension_type=DERIVE_SHARED_SECRET
    )
    request.reader_id = "2"
    request.public_key = bytearray(b"bar")
    response = Message()

    server.handle_request(request, response)
    request.zero()

    assert response.message_type == SUCCESS
    assert response.extension_type == DERIVE_SHARED_SECRET
    assert response.shared_secret == b"test"
    verify_pin_mock.assert_called_with(card, bytearray(b"foo"))
    x25519_mock.assert_called_with(card, bytearray(b"bar"))

    response_shared_secret = response.shared_secret
    response.zero()
    assert response_shared_secret == b"\0\0\0\0"
    assert api_shared_secret == b"\0\0\0\0"


def test_server_add_smartcard_key():
    buffer = bytearray(b"foo")
    seat = Seat("z", buffer)
    server = Server("test.sock", seats=[Seat("x"), Seat("y"), seat])
    request = Message(message_type=ADD_SMARTCARD_KEY)
    request.reader_id = "2"
    request.pin = bytearray(b"bar")
    response = Message()

    server.handle_request(request, response)
    request.zero()

    assert response.message_type == SUCCESS
    assert buffer == b"\0\0\0"
    assert seat.pin == b"bar"
    assert not seat.expires


def test_server_add_smartcard_key_when_constrain_lifetime(mocker):
    mocker.patch(
        "openpgpcard_x25519_agent.server._now",
        return_value=datetime(2001, 2, 3, 4, 5, 6),  # noqa: DTZ001
    )

    buffer = bytearray(b"foo")
    seat = Seat("z", buffer)
    server = Server("test.sock", seats=[Seat("x"), Seat("y"), seat])
    request = Message(message_type=ADD_SMARTCARD_KEY_CONSTRAINED)
    request.reader_id = "2"
    request.pin = bytearray(b"bar")
    request.constrain_lifetime = 3600
    response = Message()

    server.handle_request(request, response)
    request.zero()

    assert response.message_type == SUCCESS
    assert buffer == b"\0\0\0"
    assert seat.pin == b"bar"
    assert seat.expires == datetime(2001, 2, 3, 5, 5, 6)  # noqa: DTZ001


def test_server_add_smartcard_key_when_constrain_confirm():
    buffer = bytearray(b"foo")
    seat = Seat("z", buffer)
    server = Server("test.sock", seats=[Seat("x"), Seat("y"), seat])
    request = Message(message_type=ADD_SMARTCARD_KEY_CONSTRAINED)
    request.reader_id = "2"
    request.pin = bytearray(b"bar")
    request.constrain_confirm = True
    response = Message()

    server.handle_request(request, response)
    request.zero()

    assert response.message_type == FAILURE
    assert buffer == b"foo"
    assert seat.pin == b"foo"
    assert not seat.expires


def test_server_remove_smartcard_key():
    buffer = bytearray(b"foo")
    seat = Seat("z", buffer)
    server = Server("test.sock", seats=[Seat("x"), Seat("y"), seat])
    request = Message(message_type=REMOVE_SMARTCARD_KEY)
    request.reader_id = "2"
    request.pin = bytearray(b"bar")
    response = Message()

    server.handle_request(request, response)
    request.zero()

    assert response.message_type == SUCCESS
    assert buffer == b"\0\0\0"
    assert not seat.pin
    assert not seat.expires


def test_server_listen_when_interrupt_available():
    key = MagicMock()
    key.data = "interrupt"
    selector = MagicMock()
    selector.select.return_value = [(key, 0)]

    server = Server("test.sock")
    server.listening = True

    server._listen(selector)

    assert not server.listening


def test_server_listen_when_accept_available(tmp_path):
    key = MagicMock()
    key.data = "accept"
    selector = MagicMock()
    selector.select.return_value = [(key, 0)]

    server = Server(tmp_path / "test.sock")
    server.listening = True
    server.socket = MagicMock()
    server.socket.accept.return_value = (MagicMock(), None)
    server.handle_connection = MagicMock(
        side_effect=lambda _: setattr(server, "listening", False)
    )

    server._listen(selector)

    server.handle_connection.assert_called_once()


def test_server_bind_interrupt_when_already_bound(caplog):
    server = Server("test.sock")
    server.interrupt_receiver = True
    server._bind_interrupt(None)
    assert caplog.text.find("interrupt already bound") >= 0


def test_server_bind_when_already_bound(caplog):
    server = Server("test.sock")
    server.socket = True
    server._bind(None)
    assert caplog.text.find("already bound to test.sock") >= 0


def test_server_unbind_when_already_unbound(caplog):
    server = Server("test.sock")
    server._unbind(None)
    assert caplog.text.find("not bound to test.sock") >= 0


def test_server_unbind_interrupt_when_already_unbound(caplog):
    server = Server("test.sock")
    server._unbind_interrupt(None)
    assert caplog.text.find("interrupt not bound") >= 0


def test_server_get_seat_when_invalid_id():
    with pytest.raises(ValueError, match="not have requested seat: foo"):
        assert Server("test.sock").get_seat("foo")


def test_server_get_seat_when_no_seats():
    with pytest.raises(ValueError, match="not have requested seat: 0"):
        assert Server("test.sock").get_seat("0")


def test_server_get_seat_when_index_too_high():
    with pytest.raises(ValueError, match="not have requested seat: 10"):
        assert Server("test.sock", seats=[Seat(), Seat(), Seat()]).get_seat("10")


def test_server_get_seat_when_index_found():
    server = Server("test.sock", seats=[Seat("x"), Seat("y"), Seat("z")])
    assert server.get_seat("2").id == "z"


def test_seat_derive_pin_when_not_set():
    card = None
    assert not Seat().derive_pin(card)


def test_seat_derive_pin_when_no_expires_and_already_derived():
    card = None
    assert Seat(pin=bytearray(b"foo"), derived=True).derive_pin(card) == b"foo"


def test_seat_derive_pin_when_no_expires_and_no_kdf():
    card = MagicMock()
    card.get_data.return_value = []
    assert Seat(pin=bytearray(b"foo")).derive_pin(card) == b"foo"


def test_seat_derive_pin_when_no_expires_and_test_kdf():
    card = MagicMock()
    card.get_data.return_value = bytearray.fromhex(TEST_KDF_DO)
    assert Seat(pin=bytearray(b"foo")).derive_pin(card).hex().upper() == TEST_KDF_FOO


def test_seat_derive_pin_when_not_expired_and_no_kdf():
    card = MagicMock()
    card.get_data.return_value = []
    buffer = bytearray(b"foo")
    seat = Seat(pin=buffer, expires=datetime(2100, 1, 1))  # noqa: DTZ001

    assert seat.derive_pin(card) == b"foo"

    assert buffer == b"foo"
    assert seat.pin == b"foo"
    assert seat.derived
    assert seat.expires == datetime(2100, 1, 1)  # noqa: DTZ001


def test_seat_derive_pin_when_not_expired_and_test_kdf():
    card = MagicMock()
    card.get_data.return_value = bytearray.fromhex(TEST_KDF_DO)
    buffer = bytearray(b"foo")
    seat = Seat(pin=buffer, expires=datetime(2100, 1, 1))  # noqa: DTZ001

    assert seat.derive_pin(card).hex().upper() == TEST_KDF_FOO

    assert buffer == b"\0\0\0"
    assert seat.pin.hex().upper() == TEST_KDF_FOO
    assert seat.derived
    assert seat.expires == datetime(2100, 1, 1)  # noqa: DTZ001


def test_seat_derive_pin_when_expired():
    card = None
    buffer = bytearray(b"foo")
    seat = Seat(pin=buffer, derived=True, expires=datetime(2001, 2, 3))  # noqa: DTZ001

    assert not seat.derive_pin(card)

    assert buffer == b"\0\0\0"
    assert seat.pin == b""
    assert not seat.derived
    assert not seat.expires


def test_seat_set_pin():
    buffer = bytearray(b"foo")
    seat = Seat(pin=buffer, derived=True, expires=datetime(2001, 2, 3))  # noqa: DTZ001

    seat.set_pin(bytearray(b"123456"))

    assert buffer == b"\0\0\0"
    assert seat.pin == b"123456"
    assert not seat.derived
    assert not seat.expires


def test_seat_set_pin_with_expires():
    seat = Seat()

    seat.set_pin(bytearray(b"foo"), expires=datetime(2001, 2, 3))  # noqa: DTZ001

    assert seat.pin == b"foo"
    assert not seat.derived
    assert seat.expires == datetime(2001, 2, 3)  # noqa: DTZ001


def test_seat_set_pin_with_derived():
    seat = Seat()

    seat.set_pin(bytearray(b"foo"), derived=True)

    assert seat.pin == b"foo"
    assert seat.derived
    assert not seat.expires


def test_seat_clear_pin():
    buffer = bytearray(b"foo")
    seat = Seat(pin=buffer, derived=True, expires=datetime(2001, 2, 3))  # noqa: DTZ001

    seat.clear_pin()

    assert buffer == b"\0\0\0"
    assert not seat.pin
    assert not seat.derived
    assert not seat.expires


def test_seat_clear_pin_after_derive():
    card = MagicMock()
    card.get_data.return_value = bytearray.fromhex(TEST_KDF_DO)
    seat = Seat(pin=bytearray(b"foo"))
    buffer = seat.derive_pin(card)

    seat.clear_pin()

    assert buffer == bytearray(32)
    assert not seat.pin
    assert not seat.derived
    assert not seat.expires


def test_seat_expired_when_no_expires():
    assert not Seat().expired()


def test_seat_expired_when_not_expired():
    assert not Seat(expires=datetime(2100, 1, 1)).expired()  # noqa: DTZ001


def test_seat_expired_when_expired():
    assert Seat(expires=datetime(2000, 1, 1)).expired()  # noqa: DTZ001
