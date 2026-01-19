# Transmissão de mensagem com gRPC

## 📌 Introdução

Este projeto apresenta um **estudo de caso sobre a transmissão de dados utilizando gRPC**, demonstrando a comunicação entre sistemas desenvolvidos em **Python** e **Node.js**. O objetivo é evidenciar o uso do gRPC como alternativa eficiente ao modelo tradicional REST, especialmente em arquiteturas de microsserviços.

O estudo implementa a transmissão de **mensagens de texto** entre um servidor em **Python** e um cliente intermediário em **Node.js**, com uma **interface web** para interação do usuário.

---

## 🎯 Objetivos do Projeto

* Implementa comunicação **exclusiva via gRPC** entre serviços
* Utiliza **Python** e **Node.js**
* Garante interoperabilidade por meio de **Protocol Buffers**
* Disponibiliza uma **interface gráfica intuitiva** para o usuário
* Demonstra um cenário real de **API Gateway**

---

## 🧠 Arquitetura da Solução

A arquitetura adotada segue o padrão de **API Gateway**, amplamente utilizado em sistemas distribuídos:

```
[ Interface Web ]
        ↓ HTTP
[ Node.js (API Gateway) ]
        ↓ gRPC
[ Servidor Python ]
```

### Descrição das Camadas

* **Interface Web (HTML + CSS)**
  Responsável pela interação com o usuário.

* **Node.js (Gateway)**
  Recebe requisições HTTP da interface e realiza a comunicação gRPC com o servidor Python.

* **Servidor Python (gRPC)**
  Processa a mensagem recebida e retorna uma resposta via gRPC.

---

## 🧩 Tecnologias Utilizadas

* **gRPC** – Comunicação remota de alta performance
* **Protocol Buffers (protobuf)** – Definição do contrato de dados
* **Python** – Implementação do servidor gRPC
* **Node.js** – Implementação do API Gateway
* **HTML e CSS** – Interface gráfica

---

## 📁 Estrutura do Projeto

```
grpc-estudo-caso/
├── proto/
│   └── mensagem.proto
├── servidor-python/
│   └── server.py
└── cliente-node/
    ├── server.js
    ├── index.html
    ├── package.json
    └── node_modules/
```

---

## 📄 Definição do Contrato gRPC

O arquivo `.proto` define o serviço e as mensagens trocadas entre os sistemas.

```proto
syntax = "proto3";

package mensagem;

service MensagemService {
  rpc EnviarMensagem (MensagemRequest) returns (MensagemResponse);
}

message MensagemRequest {
  string texto = 1;
}

message MensagemResponse {
  string resposta = 1;
}
```

---

## ⚙️ Funcionamento do Sistema

1. O usuário digita uma mensagem na interface web
2. A interface envia a mensagem via HTTP para o Node.js
3. O Node.js encaminha a mensagem ao servidor Python usando gRPC
4. O servidor Python processa a mensagem e retorna uma resposta
5. A resposta é exibida na interface web

---

## ▶️ Execução do Projeto

### 1️⃣ Iniciar o Servidor Python

```bash
cd servidor-python
python server.py
```

### 2️⃣ Iniciar o Gateway Node.js

```bash
cd cliente-node
node server.js
```

### 3️⃣ Acessar a Interface

Abra o navegador e acesse:

```
http://localhost:3000
```

---

## ✅ Resultados Obtidos

* Comunicação bem-sucedida entre Python e Node.js
* Transmissão de dados realizada exclusivamente via gRPC
* Interface intuitiva para envio e recebimento de mensagens
* Arquitetura modular e desacoplada


