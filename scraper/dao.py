"""Data accessor object for SQLAlchemy handling."""

import logging
import urllib

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy import orm


def _ping_db(dbapi_conn, connection_rec, connection_proxy):
    """
    Ensures that MySQL connections checked out of the pool are alive.

    Originally borrowed from:
    http://groups.google.com/group/sqlalchemy/msg/a4ce563d802c929f

    and than updated with:
    https://review.openstack.org/34266

    Error codes caught:
    * 2006 MySQL server has gone away
    * 2013 Lost connection to MySQL server during query
    * 2014 Commands out of sync; you can't run this command now
    * 2045 Can't open shared memory; no answer from server (%lu)
    * 2055 Lost connection to MySQL server at '%s', system error: %d

    from http://dev.mysql.com/doc/refman/5.6/en/error-messages-client.html
    """

    try:
        dbapi_conn.cursor().execute('select 1')
    except dbapi_conn.OperationalError as e:
        if e.args[0] in (2006, 2013, 2014, 2045, 2055):
            logging.warn('Got mysql server has gone away: %s', e)
            raise exc.DisconnectionError("Database server went away")
        else:
            raise


class DataAccessor(object):

    def __init__(self, connection_uri, debug=False):
        self._engine = None
        self._session_maker = None
        self._connection_uri = connection_uri
        # Sometimes this is needed to quote unusual passwords
        # urllib.quote_plus(connection_uri)
        self._debug = debug

    @property
    def session(self):
        if self._session_maker is None:
            self._session_maker = orm.sessionmaker(bind=self._engine,
                                             autocommit=True,
                                             expire_on_commit=False)
        return self._session_maker()

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self._connection_uri,
                convert_unicode=True,
                echo=self._debug,
                pool_recycle=400
            )
            if self._engine.name.lower() == 'mysql':
                event.listen(self._engine, 'checkout', _ping_db)

        return self._engine
