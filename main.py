from datetime import datetime
from functools import wraps

import typer

from _auto_populate_data.user import create_user
from _auto_populate_data.room import create_rooms

from app.main import (
    check_room_availability,
    reserve_room as reserve_room_notify
)

typer_app = typer.Typer()


@typer_app.command(name='reserve_room')
def reserve_room(room_id: int, start_time: datetime, end_time: datetime) -> None:
    """
    Reserve a room in the office.

    Args:
        room_id: The ID of the room to reserve.
        start_time: The start time of the reservation.
        end_time: The end time of the reservation.
    """

    available = check_room_availability(room_id, start_time, end_time)
    if available:
        user_id = int(input("Enter user id: "))
        reserve_room_notify(room_id, start_time, end_time)
    else:
        print("The room is not empty")


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print('Calling ', f.__name__)
        f(*args, **kwargs)

    return wrapper


@typer_app.command(name="auto_populate")
@coro
def auto_populate_data():
    create_rooms()
    create_user()
    print("Auto populate data saved")


if __name__ == "__main__":
    typer_app()
