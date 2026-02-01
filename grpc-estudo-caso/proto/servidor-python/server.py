
import grpc
from concurrent import futures
import mensagem_pb2
import mensagem_pb2_grpc
from datetime import datetime
import time
import threading
import queue

# Armazena a conexão com o cliente (apenas 1)
cliente_conectado = None
lock_cliente = threading.Lock()

# Fila para mensagens do servidor para o cliente
fila_mensagens_servidor = queue.Queue()


class MensagemServicer(mensagem_pb2_grpc.MensagemServiceServicer):
    """Implementação do serviço para comunicação com um único cliente"""

    def ComunicacaoBidirecional(self, request_iterator, context):
        """
        Implementa comunicação bidirecional entre 2 computadores.
        Computador A (cliente) envia e recebe do Computador B (servidor).
        """
        global cliente_conectado
        
        cliente_id = id(context)
        
        with lock_cliente:
            if cliente_conectado is not None:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Cliente já conectado!")
                print(f"   Nova tentativa de conexão rejeitada.\n")
                context.abort(grpc.StatusCode.RESOURCE_EXHAUSTED, "Apenas um cliente permitido")
                return
            
            cliente_conectado = {
                "id": cliente_id,
                "timestamp": time.time(),
                "context": context,
            }
        
        timestamp_conexao = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp_conexao}] ✅ Cliente (Computador A) conectado!")
        print(f"   ID: {cliente_id}")
        print(f"   Status: Aguardando mensagens...\n")
        print(f"   💡 Você pode digitar mensagens abaixo para enviar ao cliente!\n")

        try:
            # Thread para enviar mensagens que o servidor digita
            def enviar_mensagens_servidor():
                while cliente_conectado is not None:
                    try:
                        # Tenta pegar mensagem da fila (com timeout)
                        mensagem = fila_mensagens_servidor.get(timeout=0.5)
                        if mensagem is None:  # Sinal para parar
                            break
                        
                        resposta = mensagem_pb2.MensagemResponse(
                            resposta=mensagem,
                            remetente="SERVIDOR_B",
                            timestamp=int(time.time() * 1000),
                            status="enviada"
                        )
                        yield resposta
                    except queue.Empty:
                        continue
                    except Exception as e:
                        print(f" Erro ao enviar mensagem do servidor: {e}")
            
            # Combina: recebe do cliente + envia mensagens do servidor
            enviador = enviar_mensagens_servidor()
            
            for requisicao in request_iterator:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] 📨 Mensagem recebida de {requisicao.remetente}:")
                print(f"   \"{requisicao.texto}\"\n")

                # Envia confirmação de recebimento
                try:
                    resposta_confirmacao = mensagem_pb2.MensagemResponse(
                        resposta="Mensagem recebida pelo Servidor (Computador B)",
                        remetente="SERVIDOR_B",
                        timestamp=int(time.time() * 1000),
                        status="confirmada"
                    )
                    yield resposta_confirmacao
                except Exception as e:
                    print(f"  Erro ao enviar confirmação: {e}")
                
                # Também envia mensagens que estão na fila
                while not fila_mensagens_servidor.empty():
                    try:
                        mensagem = fila_mensagens_servidor.get_nowait()
                        if mensagem is not None:
                            resposta = mensagem_pb2.MensagemResponse(
                                resposta=mensagem,
                                remetente="SERVIDOR_B",
                                timestamp=int(time.time() * 1000),
                                status="enviada"
                            )
                            yield resposta
                    except queue.Empty:
                        break

        except grpc.RpcError as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro gRPC: {e}")
        finally:
            with lock_cliente:
                cliente_conectado = None
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Cliente desconectado")
            print(f"   Servidor aguardando nova conexão...\n")

    def EnviarMensagem(self, request, context):
        """
        Método compatível com versão anterior.
        Processa uma mensagem única sem streaming.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 📨 Mensagem HTTP recebida: {request.texto}\n")
        
        return mensagem_pb2.MensagemResponse(
            resposta=f"Servidor Python (Computador B) recebeu: {request.texto}",
            remetente="SERVIDOR_B",
            timestamp=int(time.time() * 1000),
            status="processada"
        )


def servir():
    """Inicia o servidor gRPC no Computador B"""
    porta = 50051
    
    # Cria o servidor gRPC
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_concurrent_streams', 100),
        ]
    )
    
    # Adiciona o serviço
    mensagem_pb2_grpc.add_MensagemServiceServicer_to_server(
        MensagemServicer(), server
    )

    # Configura a escuta
    server.add_insecure_port(f'[::]:{porta}')
    server.start()
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║      🖥️  Computador B - Servidor gRPC Python               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

🚀 Servidor iniciado em [::]:50051
📍 Compartilhe este IP com o Computador A para conectar
⏳ Aguardando conexão do Computador A (Cliente)...\n""")
    
    # Thread para ler inputs do servidor
    def thread_input_servidor():
        """Lê mensagens do terminal do servidor e envia para o cliente"""
        while True:
            try:
                with lock_cliente:
                    if cliente_conectado is None:
                        continue
                
                # Lê input do usuário
                mensagem = input(f"\n[SERVIDOR] Digite uma mensagem (ou 'sair'): ").strip()
                
                if mensagem.lower() == 'sair':
                    print("Encerrando servidor...")
                    server.stop(grace=5)
                    break
                
                if mensagem and cliente_conectado is not None:
                    fila_mensagens_servidor.put(mensagem)
                    print(f"Enviando para cliente: {mensagem}\n")
                    
            except EOFError:
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("\n\nEncerrando servidor...")
                server.stop(grace=5)
                break
            except Exception as e:
                print(f"Erro: {e}")
    
    # Inicia thread de input
    input_thread = threading.Thread(target=thread_input_servidor, daemon=True)
    input_thread.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n\nEncerrando servidor...")
        server.stop(grace=5)
        print("Servidor encerrado com sucesso\n")


if __name__ == "__main__":
    servir()

