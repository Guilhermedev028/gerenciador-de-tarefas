from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from src.database import listar_tarefas  # Importe a função listar_tarefas


SCOPES = ['https://www.googleapis.com/auth/calendar']

def autenticar_google():
    creds = None
    # O arquivo token.json armazena o token de acesso do usuário.
    # Se o arquivo existir, carrega as credenciais salvas.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Se não tiver credenciais válidas ou elas expiraram, pede o login do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # O arquivo credentials.json precisa ser configurado corretamente.
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salva as credenciais para o próximo uso
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds

def sincronizar_tarefas_com_google():
    # O resto do seu código permanece igual
    creds = autenticar_google()

    if not creds or not creds.valid:
        print("Falha na autenticação.")
        return

    service = build('calendar', 'v3', credentials=creds)
    
    # Agora, listar_tarefas deve ser encontrada no módulo database.py
    tarefas = listar_tarefas()

    for tarefa in tarefas:
        titulo = tarefa[1]
        descricao = tarefa[2]
        data_hora = tarefa[3]

        try:
            print(f"Processando tarefa: {titulo} - {data_hora}")
            inicio_data_hora = datetime.strptime(data_hora, '%Y-%m-%d %H:%M')
        except ValueError:
            print(f"Erro de formato para tarefa '{titulo}': {data_hora}")
            continue

        fim_data_hora = inicio_data_hora + timedelta(hours=1)

        evento_google = {
            'summary': titulo,
            'description': descricao,
            'start': {
                'dateTime': inicio_data_hora.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': fim_data_hora.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }

        try:
            evento = service.events().insert(calendarId='primary', body=evento_google).execute()
            print(f"Evento criado: {evento['htmlLink']}")
        except Exception as e:
            print(f"Erro ao criar evento: {e}")