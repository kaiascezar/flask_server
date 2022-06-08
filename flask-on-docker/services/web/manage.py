from flask.cli import FlaskGroup
from project import create_app, db


cli = FlaskGroup(create_app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    __tablename__ = "users"

    db.session.add(username="BillyMin", password='test1234!')
    db.session.commit()
    

if __name__ == "__main__":
    cli()
