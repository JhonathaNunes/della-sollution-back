from models import db
from exceptions import NotFoundException

def get_all(model):
    return model.query.all()


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit()


def delete_instance(model, id):
    instance = model.query.get(id)

    if instance is None:
        raise NotFoundException

    db.session.delete(instance)
    commit()


def update_instance(model, id, **kwargs):
    instance = model.query.get(id)

    if instance is None:
        raise NotFoundException

    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit()


def commit():
    db.session.commit()
