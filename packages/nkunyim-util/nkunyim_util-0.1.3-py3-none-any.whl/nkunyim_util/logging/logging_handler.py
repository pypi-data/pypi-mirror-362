import csv
from datetime import datetime
import logging
from pathlib import Path

from django.conf import settings

from .logging_command import LoggingCommand, LOG_TYPE_KEY, LOG_TYPE_GEN



class LoggingHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        try:
            data = record.__dict__.copy()
            stream = data[LOG_TYPE_KEY] if LOG_TYPE_KEY in data else LOG_TYPE_GEN
            command = LoggingCommand()
            response = command.send(stream=stream, data=data)
            if not response.ok:
                self._write_to_csv(data)

        except Exception:
            self.handleError(record)

    def _write_to_csv(self, data: dict) -> None:
        date_str = datetime.now().strftime("%Y%m%d")
        file_path = Path(settings.TEXT_FILE_PATH) / f"{date_str}.csv"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        write_header = not file_path.exists() or file_path.stat().st_size == 0

        with file_path.open(mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())

            if write_header:
                writer.writeheader()

            writer.writerow(data)