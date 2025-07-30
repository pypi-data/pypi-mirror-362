import os
import subprocess
import platform
import click
from Osdental.Shared.Logger import logger
from Osdental.Shared.Enums.Message import Message
from Osdental.Shared.Utils.CaseConverter import CaseConverter

SRC_PATH = 'src'
APP_PATH = os.path.join(SRC_PATH, 'Application')
DOMAIN_PATH = os.path.join(SRC_PATH, 'Domain')
INFRA_PATH = os.path.join(SRC_PATH, 'Infrastructure')
GRAPHQL_PATH = os.path.join(INFRA_PATH, 'Graphql')
SCHEMAS_PATH = os.path.join(GRAPHQL_PATH, 'Schemas')

@click.group()
def cli():
    """Comandos personalizados para gestionar el proyecto."""
    pass

@cli.command()
def clean():
    """Borrar todos los __pycache__."""
    if platform.system() == 'Windows':
        subprocess.run('for /d /r . %d in (__pycache__) do @if exist "%d" rd /s/q "%d"', shell=True)
    else:
        subprocess.run("find . -name '__pycache__' -type d -exec rm -rf {} +", shell=True)

    logger.info(Message.PYCACHE_CLEANUP_SUCCESS_MSG)


@cli.command(name='start-app')
@click.argument('app')
def start_app(app: str):
    """Crear un servicio con estructura hexagonal y CRUD básico."""
    app = CaseConverter.snake_to_pascal(app)
    if '-' in app:
        part_one, part_two = tuple(app.split('-'))
        app = CaseConverter.snake_to_pascal(part_one) + CaseConverter.snake_to_pascal(part_two)

    name_method = CaseConverter.case_to_snake(app)
    data = 'data: Dict[str,str]'
    token = 'token: AuthToken'
    api_type_response = 'Response!'
    
    directories = [
        os.path.join(SRC_PATH),
        os.path.join(APP_PATH, 'UseCases'),
        os.path.join(APP_PATH, 'Interfaces'),
        os.path.join(DOMAIN_PATH, 'Interfaces'),
        os.path.join(GRAPHQL_PATH, 'Resolvers'),
        os.path.join(SCHEMAS_PATH),
        os.path.join(SCHEMAS_PATH, app),
        os.path.join(INFRA_PATH, 'Repositories', app)
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Contenidos CRUD
    use_case_interface_name = f'{app}UseCaseInterface'
    use_case_interface_content = f'''
from abc import ABC, abstractmethod
from typing import Dict
from Osdental.Models.Token import AuthToken

class {use_case_interface_name}(ABC):

    @abstractmethod
    async def get_all_{name_method}(self, {token}, {data}) -> str: ...

    @abstractmethod
    async def get_{name_method}_by_id(self, {token}, {data}) -> str: ...

    @abstractmethod
    async def create_{name_method}(self, {token}, {data}) -> str: ...

    @abstractmethod
    async def update_{name_method}(self, {token}, {data}) -> str: ...

    @abstractmethod
    async def delete_{name_method}(self, {token}, {data}) -> str: ...
    '''


    use_case_content = f'''
from typing import Dict
from Osdental.Decorators.DecryptedData import process_encrypted_data
from Osdental.Models.Token import AuthToken
from ..Interfaces.{use_case_interface_name} import {use_case_interface_name}
from src.Domain.Interfaces.{app}RepositoryInterface import {app}RepositoryInterface

class {app}UseCase({use_case_interface_name}):

    def __init__(self, repository: {app}RepositoryInterface):
        self.repository = repository
        
    @process_encrypted_data()
    async def get_all_{name_method}(self, {token}, {data}) -> str: pass

    @process_encrypted_data()        
    async def get_{name_method}_by_id(self, {token}, {data}) -> str: pass
        
    @process_encrypted_data()    
    async def create_{name_method}(self, {token}, {data}) -> str: pass

    @process_encrypted_data()
    async def update_{name_method}(self, {token}, {data}) -> str: pass

    @process_encrypted_data()
    async def delete_{name_method}(self, {token}, {data}) -> str: pass
    '''


    repository_interface_name = f'{app}RepositoryInterface'
    repository_interface_content = f'''
from abc import ABC, abstractmethod
from typing import List, Dict

class {repository_interface_name}(ABC):

    @staticmethod
    @abstractmethod
    async def get_all_{name_method}(self, {data}) -> List[Dict[str,str]]: ...

    @staticmethod
    @abstractmethod
    async def get_{name_method}_by_id(self, id: str) -> Dict[str,str]: ...

    @staticmethod
    @abstractmethod
    async def create_{name_method}(self, {data}) -> str: ...

    @staticmethod
    @abstractmethod
    async def update_{name_method}(self, id: str, {data}) -> str: ...
    
    @staticmethod
    @abstractmethod
    async def delete_{name_method}(self, id: str) -> str: ...
    '''


    repository_content = f'''
from typing import List, Dict
from src.Domain.Interfaces.{repository_interface_name} import {repository_interface_name}

class {app}Repository({repository_interface_name}):
    
    @staticmethod
    async def get_all_{name_method}({data}) -> List[Dict[str,str]]: pass
    
    @staticmethod
    async def get_{name_method}_by_id(id: str) -> Dict[str,str]: pass

    @staticmethod    
    async def create_{name_method}({data}) -> str: pass

    @staticmethod                
    async def update_{name_method}(id: str, {data}) -> str:pass
        
    @staticmethod    
    async def delete_{name_method}(id: str) -> str: pass
    '''


    query_graphql = f'''type Query {{
    getAll{app}(data: String!): {api_type_response}
    get{app}ById(data: String!): {api_type_response}
}}
    '''

    mutation_graphql = f'''type Mutation {{
    create{app}(data: String!): {api_type_response}
    update{app}(data: String!): {api_type_response}
    delete{app}(data: String!): {api_type_response}
}}
    '''

    resolver_content_init = f"""
from ..Resolvers.{app}Resolver import {app}Resolver

{name_method}_query_resolvers = {{
    'getAll{app}': {app}Resolver.resolve_get_all_{name_method},
    'get{app}ById': {app}Resolver.resolve_get_{name_method}_by_id
}}

{name_method}_mutation_resolvers = {{
    'create{app}': {app}Resolver.resolve_create_{name_method},
    'update{app}': {app}Resolver.resolve_update_{name_method},
    'delete{app}': {app}Resolver.resolve_delete_{name_method}
}}
    """

    resolver_content = f'''
from Osdental.Decorators.AuditLog import handle_audit_and_exception
from src.Application.UseCases.{app}UseCase import {app}UseCase
from src.Infrastructure.Repositories.{app}.{app}Repository import {app}Repository

use_case = {app}UseCase({app}Repository)

class {app}Resolver:
        
    @staticmethod
    @handle_audit_and_exception
    async def resolve_get_all_{name_method}(_, info, data):
        return await use_case.get_all_{name_method}(info=info, aes_data=data)

    @staticmethod
    @handle_audit_and_exception
    async def resolve_get_{name_method}_by_id(_, info, data):
        return await use_case.get_{name_method}_by_id(info=info, aes_data=data)

    @staticmethod
    @handle_audit_and_exception
    async def resolve_create_{name_method}(_, info, data):
        return await use_case.create_{name_method}(info=info, aes_data=data)

    @staticmethod
    @handle_audit_and_exception
    async def resolve_update_{name_method}(_, info, data):
        return await use_case.update_{name_method}(info=info, aes_data=data)
    
    @staticmethod
    @handle_audit_and_exception
    async def resolve_delete_{name_method}(_, info, data):
        return await use_case.delete_{name_method}(info=info, aes_data=data)
    '''


    response_content = '''
type Response {
    status: String
    message: String
    data: String
}
    '''

    repository_init_content = ''
    
    files = {
        os.path.join(APP_PATH, 'UseCases', f'{app}UseCase.py'): use_case_content,
        os.path.join(APP_PATH, 'Interfaces', f'{app}UseCaseInterface.py'): use_case_interface_content,
        os.path.join(DOMAIN_PATH, 'Interfaces', f'{app}RepositoryInterface.py'): repository_interface_content,
        os.path.join(GRAPHQL_PATH, 'Resolvers', '__init__.py'): resolver_content_init,
        os.path.join(GRAPHQL_PATH, 'Resolvers', f'{app}Resolver.py'): resolver_content,
        os.path.join(SCHEMAS_PATH, app, 'Query.graphql'): query_graphql,
        os.path.join(SCHEMAS_PATH, app, 'Mutation.graphql'): mutation_graphql,
        os.path.join(SCHEMAS_PATH, 'Response.graphql'): response_content,
        os.path.join(INFRA_PATH, 'Repositories', app, '__init__.py'): repository_init_content,
        os.path.join(INFRA_PATH, 'Repositories', app, f'{app}Repository.py'): repository_content
    }
    for file_path in files:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    for file_path, content in files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(content)

    logger.info(Message.HEXAGONAL_SERVICE_CREATED_MSG)

@cli.command()
@click.argument('port')
def start(port:int):
    """Levantar el servidor FastAPI."""
    try:
        subprocess.run(['uvicorn', 'app:app', '--port', str(port), '--reload'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'{Message.SERVER_NETWORK_ACCESS_ERROR_MSG}: {e}')


@cli.command()
@click.argument('port')
def serve(port:int):
    """Levantar el servidor FastAPI accesible desde cualquier máquina."""
    try:
        # Levanta el servidor en el puerto n accesible desde cualquier IP
        subprocess.run(['uvicorn', 'app:app', '--host', '0.0.0.0', '--port', str(port), '--reload'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'{Message.SERVER_NETWORK_ACCESS_ERROR_MSG}: {e}')


@cli.command()
@click.argument('redis_env')
async def clean_redis(redis_env:str):
    try:
        from Osdental.RedisCache.Redis import RedisCacheAsync
        redis_url = os.getenv(redis_env)
        if not redis_url:
            logger.warning(f'Environment variable not found: {redis_env}')
            return
        
        redis = RedisCacheAsync(redis_url=redis_url)
        await redis.flush()
        logger.info(Message.REDIS_CLEANUP_SUCCESS_MSG)
    except Exception as e:
        logger.error(f'{Message.REDIS_CLEANUP_ERROR_MSG}: {e}')


if __name__ == "__main__":
    cli()
