# 🔐 SmartLock - Sistema de Reconhecimento Facial IoT

O **SmartLock** é um sistema de controle de acesso inteligente que integra Visão Computacional, Desenvolvimento Web e IoT. O projeto utiliza IA para identificar usuários cadastrados e comandar a abertura de uma fechadura solenoide via MQTT.

---

## 🚀 Funcionalidades

* **Reconhecimento Facial:** Identificação em tempo real utilizando a biblioteca `DeepFace`.
* **Gestão de Usuários:** Interface administrativa para cadastrar novos rostos e revogar acessos.
* **Integração IoT:** Comunicação com NodeMCU ESP8266 para controle de hardware.
* **Logs de Acesso:** Persistência de dados em banco MySQL para auditoria.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.x, Django Framework.
* **IA/Visão:** OpenCV, DeepFace (VGG-Face).
* **Banco de Dados:** MySQL (via Docker).
* **Comunicação:** MQTT (Broker EMQX via Docker).
* **Hardware:** NodeMCU ESP8266, Módulo Relé, Solenoide 12V.

---

## 📦 Configuração e Instalação

### 1. Clonar o Repositório
```bash
git clone [https://github.com/JoaoHenrique32/sistema_smartlock](https://github.com/JoaoHenrique32/sistema_smartlock)
cd sistema_smartlock


2. Configurar o Ambiente Python
Recomenda-se o uso de um ambiente virtual:

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
.\venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate


3. Instalar Dependências

pip install -r requirements.txt


4. Subir Serviços (Docker)
O projeto utiliza Docker para gerenciar o Banco de Dados e o Broker MQTT:

docker-compose up -d

5. Executar o Sistema


Terminal
python manage.py migrate
python manage.py runserver


Acesse em: http://127.0.0.1:8000


🔌 Configuração de Hardware (NodeMCU)
Abra o código contido na pasta /hardware (ou o projeto Fechadura_NodeMCU git: https://github.com/JoaoHenrique32/Fechadura_NodeMCU).

Configure as variáveis de rede no código:

ssid: Nome do seu Wi-Fi (2.4GHz).

password: Senha do Wi-Fi.

mqtt_server: O endereço IP do seu computador na rede.

Faça o upload para o NodeMCU ESP8266.