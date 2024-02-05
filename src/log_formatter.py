import logging
import os
import re
from datetime import datetime
from pathlib import Path

import aiofiles


class LogAligner:
    """
    Aligns log lines in a log file.

    Attributes:
        file_path (Path): Path to the log file.
        delete_original (bool): Whether to delete the original file after alignment.
    """

    LOG_LINE_PATTERN = re.compile(r" - ")

    def __init__(self, file_path="app.log", delete_original=False):
        self.file_path = Path(file_path)
        self.delete_original = delete_original
        self.logger = logging.getLogger(self.__class__.__name__)

    async def align_log_entries(self):
        """
        Aligns the log lines in the file asynchronously.
        """
        lines = await self._read_logs()
        if not lines:
            return

        max_name_length, max_level_length = self._analyze_log_lines(lines)
        output_file = Path(f"hue-alerts_{datetime.now().strftime('%Y%m%d')}.log")
        await self._write_aligned_logs(
            lines, max_name_length, max_level_length, output_file
        )

        if self.delete_original:
            self._delete_file(self.file_path)

    async def _read_logs(self):
        """
        Reads the logs from the file asynchronously.

        Returns:
            list: List of log lines.
        """
        self.logger.debug(f"Reading logs from '{self.file_path}' and aligning them.")
        try:
            async with aiofiles.open(
                self.file_path, mode="r", encoding="utf-8"
            ) as file:
                return await file.readlines()
        except IOError as e:
            raise IOError(f"Error reading file {self.file_path}: {e}") from e

    def _analyze_log_lines(self, lines):
        """
        Analyzes the log lines to determine the maximum length of the name and level.

        Args:
            lines (list): List of log lines.

        Returns:
            tuple: Tuple containing the maximum name and level lengths.
        """
        max_name_length, max_level_length = 0, 0
        for line in lines:
            parts = self.LOG_LINE_PATTERN.split(line)
            if len(parts) >= 4:
                max_name_length, max_level_length = (
                    max(max_name_length, len(parts[1])),
                    max(max_level_length, len(parts[2])),
                )
        return max_name_length, max_level_length

    async def _write_aligned_logs(
        self, lines, max_name_length, max_level_length, output_file
    ):
        """
        Writes the aligned log lines to a new file asynchronously.

        Args:
            lines (list): List of log lines.
            max_name_length (int): Maximum length of the name.
            max_level_length (int): Maximum length of the level.
            output_file (Path): Path to the output file.
        """

        try:
            async with aiofiles.open(output_file, mode="w", encoding="utf-8") as file:
                for line in lines:
                    parts = self.LOG_LINE_PATTERN.split(line, maxsplit=3)
                    if len(parts) >= 4:
                        aligned_line = f"{parts[0]} - {parts[1]:<{max_name_length}} - {parts[2]:<{max_level_length}} - {parts[3]}"
                        await file.write(aligned_line)
        except IOError as e:
            raise IOError(f"Error writing to file {output_file}: {e}") from e

    def _delete_file(self, file_path):
        """
        Deletes the file.

        Args:
            file_path (Path): Path to the file.
        """
        try:
            os.remove(file_path)
        except OSError as e:
            raise OSError(f"Error deleting file {file_path}: {e}") from e
