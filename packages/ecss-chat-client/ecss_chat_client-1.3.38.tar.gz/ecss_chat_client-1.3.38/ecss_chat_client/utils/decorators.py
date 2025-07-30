class DecoratorsService:

    @staticmethod
    def paginate(function):
        """Установки пагинации."""
        def wrapper(self, *args, **kwargs):
            count = kwargs.get('count', self.settings.count)
            offset = kwargs.get('offset', self.settings.offset)
            return function(self, *args, **kwargs, count=count, offset=offset)
        return wrapper


decorator_service = DecoratorsService()
