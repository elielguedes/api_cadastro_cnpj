"""
Integração AWS Lambda com FastAPI
Arquivo: app/services/lambda_service.py
Autor: Eliel Guedes
"""

import json
import boto3
import asyncio
from typing import Dict, Any, Optional
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class LambdaService:
    """
    Serviço para integração com funções Lambda
    """
    
    def __init__(self, region_name: str = "us-east-2"):
        self.region_name = region_name
        self.lambda_client = boto3.client('lambda', region_name=region_name)
    
    async def validate_cnpj_async(self, cnpj: str) -> Dict[str, Any]:
        """
        Valida CNPJ usando função Lambda assíncrona
        """
        try:
            payload = {
                'cnpj': cnpj
            }
            
            # Invocar Lambda de forma assíncrona
            response = await asyncio.to_thread(
                self.lambda_client.invoke,
                FunctionName='validate-cnpj-api',
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            # Processar resposta
            response_payload = json.loads(response['Payload'].read())
            
            if response['StatusCode'] == 200:
                return json.loads(response_payload['body'])
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro na validação Lambda: {response_payload}"
                )
                
        except Exception as e:
            logger.error(f"Erro chamando Lambda validate-cnpj-api: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro na validação assíncrona: {str(e)}"
            )
    
    async def process_csv_file(self, csv_content: str, chunk_size: int = 100) -> Dict[str, Any]:
        """
        Processa arquivo CSV usando função Lambda
        """
        try:
            payload = {
                'csv_content': csv_content,
                'chunk_size': chunk_size,
                'output_bucket': 'cnpj-processed-data',  # Configurar seu bucket
                'output_key': f'processed/csv_processed_{int(asyncio.get_event_loop().time())}.json'
            }
            
            # Invocar Lambda
            response = await asyncio.to_thread(
                self.lambda_client.invoke,
                FunctionName='import-csv-processor',
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            response_payload = json.loads(response['Payload'].read())
            
            if response['StatusCode'] == 200:
                return json.loads(response_payload['body'])
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro no processamento CSV: {response_payload}"
                )
                
        except Exception as e:
            logger.error(f"Erro chamando Lambda import-csv-processor: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro no processamento de arquivo: {str(e)}"
            )
    
    async def generate_report(self, empresas_data: Optional[list] = None) -> Dict[str, Any]:
        """
        Gera relatório usando função Lambda
        """
        try:
            payload = {
                'empresas_data': empresas_data or [],
                's3_bucket': 'cnpj-reports',  # Configurar seu bucket
                'sns_topic_arn': ''  # Configurar seu SNS topic se necessário
            }
            
            # Invocar Lambda
            response = await asyncio.to_thread(
                self.lambda_client.invoke,
                FunctionName='generate-reports',
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            response_payload = json.loads(response['Payload'].read())
            
            if response['StatusCode'] == 200:
                return json.loads(response_payload['body'])
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro na geração de relatório: {response_payload}"
                )
                
        except Exception as e:
            logger.error(f"Erro chamando Lambda generate-reports: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro na geração de relatório: {str(e)}"
            )
    
    def invoke_lambda_sync(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoca função Lambda de forma síncrona (para casos específicos)
        """
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            response_payload = json.loads(response['Payload'].read())
            
            if response['StatusCode'] == 200:
                return json.loads(response_payload['body'])
            else:
                raise Exception(f"Lambda error: {response_payload}")
                
        except Exception as e:
            logger.error(f"Erro invocando Lambda {function_name}: {e}")
            raise


# Instância global do serviço
lambda_service = LambdaService()