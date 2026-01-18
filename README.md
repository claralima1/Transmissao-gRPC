# 📚 Transmissão de Mensagem de Texto com gRPC 

**Linguagens:** Python + Node.js  

---

## 🎯 Cenário  

Uma aplicação distribuída onde:

- Um servidor em **Python** recebe mensagens de texto  
- Um cliente em **Node.js** envia mensagens via **gRPC**  
- A comunicação ocorre usando **Protobuf**  
- A mensagem transmitida é um **texto simples**

---
### 🧭 Visão Geral da Arquitetura

```text
+-------------------+        gRPC / Protobuf        +-------------------+
|                   |  --------------------------> |                   |
|  Cliente Node.js  |                              |  Servidor Python  |
|                   |  <-------------------------- |                   |
+-------------------+        (Resposta opcional)    +-------------------+
