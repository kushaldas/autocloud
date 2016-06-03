from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


def get_object_or_404(session, model, *criterion):
    try:
        return session.query(model).filter(*criterion).one()
    except exc.NoResultFound, exc.MultipleResultsFound:
        abort(404)
