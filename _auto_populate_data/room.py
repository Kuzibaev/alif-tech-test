from app.core.deps import get_db
from app.core.logging import app_logger
from app.models import Room


def create_rooms(total_rooms: int = 5) -> None:
    db = get_db()
    existing_rooms = db.query(Room).count()
    if existing_rooms > 0:
        app_logger.info("Rooms already exist in the database.")
        db.close()
        return

    rooms = []
    for i in range(1, total_rooms + 1):
        room = Room(number=f"Room {i}", capacity=i)
        rooms.append(room)

    db.add_all(rooms)
    db.commit()

    app_logger.info(f"Successfully created {total_rooms} rooms.")

    db.close()
