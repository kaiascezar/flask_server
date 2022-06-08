from flask.cli import FlaskGroup
from project import app, db, Fruit


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(Fruit(name="BillyMin", password='test1234!'))
    db.session.commit()
    

if __name__ == "__main__":
    cli()
