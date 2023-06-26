import typer

from app.core.deps import get_db
from app.models import Room


def create_rooms(total_rooms: int = 5) -> None:
    db = get_db()
    existing_rooms = db.query(Room).count()
    if existing_rooms > 0:
        typer.echo("Rooms already exist in the database.")
        db.close()
        return

    rooms = []
    for i in range(1, total_rooms + 1):
        room = Room(number=f"Room {i}", capacity=i)
        rooms.append(room)

    db.add_all(rooms)
    db.commit()

    typer.echo(f"Successfully created {total_rooms} rooms.")

    db.close()
