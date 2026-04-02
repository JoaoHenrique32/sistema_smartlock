from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import base64
import numpy as np
import cv2
import paho.mqtt.client as mqtt
import os
from deepface import DeepFace

# ... (mantenha os imports e as funções de API identify_face e register_face que já fizemos)

# --- CONFIGURAÇÃO MQTT ---
MQTT_BROKER = "localhost"
MQTT_TOPIC = "t/fechadura"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
except Exception as e:
    print("Aviso: MQTT não conectou. Docker está ligado?")
    
def index(request):
    """Renderiza a página principal com a lista de usuários cadastrados"""
    db_path = os.path.join(settings.BASE_DIR, "banco_rostos")
    usuarios_cadastrados = []
    
    if os.path.exists(db_path):
        # Lista arquivos .jpg e remove a extensão para exibir o nome
        for arquivo in os.listdir(db_path):
            if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                nome = os.path.splitext(arquivo)[0]
                usuarios_cadastrados.append(nome)
                
    return render(request, 'index.html', {'usuarios': usuarios_cadastrados})

@csrf_exempt
def delete_face(request):
    """Recebe o nome via POST e deleta a foto correspondente"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_usuario = data.get('nome')
            
            # Caminho da foto (ajuste a extensão se necessário)
            caminho_arquivo = os.path.join(settings.BASE_DIR, "banco_rostos", f"{nome_usuario}.jpg")
            
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
                return JsonResponse({"status": "sucesso", "mensagem": f"Usuário {nome_usuario} removido!"})
            else:
                return JsonResponse({"status": "erro", "mensagem": "Arquivo não encontrado."})
                
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)})

    return JsonResponse({"status": "invalido"})

# O @csrf_exempt permite que o site envie dados sem dar erro de segurança na fase de testes
@csrf_exempt 
def identify_face(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]

            # Converte a imagem do site para o padrão OpenCV
            img_bytes = base64.b64decode(image_data)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Aponta para a pasta onde o botão azul está salvando as fotos
            db_path = os.path.join(settings.BASE_DIR, "banco_rostos")
            
            # Trava de segurança: e se a pasta estiver vazia?
            if not os.path.exists(db_path) or len(os.listdir(db_path)) == 0:
                return JsonResponse({"status": "erro", "mensagem": "O banco de dados está vazio. Cadastre alguém primeiro!"})

            print("Procurando rosto no banco de dados...")
            
            # O coração da IA: Compara a foto da câmera com a pasta
            results = DeepFace.find(img_path=frame, db_path=db_path, enforce_detection=False, model_name="VGG-Face")

            # Verifica se encontrou alguém (O DeepFace retorna uma lista de DataFrames)
            if len(results) > 0 and not results[0].empty:
                
                # Pega o caminho completo do arquivo (Ex: C:\...\banco_rostos\joao.jpg)
                caminho_completo = results[0]['identity'][0]
                
                # Extrai só o nome do arquivo (Ex: joao.jpg)
                nome_arquivo = os.path.basename(caminho_completo)
                
                # Tira a extensão .jpg para pegar só o nome (Ex: joao)
                usuario = os.path.splitext(nome_arquivo)[0]
                
                print(f"ACESSO LIBERADO: {usuario}")
                
                # Envia o comando MQTT com o nome REAL de quem está na câmera
                msg = f'{{"aluno": "{usuario}", "status": "LIBERADO"}}'
                client.publish(MQTT_TOPIC, msg)
                
                # Responde para o site exibir o Pop-up com o nome!
                return JsonResponse({"status": "sucesso", "mensagem": f"Acesso Liberado! Bem-vindo(a), {usuario}."})
            
            else:
                print("ACESSO NEGADO: Desconhecido")
                msg = '{"aluno": "Desconhecido", "status": "NEGADO"}'
                client.publish(MQTT_TOPIC, msg)
                return JsonResponse({"status": "erro", "mensagem": "Acesso Negado: Rosto não reconhecido."})

        except Exception as e:
            print(f"Erro na identificação: {e}")
            return JsonResponse({"status": "erro", "mensagem": str(e)})

    return JsonResponse({"status": "invalido"})

@csrf_exempt 
def register_face(request):
    if request.method == 'POST':
        try:
            # 1. Recebe os dados
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            nome_usuario = data['nome'].strip() # Tira espaços em branco do nome

            # 2. Usa a pasta raiz do seu projeto Django (onde está o manage.py)
            db_path = os.path.join(settings.BASE_DIR, "banco_rostos")
            
            # Cria a pasta se não existir
            if not os.path.exists(db_path):
                os.makedirs(db_path)
                print(f"📁 Pasta criada em: {db_path}")

            # 3. Converte e Salva
            img_bytes = base64.b64decode(image_data)
            caminho_arquivo = os.path.join(db_path, f"{nome_usuario}.jpg")

            with open(caminho_arquivo, "wb") as arquivo_foto:
                arquivo_foto.write(img_bytes)

            # 4. Avisa no terminal do VS Code exatamente onde salvou!
            print(f"✅ SUCESSO! Foto salva exatamente aqui: {caminho_arquivo}")

            return JsonResponse({"status": "sucesso", "mensagem": f"Rosto de {nome_usuario} salvo no banco!"})

        except Exception as e:
            print(f"❌ ERRO NO PYTHON: {e}")
            return JsonResponse({"status": "erro", "mensagem": str(e)})

    return JsonResponse({"status": "invalido"})

