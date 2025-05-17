

class PathLogger:
    def __init__(self,
                 delimiter: str = ";",
                 overwrite: bool = True,
                 header: list[str] = None,
                 log_file_path: str = "path_logger.log"):

        self._delimiter = delimiter
        self._overwrite = overwrite
        self._header = header
        self._log_file_path = log_file_path

        # Create file and write header if specified
        self._open_file()
        if self._header:
            self._write_to_file(self._header)


    def __del__(self):
        self._log_file.close()


    def _open_file(self):
        write_mode = "w" if self._overwrite else "w+"
        self._log_file = open(self._log_file_path, write_mode, encoding="utf-8")


    def _write_to_file(self, values: list[str]|tuple[any, ...]):
        output_string = ""
        for value in values:
            output_string += str(value)
            output_string += self._delimiter


        output_string = output_string[:-1]
        output_string += "\n"
        self._log_file.write(output_string)


    def write_log(self, *values: any):
            if self._header is None or len(self._header) == len(values):
                self._write_to_file(values)
            else:
                raise RuntimeError("Header size does not match the number of values")


    def close_logger(self):
        self._log_file.close()
