# -*- coding: utf-8 -*-
# custom_erros.py
# Authors: Stephan Meighen-Berger
# Collection of custom errors for subghosts

import sys
import inspect


class NoTraceBackWithLineNumber(Exception):
    """Custom error messages for exceptions"""
    def __init__(self, msg):
        try:

            ln = sys.exc_info()[-1].tb_lineno
        except AttributeError:
            ln = inspect.currentframe().f_back.f_lineno
            stack = inspect.stack()
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            the_method = stack[1][0].f_code.co_name
            print("An error was raised in {}.{}()".format(the_class, the_method))
        self.args = "{0.__name__} (line {1}): {2}".format(type(self), ln, msg),
        sys.exit(self)


class CustomError(NoTraceBackWithLineNumber):
    """ example for a custom error class"""
    pass

class UnknownModelError(NoTraceBackWithLineNumber):
    """ Unknown model error"""
    pass

class UnphysicalError(NoTraceBackWithLineNumber):
    """ input values aren't physical"""
    pass

class NotImplementedError(NoTraceBackWithLineNumber):
    """ This has not yet been implemented. Please contact the authors"""
    pass
