import logging
from functools import wraps, partial

logger = logging.getLogger('aplus_client.interfaces')


def none_on_error(*args, exceptions=None):
    if not args:
        return partial(none_on_error, exceptions=exceptions)
    if len(args) > 1 or (isinstance(args[0], type) and issubclass(args[0], Exception)):
        return partial(none_on_error, exceptions=args)

    func = args[0]
    exceptions = tuple(set([AttributeError] + (list(exceptions) if exceptions else [])))

    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            logger.info("interface %s raised exception %s", func.__name__, e)
            return None
    return wrap


class GraderInterface2:
    def __init__(self, data):
        self.data = data

    @property
    @none_on_error
    def exercise(self):
        return self.data.exercise

    @property
    @none_on_error
    def course(self):
        return self.data.exercise.course

    @property
    @none_on_error
    def language(self):
        return self.data.exercise.course.language or None

    @property
    @none_on_error(KeyError)
    def form_spec(self):
        return self.data.exercise.exercise_info.get_item('form_spec')

    @property
    @none_on_error
    def submitters(self):
        return self.data.submission.submitters
