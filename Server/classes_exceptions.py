#pylint: disable = E0611

class PlayerNotFoundException(Exception):
    """
    Exceção levantada quando um player não é encontrado.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SingletonException(Exception):
    """
    Exceção levantada ao tentar criar múltiplas instâncias de uma classe singleton.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message
