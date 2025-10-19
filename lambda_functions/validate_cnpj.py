"""
AWS Lambda Function: Validação Assíncrona de CNPJ
Autor: Eliel Guedes
Descrição: Valida CNPJ usando algoritmo matemático e consulta APIs externas
"""

import json
import re
import boto3
import requests
from typing import Dict, Any


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ usando algoritmo oficial da Receita Federal
    """
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se não são todos os dígitos iguais
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validação do primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = sum(int(cnpj[i]) * multiplicadores1[i] for i in range(12))
    resto1 = soma1 % 11
    digito1 = 0 if resto1 < 2 else 11 - resto1
    
    if int(cnpj[12]) != digito1:
        return False
    
    # Validação do segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma2 = sum(int(cnpj[i]) * multiplicadores2[i] for i in range(13))
    resto2 = soma2 % 11
    digito2 = 0 if resto2 < 2 else 11 - resto2
    
    return int(cnpj[13]) == digito2


def consultar_cnpj_receita(cnpj: str) -> Dict[str, Any]:
    """
    Consulta dados da empresa na Receita Federal (API pública)
    """
    try:
        # API pública da Receita Federal
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'OK':
                return {
                    'found': True,
                    'razao_social': data.get('nome', ''),
                    'nome_fantasia': data.get('fantasia', ''),
                    'situacao': data.get('situacao', ''),
                    'atividade_principal': data.get('atividade_principal', [{}])[0].get('text', ''),
                    'endereco': {
                        'logradouro': data.get('logradouro', ''),
                        'numero': data.get('numero', ''),
                        'bairro': data.get('bairro', ''),
                        'municipio': data.get('municipio', ''),
                        'uf': data.get('uf', ''),
                        'cep': data.get('cep', '')
                    }
                }
        
        return {'found': False, 'error': 'CNPJ não encontrado na Receita Federal'}
        
    except Exception as e:
        return {'found': False, 'error': f'Erro na consulta: {str(e)}'}


def lambda_handler(event, context):
    """
    Handler principal da função Lambda
    """
    try:
        # Extrair CNPJ do evento
        cnpj = event.get('cnpj', '')
        
        if not cnpj:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'CNPJ é obrigatório',
                    'valid': False
                })
            }
        
        # Validação matemática
        is_valid = validar_cnpj(cnpj)
        
        result = {
            'cnpj': cnpj,
            'valid': is_valid,
            'timestamp': context.aws_request_id,
            'function_name': context.function_name
        }
        
        # Se válido, consultar dados na Receita
        if is_valid:
            receita_data = consultar_cnpj_receita(cnpj)
            result['receita_federal'] = receita_data
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Erro interno: {str(e)}',
                'valid': False
            })
        }


# Função de teste local
if __name__ == "__main__":
    # Teste local
    test_event = {
        'cnpj': '11.222.333/0001-81'
    }
    
    class MockContext:
        aws_request_id = 'test-request-123'
        function_name = 'validate-cnpj-local'
    
    result = lambda_handler(test_event, MockContext())
    print(json.dumps(json.loads(result['body']), indent=2, ensure_ascii=False))