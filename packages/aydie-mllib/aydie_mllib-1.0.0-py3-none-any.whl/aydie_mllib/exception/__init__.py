import os
import sys

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = "\n\nError occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class AydieException(Exception):
    def __init__(self, error_messgae, error_detail):
        super().__init__(error_messgae)
        self.error_message = error_message_detail(
            error_messgae, error_detail = error_detail
        )
        
    def __str__(self):
        return self.error_message