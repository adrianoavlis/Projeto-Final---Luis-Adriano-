# Projeto: Refatoração do módulo Painel (com SQL Server)

## Repositório
https://github.com/adrianoavlis/ProjetoFinal-LuisAdriano.git

## Escopo
Refatorar o módulo:
app/Painel

## Objetivo
Modernizar a arquitetura mantendo TOTAL compatibilidade com o banco existente.

## Banco de dados

- Banco: SQL Server
- A estrutura do banco NÃO deve ser alterada
- Os dados existentes devem ser preservados
- Queries devem continuar compatíveis com a branch principal

## Regra crítica

⚠️ NÃO modificar:
- nomes de tabelas
- nomes de colunas
- procedures existentes
- contratos de dados já utilizados

A refatoração deve acontecer APENAS na camada de aplicação.

## Stack obrigatória

- FastAPI
- Pydantic
- SQLAlchemy (com suporte a SQL Server)
- Pytest

## Conexão com SQL Server

Utilizar:
- driver ODBC (pyodbc)

Exemplo de connection string:
mssql+pyodbc://user:password@server/database?driver=ODBC+Driver+17+for+SQL+Server

## Arquitetura alvo

app/
  painel/
    domain/
    application/
    infrastructure/
      database/
      repositories/
    presentation/
    schemas/

## Diretrizes

- Regras de negócio → domain
- Banco → apenas via repository
- Controllers → sem lógica

## Estratégia

1. Mapear queries atuais do Painel
2. Criar repositories equivalentes
3. Encapsular acesso ao SQL Server
4. Migrar lógica para use cases
5. Criar API moderna sem alterar comportamento

## Resultado esperado

- Mesmo comportamento da aplicação atual
- Código desacoplado
- Banco intacto