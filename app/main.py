from datetime import datetime

from app.core.conf import settings
from app.core.logging import app_logger
from app.models.models import *
from app.utils.send_sms import send_notification
from app.core.deps import get_db


def check_room_availability(room_id: int, start_time: datetime, end_time: datetime) -> bool:
    session = get_db()
    overlapping_reservations = session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).all()

    if not overlapping_reservations:
        return True
    for reservation in overlapping_reservations:
        user = reservation.user
        duration = reservation.end_time - reservation.start_time

        message = f"Room {room_id} is busy. Reserved by User {user.full_name}.\n"
        message += f"Reservation duration: {duration}"
        app_logger.info(message)
    return False


def reserve_room(room_id: int, start_time: datetime, end_time: datetime, user_id: int = 1):
    session = get_db()
    reservation = Reservation(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
        user_id=user_id
    )
    session.add(reservation)
    session.commit()

    app_logger.info(f"Room {room_id} reserved successfully!\n")

    user = session.query(User).get(user_id)
    notification_message = f"Room {room_id} has been reserved.\n"
    notification_message += f"Reservation details:\n"
    notification_message += f"Date: {start_time.date()}\n"
    notification_message += f"Time: {start_time.time()} - {end_time.time()}\n"
    notification_message += f"Room Number: {room_id}"

    if not settings.DEBUG:
        send_notification(user.email, user.phone_number, notification_message)
        app_logger.info(f"Sent message to Email:{user.email} and Phone:{user.phone}.\n {notification_message}")
    app_logger.info(f"Sent message to Email:{user.email} and Phone:{user.phone}.\n {notification_message}")
