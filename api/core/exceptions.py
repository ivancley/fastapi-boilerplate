from fastapi import HTTPException, status


class ExceptionNotFound(HTTPException):
    def __init__(self, detail: str = "Não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ExceptionBadRequest(HTTPException):
    def __init__(self, detail: str = "Erro de requisição"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ExceptionInternalServerError(HTTPException):
    def __init__(self, detail: str = "Erro interno no servidor"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
