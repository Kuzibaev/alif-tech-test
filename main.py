import logging
from datetime import datetime, timedelta
from functools import wraps
import typer

from app.main import check_room_availability, reserve_room as reserve_room_notify
from app.utils.datetime import utcnow
from _auto_populate_data.user import create_user
from _auto_populate_data.room import create_rooms

typer_app = typer.Typer()

logger = logging.getLogger(__name__)


@typer_app.command(name='reserve_room')
def reserve_room(room_id: int = 1, start_time: datetime = utcnow() + timedelta(hours=1),
                 end_time: datetime = utcnow() + timedelta(hours=2)) -> None:
    """
    Reserve a room in the office.

    Args:
        room_id: The ID of the room to reserve.
        start_time: The start time of the reservation.
        end_time: The end time of the reservation.
    """

    available = check_room_availability(room_id, start_time, end_time)
    if available:
        reserve_room_notify(room_id, start_time, end_time)
    else:
        logger.debug("The room is not empty")


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
    logger.debug("Auto populate data saved")
    typer.echo("Auto populate data saved")


if __name__ == "__main__":
    typer_app()
