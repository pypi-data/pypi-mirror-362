import re
from subprocess import (
    PIPE,
    Popen,
)


class HashData:
    """Хэширует данные."""

    # Регулярное выражение для получения вычисленного значения HASH
    HASH_PATTERN = '\(stdin\)= (?P<hash>.+)\\n'  # noqa: W605

    def __init__(self, hash_algorithm: str, delimiter: str = ''):
        self.hash_algorithm = hash_algorithm  # Пример: 'md_gost12_256'
        self.delimiter = delimiter

    def _get_hash(self, *args: str) -> str:
        """Возвращает HASH для строки сформированной из переданных данных.

        :param args: хэшируемые данные
        :raises IOError: ошибка при вычислении хэша
        :raises ValueError: вывод команды не содержит хэша
        :return: хэш
        """
        text = self.delimiter.join(args).strip().encode()

        pr = Popen(
            [f'openssl dgst -{self.hash_algorithm}'],
            shell=True,  # noqa: S602
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )
        openssl_stdout, openssl_stderr = pr.communicate(text)

        if openssl_stderr:
            raise IOError(
                f'Ошибка вычисления значения HASH по алгоритму {self.hash_algorithm}',
            )

        matches = re.compile(self.HASH_PATTERN).search(openssl_stdout.decode())

        if matches is None:
            raise ValueError(f'Строка "{openssl_stdout}" не содержит HASH')

        return matches.group('hash')

    def get_hash(self, *args: str) -> str:
        """
        Интерфейс хэширования строки.

        Возвращает хэш-строку.
        """
        return self._get_hash(*args)

    def get_upper_hash(self, *args: str) -> str:
        """
        Интерфейс хэширования строки.

        Возвращает хэш-строку в верхнем регистре.
        """
        return self._get_hash(*args).upper()
