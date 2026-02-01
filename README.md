# 🚀 Comunicação gRPC entre Dois Computadores

## 📋 Visão Geral

Este projeto implementa **comunicação bidirecional simples** entre **2 computadores** usando **gRPC**:

- **Computador A**: Cliente Python que conecta ao servidor
- **Computador B**: Servidor Python que aguarda conexão

Ambos podem enviar e receber mensagens **simultaneamente**.

---

## 🧩 Arquitetura

```
┌──────────────────────┐          ┌──────────────────────┐
│   Computador A       │          │   Computador B       │
│   (Cliente)          │          │   (Servidor)         │
│                      │          │                      │
│ ┌─────────────────┐  │ gRPC     │ ┌─────────────────┐  │
│ │ Python Client   │◄─┼──────────┼─┤ Python Server   │  │
│ │                 │  │ :50051   │ │                 │  │
│ └─────────────────┘  │          │ └─────────────────┘  │
│                      │          │                      │
│  Terminal/Entrada   │          │  Terminal/Entrada    │
└──────────────────────┘          └──────────────────────┘
```

---

## ⚙️ Instalação

### 1️⃣ Em ambos os computadores:

```bash
# Clone o repositório
git clone <seu-repo>
cd grpc-estudo-caso/proto/servidor-python

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## 🚀 Execução

### 📍 No Computador B (Servidor) - PRIMEIRO

```bash
cd grpc-estudo-caso/proto/servidor-python
source venv/bin/activate  # ou venv\Scripts\activate no Windows
python3 server.py
```


### 📍 No Computador A (Cliente) - DEPOIS

```bash
cd grpc-estudo-caso/proto/servidor-python
source venv/bin/activate  # ou venv\Scripts\activate no Windows
python3 cliente.py
```

**Você será solicitado:**
1. **IP do Computador B**: Digite o IP (ex: `192.168.1.100:50051`)
   - Se na mesma máquina: `localhost:50051`
2. **Seu nome**: Digite um identificador (ex: `Alice`)

---

## 💬 Como Usar

Após conectar, ambos podem digitar mensagens que serão entregues simultaneamente:

**Computador B (Servidor):**
```
[12:34:56] 📨 Mensagem recebida de Alice:
   "Olá, tudo bem?"

[12:34:58] ✅ Confirmação enviada
```

**Computador A (Cliente):**
```
[Alice] Digite uma mensagem (ou 'sair'): Olá, tudo bem?
   📤 Enviando para Computador B: Olá, tudo bem?

✅ [12:34:58] SERVIDOR_B: Mensagem recebida pelo Servidor (Computador B)
```

