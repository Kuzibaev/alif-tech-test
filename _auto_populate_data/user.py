import typer

from app.core.deps import get_db
from app.core.sessions import Session
from app.models import User

DATAS = [
    {
        'full_name': 'Turonbek Kuzibaev',
        'phone': '+99899872344',
        'email': 'qoziboyevturonbek@gmail.com'
    }
]


def create_user():
    db = get_db()
    existing_users = db.query(User).count()
    if existing_users > 0:
        typer.echo("Users already exist in the database.")
        db.close()
        return
    users = []
    for data in DATAS:
        user = User(**data)
        users.append(user)

    db.add_all(users)
    db.commit()

    typer.echo("Successfully created users.")

    db.close()
