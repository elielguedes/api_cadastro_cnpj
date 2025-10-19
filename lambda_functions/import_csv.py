"""
AWS Lambda Function: Processador de Arquivos CSV
Autor: Eliel Guedes
Descrição: Processa arquivos CSV grandes de forma assíncrona
"""

import json
import csv
import io
import boto3
from datetime import datetime
from typing import Dict, List, Any


def process_csv_chunk(csv_content: str, chunk_size: int = 100) -> Dict[str, Any]:
    """
    Processa um chunk do arquivo CSV
    """
    processed_records = []
    errors = []
    
    try:
        # Criar reader do CSV
        csv_reader = csv.DictReader(io.StringIO(csv_content), delimiter=';')
        
        count = 0
        for row in csv_reader:
            if count >= chunk_size:
                break
                
            try:
                # Processar linha
                processed_record = {
                    'cnpj': row.get('cnpj', '').strip(),
                    'razao_social': row.get('razao_social', '').strip(),
                    'nome_fantasia': row.get('nome_fantasia', '').strip(),
                    'situacao': row.get('situacao', '').strip(),
                    'data_situacao': row.get('data_situacao', '').strip(),
                    'motivo_situacao': row.get('motivo_situacao', '').strip(),
                    'nm_cidade_exterior': row.get('nm_cidade_exterior', '').strip(),
                    'pais': row.get('pais', '').strip(),
                    'nome_pais': row.get('nome_pais', '').strip(),
                    'codigo_natureza_juridica': row.get('codigo_natureza_juridica', '').strip(),
                    'data_inicio_atividade': row.get('data_inicio_atividade', '').strip(),
                    'cnae_fiscal': row.get('cnae_fiscal', '').strip(),
                    'descricao_tipo_logradouro': row.get('descricao_tipo_logradouro', '').strip(),
                    'logradouro': row.get('logradouro', '').strip(),
                    'numero': row.get('numero', '').strip(),
                    'complemento': row.get('complemento', '').strip(),
                    'bairro': row.get('bairro', '').strip(),
                    'cep': row.get('cep', '').strip(),
                    'uf': row.get('uf', '').strip(),
                    'codigo_municipio': row.get('codigo_municipio', '').strip(),
                    'municipio': row.get('municipio', '').strip(),
                    'ddd_telefone_1': row.get('ddd_telefone_1', '').strip(),
                    'telefone_1': row.get('telefone_1', '').strip(),
                    'ddd_telefone_2': row.get('ddd_telefone_2', '').strip(),
                    'telefone_2': row.get('telefone_2', '').strip(),
                    'ddd_fax': row.get('ddd_fax', '').strip(),
                    'fax': row.get('fax', '').strip(),
                    'correio_eletronico': row.get('correio_eletronico', '').strip(),
                    'qualificacao_responsavel': row.get('qualificacao_responsavel', '').strip(),
                    'capital_social': row.get('capital_social', '').strip(),
                    'porte': row.get('porte', '').strip(),
                    'opcao_pelo_simples': row.get('opcao_pelo_simples', '').strip(),
                    'data_opcao_pelo_simples': row.get('data_opcao_pelo_simples', '').strip(),
                    'data_exclusao_do_simples': row.get('data_exclusao_do_simples', '').strip(),
                    'opcao_pelo_mei': row.get('opcao_pelo_mei', '').strip(),
                    'situacao_especial': row.get('situacao_especial', '').strip(),
                    'data_situacao_especial': row.get('data_situacao_especial', '').strip()
                }
                
                # Validar CNPJ básico
                if processed_record['cnpj'] and len(processed_record['cnpj'].replace('.', '').replace('/', '').replace('-', '')) == 14:
                    processed_records.append(processed_record)
                else:
                    errors.append(f"CNPJ inválido na linha {count + 1}: {processed_record['cnpj']}")
                
                count += 1
                
            except Exception as e:
                errors.append(f"Erro processando linha {count + 1}: {str(e)}")
                continue
        
        return {
            'success': True,
            'processed_count': len(processed_records),
            'error_count': len(errors),
            'records': processed_records,
            'errors': errors[:10]  # Limitar erros para não estourar payload
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Erro geral no processamento: {str(e)}",
            'processed_count': 0,
            'error_count': 1
        }


def save_to_s3(bucket_name: str, key: str, data: Any) -> bool:
    """
    Salva dados processados no S3
    """
    try:
        s3_client = boto3.client('s3')
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(data, ensure_ascii=False, indent=2),
            ContentType='application/json'
        )
        
        return True
        
    except Exception as e:
        print(f"Erro salvando no S3: {e}")
        return False


def lambda_handler(event, context):
    """
    Handler principal da função Lambda
    """
    try:
        # Extrair parâmetros do evento
        csv_content = event.get('csv_content', '')
        chunk_size = event.get('chunk_size', 100)
        output_bucket = event.get('output_bucket', '')
        output_key = event.get('output_key', '')
        
        if not csv_content:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'error': 'csv_content é obrigatório'
                })
            }
        
        # Processar CSV
        result = process_csv_chunk(csv_content, chunk_size)
        
        # Adicionar metadados
        result['timestamp'] = datetime.utcnow().isoformat()
        result['request_id'] = context.aws_request_id
        result['function_name'] = context.function_name
        
        # Salvar no S3 se especificado
        if output_bucket and output_key:
            s3_saved = save_to_s3(output_bucket, output_key, result)
            result['s3_saved'] = s3_saved
            result['s3_location'] = f"s3://{output_bucket}/{output_key}" if s3_saved else None
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': f'Erro interno: {str(e)}',
                'success': False
            })
        }


# Função de teste local
if __name__ == "__main__":
    # Teste local com dados simulados
    test_csv = """cnpj;razao_social;nome_fantasia;situacao
11.222.333/0001-81;EMPRESA TESTE LTDA;TESTE;ATIVA
22.333.444/0001-92;OUTRA EMPRESA SA;OUTRA;ATIVA"""
    
    test_event = {
        'csv_content': test_csv,
        'chunk_size': 10
    }
    
    class MockContext:
        aws_request_id = 'test-request-456'
        function_name = 'process-csv-local'
    
    result = lambda_handler(test_event, MockContext())
    print(json.dumps(json.loads(result['body']), indent=2, ensure_ascii=False))