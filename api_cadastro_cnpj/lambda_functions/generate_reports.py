"""
AWS Lambda Function: Gerador de Relatórios Automatizados
Autor: Eliel Guedes
Descrição: Gera relatórios estatísticos dos dados de empresas
"""

import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any


def generate_statistics_report(empresas_data: List[Dict]) -> Dict[str, Any]:
    """
    Gera estatísticas dos dados de empresas
    """
    try:
        total_empresas = len(empresas_data)
        
        # Estatísticas por situação
        situacoes = {}
        for empresa in empresas_data:
            situacao = empresa.get('situacao', 'NÃO INFORMADO')
            situacoes[situacao] = situacoes.get(situacao, 0) + 1
        
        # Estatísticas por UF
        ufs = {}
        for empresa in empresas_data:
            uf = empresa.get('uf', 'NÃO INFORMADO')
            ufs[uf] = ufs.get(uf, 0) + 1
        
        # Estatísticas por porte
        portes = {}
        for empresa in empresas_data:
            porte = empresa.get('porte', 'NÃO INFORMADO')
            portes[porte] = portes.get(porte, 0) + 1
        
        # Top 10 municípios
        municipios = {}
        for empresa in empresas_data:
            municipio = empresa.get('municipio', 'NÃO INFORMADO')
            municipios[municipio] = municipios.get(municipio, 0) + 1
        
        top_municipios = sorted(municipios.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Empresas do Simples Nacional
        simples_sim = sum(1 for emp in empresas_data if emp.get('opcao_pelo_simples', '').upper() == 'SIM')
        simples_nao = sum(1 for emp in empresas_data if emp.get('opcao_pelo_simples', '').upper() == 'NÃO')
        
        # MEI
        mei_sim = sum(1 for emp in empresas_data if emp.get('opcao_pelo_mei', '').upper() == 'SIM')
        mei_nao = sum(1 for emp in empresas_data if emp.get('opcao_pelo_mei', '').upper() == 'NÃO')
        
        return {
            'resumo_executivo': {
                'total_empresas': total_empresas,
                'data_geracao': datetime.utcnow().isoformat(),
                'periodo_analise': 'Dados atuais no sistema'
            },
            'distribuicao_situacao': situacoes,
            'distribuicao_uf': dict(sorted(ufs.items(), key=lambda x: x[1], reverse=True)[:10]),
            'distribuicao_porte': portes,
            'top_municipios': [{'municipio': mun, 'quantidade': qtd} for mun, qtd in top_municipios],
            'simples_nacional': {
                'optantes': simples_sim,
                'nao_optantes': simples_nao,
                'percentual_optantes': round((simples_sim / total_empresas) * 100, 2) if total_empresas > 0 else 0
            },
            'mei': {
                'optantes': mei_sim,
                'nao_optantes': mei_nao,
                'percentual_optantes': round((mei_sim / total_empresas) * 100, 2) if total_empresas > 0 else 0
            }
        }
        
    except Exception as e:
        return {
            'error': f'Erro gerando relatório: {str(e)}',
            'resumo_executivo': {
                'total_empresas': 0,
                'data_geracao': datetime.utcnow().isoformat(),
                'erro': True
            }
        }


def send_report_notification(report_data: Dict, sns_topic_arn: str = None) -> bool:
    """
    Envia notificação sobre relatório gerado (via SNS)
    """
    try:
        if not sns_topic_arn:
            return False
            
        sns_client = boto3.client('sns')
        
        resumo = report_data.get('resumo_executivo', {})
        
        message = f"""
📊 RELATÓRIO MENSAL DE EMPRESAS GERADO

📈 Resumo Executivo:
• Total de Empresas: {resumo.get('total_empresas', 0):,}
• Data de Geração: {resumo.get('data_geracao', 'N/A')}

🏢 Simples Nacional:
• Optantes: {report_data.get('simples_nacional', {}).get('optantes', 0):,}
• Percentual: {report_data.get('simples_nacional', {}).get('percentual_optantes', 0)}%

👨‍💼 MEI:
• Optantes: {report_data.get('mei', {}).get('optantes', 0):,}
• Percentual: {report_data.get('mei', {}).get('percentual_optantes', 0)}%

🗺️ Top 3 Estados:
"""
        
        # Adicionar top UFs
        ufs = report_data.get('distribuicao_uf', {})
        for i, (uf, qtd) in enumerate(list(ufs.items())[:3]):
            message += f"• {uf}: {qtd:,} empresas\n"
        
        message += "\n🤖 Relatório gerado automaticamente via AWS Lambda"
        
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='📊 Relatório Mensal - API Cadastro CNPJ'
        )
        
        return True
        
    except Exception as e:
        print(f"Erro enviando notificação: {e}")
        return False


def save_report_to_s3(report_data: Dict, bucket_name: str, key_prefix: str = "reports") -> Dict[str, str]:
    """
    Salva relatório no S3
    """
    try:
        s3_client = boto3.client('s3')
        
        # Nome do arquivo com timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{key_prefix}/relatorio_empresas_{timestamp}.json"
        
        # Salvar JSON
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=json.dumps(report_data, ensure_ascii=False, indent=2),
            ContentType='application/json',
            Metadata={
                'generated_by': 'lambda_generate_reports',
                'generation_date': datetime.utcnow().isoformat(),
                'total_companies': str(report_data.get('resumo_executivo', {}).get('total_empresas', 0))
            }
        )
        
        return {
            'success': True,
            'bucket': bucket_name,
            'key': filename,
            'url': f"s3://{bucket_name}/{filename}"
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def lambda_handler(event, context):
    """
    Handler principal da função Lambda
    """
    try:
        # Dados podem vir do evento ou ser buscados de uma fonte externa
        empresas_data = event.get('empresas_data', [])
        s3_bucket = event.get('s3_bucket', '')
        sns_topic = event.get('sns_topic_arn', '')
        
        # Se não há dados no evento, simular dados para demonstração
        if not empresas_data:
            empresas_data = [
                {
                    'cnpj': '11.111.111/0001-11',
                    'razao_social': 'EMPRESA EXEMPLO 1 LTDA',
                    'situacao': 'ATIVA',
                    'uf': 'SP',
                    'municipio': 'SÃO PAULO',
                    'porte': 'MICRO EMPRESA',
                    'opcao_pelo_simples': 'SIM',
                    'opcao_pelo_mei': 'NÃO'
                },
                {
                    'cnpj': '22.222.222/0001-22',
                    'razao_social': 'EMPRESA EXEMPLO 2 SA',
                    'situacao': 'ATIVA',
                    'uf': 'RJ',
                    'municipio': 'RIO DE JANEIRO',
                    'porte': 'PEQUENA EMPRESA',
                    'opcao_pelo_simples': 'NÃO',
                    'opcao_pelo_mei': 'NÃO'
                },
                {
                    'cnpj': '33.333.333/0001-33',
                    'razao_social': 'MEI EXEMPLO',
                    'situacao': 'ATIVA',
                    'uf': 'MG',
                    'municipio': 'BELO HORIZONTE',
                    'porte': 'MICRO EMPRESA',
                    'opcao_pelo_simples': 'SIM',
                    'opcao_pelo_mei': 'SIM'
                }
            ]
        
        # Gerar relatório
        report = generate_statistics_report(empresas_data)
        
        # Adicionar metadados
        report['metadata'] = {
            'lambda_request_id': context.aws_request_id,
            'function_name': context.function_name,
            'execution_time_remaining': context.get_remaining_time_in_millis(),
            'memory_limit': context.memory_limit_in_mb
        }
        
        # Salvar no S3 se especificado
        s3_result = {}
        if s3_bucket:
            s3_result = save_report_to_s3(report, s3_bucket)
            report['s3_storage'] = s3_result
        
        # Enviar notificação se especificado
        notification_sent = False
        if sns_topic:
            notification_sent = send_report_notification(report, sns_topic)
        
        report['notification_sent'] = notification_sent
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(report, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': f'Erro interno: {str(e)}',
                'success': False,
                'timestamp': datetime.utcnow().isoformat()
            })
        }


# Função de teste local
if __name__ == "__main__":
    # Teste local
    test_event = {
        'empresas_data': [],  # Usar dados simulados
        's3_bucket': 'meu-bucket-relatorios',
        'sns_topic_arn': 'arn:aws:sns:us-east-1:123456789:relatorios'
    }
    
    class MockContext:
        aws_request_id = 'test-request-789'
        function_name = 'generate-reports-local'
        memory_limit_in_mb = 128
        
        def get_remaining_time_in_millis(self):
            return 30000
    
    result = lambda_handler(test_event, MockContext())
    print(json.dumps(json.loads(result['body']), indent=2, ensure_ascii=False))