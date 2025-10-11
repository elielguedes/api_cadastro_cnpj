"""
Pacote de serviços para lógica de negócio da aplicação.

Este módulo organiza os serviços que implementam operações CRUD e lógica de negócio:

- empresa_service.py: Operações relacionadas às empresas
- estabelecimento_service.py: Operações relacionadas aos estabelecimentos  
- socio_service.py: Operações relacionadas aos sócios

Os serviços abstraem a lógica de acesso aos dados dos routers/controllers,
implementando padrões como Repository/Service Layer para:
- Separar responsabilidades entre apresentação (routers) e dados (models)
- Facilitar testes unitários
- Reutilizar lógica de negócio em diferentes contextos
- Manter código organizado e manutenível

Cada serviço encapsula operações CRUD específicas e validações de negócio.
"""