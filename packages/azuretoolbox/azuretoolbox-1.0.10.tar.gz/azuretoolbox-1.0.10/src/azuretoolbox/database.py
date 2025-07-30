from typing import Any
from pyodbc import connect
from datetime import datetime
from decimal import Decimal

class Database:
    def __init__(self) -> None:
        self._conn = None
        pass

    def connect(self, server: str, database: str, username: str, password: str, encrypt: bool = True, trust_server_certificate: bool = False, connection_timeout: int = 30) -> bool:
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};" \
            "SERVER=" + server + ";" \
            "DATABASE=" + database + ";" \
            "UID=" + username + ";" \
            "PWD=" + password + ";" \
            "Encrypt=" + ("yes" if encrypt else "no") + ";" \
            "TrustServerCertificate=" + ("yes" if trust_server_certificate else "no") + ";" \
            "Connection Timeout=" + str(connection_timeout) + ";"

        self._conn = connect(conn_str)
        return True

    def disconnect(self) -> bool:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        return True

    def __parse__(self, response: list, header: tuple) -> list[dict]:
        result = []
        for row in response:
            temp = {}
            for i in range(len(header)):
                try:
                    if type(row[i]) == datetime:
                        temp[header[i][0]] = row[i].strftime(
                            '%Y-%m-%d %H:%M:%S')
                    elif type(row[i]) == Decimal:
                        temp[header[i][0]] = float(row[i])
                    elif type(row[i]) == bytes:
                        temp[header[i][0]] = row[i].decode('latin-1')
                    else:
                        temp[header[i][0]] = row[i]
                except Exception:  # pragma: no cover
                    temp[header[i][0]] = str(row[i])
            result.append(temp)
        return result

    def query(self, query: str) -> list[dict]:
        if self._conn is None:
            raise Exception("Connection not established")

        cursor = self._conn.cursor()
        cursor.execute(query)
        response = cursor.fetchall()
        return self.__parse__(response, cursor.description)

    def command(self, query: str, *params: Any) -> bool:
        if self._conn is None:
            raise Exception("Connection not established")

        cursor = self._conn.cursor()
        cursor.execute(query, params)
        self._conn.commit()
        return True
