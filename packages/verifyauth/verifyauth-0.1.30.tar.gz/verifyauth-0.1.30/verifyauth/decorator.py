import os
import logging
from functools import wraps
from fastapi.responses import JSONResponse, PlainTextResponse
import requests
from fastapi import HTTPException, status
from pythonjsonlogger import jsonlogger
from .response_handler import custom_soap_response
import time

# Configura a URL do serviço de autenticação a partir das variáveis de ambiente, com um valor padrão
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:8083/')

# Inicialização de logger
def initLog(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    log_formatter = jsonlogger.JsonFormatter('%(filename)s %(funcName)s %(lineno)s %(asctime)s %(levelname)s %(name)s %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger

logger = initLog(__name__)

# Decorator para verificar autenticação
def verifyauth(servico, capacidade, response_tag = 'capacidadeServicoDefaultResponse', result_tag = 'capacidadeServicoDefaultResult'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                auth_data = {}

                # Log de entrada
                # print(f"Args: {args}, Kwargs: {kwargs}")
                logger.info(f"Iniciando autenticação para o serviço: {servico}")                
                logger.debug(f"*URL servidor de autenticacao: {AUTH_SERVICE_URL}")

                header = kwargs.get('header')

                if not header:
                    if len(args) > 1:
                        header = args[1]
                    else:
                        logger.error("Objeto header não encontrado.")
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Header object missing")

                if header.security.username_token.username is not None and header.security.username_token.username != '': 
                    # Dados de autenticação
                    auth_data = {
                        "username": header.security.username_token.username,
                        "password": header.security.username_token.password,
                        "service_name": servico,
                        "capacity": capacidade
                    }
                elif header.security.token is not None and header.security.token != '':
                    # Dados de autenticação com token
                    auth_data = {
                        "token": header.security.token,
                    }
                else:
                    logger.error("Nenhum dado de autenticação encontrado.")
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authentication data missing")
                
                logger.info(f"Autenticando dados")
                # print(f"Autenticando com os dados: {auth_data}")
                
                AUTH_URL = AUTH_SERVICE_URL + 'auth'
                response = requests.post(AUTH_URL, json=auth_data)

                # Tratamento das respostas da autenticação
                if response.status_code == 200:
                    return func(*args, **kwargs)
                elif response.status_code == 401:
                    logger.error(f"Falha na autenticação: {response.content}")
                    # raise  HTTPException(401, detail="Authentication Failed")
                    
                    return custom_soap_response(
                        status=False, 
                        # message="Nome de Sistema inválido", 
                        message="Senha do Sistema Inválida",                         
                        response_tag=response_tag,
                        result_tag=result_tag,
                        session_id= int(time.time()),
                        status_code=200
                    )
                else:
                    logger.error(f"Erro de autenticação: {response.content}")
                    raise HTTPException(status_code=401, detail="Authentication Failed")
            except HTTPException as http_exc:
                session_id_error = int(time.time())
                logger.error(f"{session_id_error} - Erro durante a autenticação: {http_exc.status_code} {http_exc.detail}")
                return custom_soap_response(
                    status=False,
                    message=str(http_exc.detail),
                    response_tag=response_tag,
                    result_tag=result_tag,
                    session_id=session_id_error,
                    status_code=http_exc.status_code
                )
            except Exception as e:
                session_id_error = int(time.time())
                logger.error(f"{session_id_error} - Erro inesperado durante a autenticação: {str(e)}")
                return custom_soap_response(
                    status=False,
                    message="Erro interno do servidor",
                    response_tag=response_tag,
                    result_tag=result_tag,
                    session_id=session_id_error,
                    status_code=500
                )

        return wrapper
    return decorator

# Decorator para obter acesso
def GetAccess(servico):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request = kwargs.get('request')
                header = kwargs.get('header')

                # Verificação dos argumentos request e header
                if not request:
                    if len(args) > 0:
                        request = args[0]
                    else:
                        logger.error("Objeto request não encontrado.")

                if not header:
                    if len(args) > 1:
                        header = args[1]
                    else:
                        logger.error("Objeto header não encontrado.")
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Header object missing")

                # Dados de autenticação
                auth_data = {
                    "username": header.security.username_token.username,
                    "password": header.security.username_token.password,
                    "name": servico
                }

                logger.info(f"Obtendo acesso com os dados: {auth_data}")
                GET_URL = AUTH_SERVICE_URL + 'getaccess'
                response = requests.post(GET_URL, json=auth_data)

                # Tratamento das respostas de obtenção de acesso
                #if response.status_code == 200:
                    #return  func(*args, **kwargs)
                if response.status_code == 401:
                    logger.error(f"Falha na autenticação: {response.content}")
                    return PlainTextResponse("Falha na autenticação",status_code=401)
                else:
                    logger.error(f"Erro na obtenção de acesso: {response.content}")
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Authentication Failed")
            except Exception as e:
                logger.error(f"Erro inesperado durante a obtenção de acesso: {str(e)}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro inesperado durante a obtenção de acesso")

        return wrapper
    return decorator
