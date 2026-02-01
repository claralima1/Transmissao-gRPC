

import grpc
import sys
import os
import time
from datetime import datetime
import threading

# Adiciona o diretório proto ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import mensagem_pb2
import mensagem_pb2_grpc


class ClienteGRPC:
    def __init__(self, endereco_servidor, nome_cliente="Computador-A"):
        """Inicializa o cliente gRPC"""
        self.endereco_servidor = endereco_servidor
        self.nome_cliente = nome_cliente
        self.canal = None
        self.stub = None
        self.stream = None
        self.conectado = False

    def conectar(self):
        """Conecta ao servidor gRPC remoto (Computador B)"""
        try:
            print(f"\n Conectando ao Computador B em {self.endereco_servidor}...")
            self.canal = grpc.insecure_channel(self.endereco_servidor)
            self.stub = mensagem_pb2_grpc.MensagemServiceStub(self.canal)
            print(f" Conectado com sucesso ao servidor em {self.endereco_servidor}")
            self.conectado = True
            return True
        except Exception as e:
            print(f" Erro ao conectar: {e}")
            self.conectado = False
            return False

    def criar_stream_bidirecional(self):
        """Cria um stream bidirecional com o servidor"""
        try:
            print("\n Iniciando comunicação bidirecional com Computador B...")
            
            def gerar_mensagens():
                """Gerador que envia mensagens para o servidor"""
                while self.conectado:
                    try:
                        # Obtém input do usuário
                        texto = input(f"\n[{self.nome_cliente}] Digite uma mensagem (ou 'sair'): ").strip()
                        
                        if texto.lower() == "sair":
                            self.conectado = False
                            break
                        
                        if texto:
                            mensagem = mensagem_pb2.MensagemRequest(
                                texto=texto,
                                remetente=self.nome_cliente,
                                timestamp=int(time.time() * 1000)
                            )
                            print(f"  Enviando para Computador B: {texto}")
                            yield mensagem
                    except EOFError:
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"   Erro ao enviar: {e}")

            # Chama o método de streaming bidirecional
            self.stream = self.stub.ComunicacaoBidirecional(gerar_mensagens())
            
            # Thread para receber mensagens
            thread_receber = threading.Thread(target=self.receber_mensagens, daemon=True)
            thread_receber.start()
            
            # Aguarda a thread
            thread_receber.join()
            
        except grpc.RpcError as e:
            print(f" Erro gRPC: {e.code()} - {e.details()}")
        except Exception as e:
            print(f" Erro: {e}")

    def receber_mensagens(self):
        """Recebe mensagens do Computador B"""
        try:
            for resposta in self.stream:
                timestamp = datetime.fromtimestamp(resposta.timestamp / 1000).strftime("%H:%M:%S")
                
                emoji = "📨"
                if resposta.status == "confirmada":
                    emoji = "✅"
                elif resposta.status == "erro":
                    emoji = "❌"
                
                print(f"\n{emoji} [{timestamp}] {resposta.remetente}: {resposta.resposta}")
                print(f"   [{self.nome_cliente}] >>> ", end="", flush=True)
                
        except grpc.RpcError as e:
            print(f"\n, Erro ao receber mensagens: {e.code()} - {e.details()}")
        except Exception as e:
            print(f"\n Erro: {e}")
        finally:
            self.conectado = False

    def desconectar(self):
        """Desconecta do servidor"""
        try:
            if self.stream:
                self.stream.cancel()
            print("\n Desconectado do Computador B")
        except Exception as e:
            print(f" Erro ao desconectar: {e}")


def main():
    """Função principal - Computador A (Cliente)"""
    print("""
╔════════════════════════════════════════════════════════════╗
║      🖥️  Computador A - Cliente gRPC Python                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Obtém configurações do usuário
    servidor_padrao = os.getenv("SERVIDOR_GRPC", "localhost:50051")
    endereco = input(f"Digite o IP:porta do Computador B [{servidor_padrao}]: ").strip() or servidor_padrao
    
    nome = input("Digite seu nome [Computador-A]: ").strip() or "Computador-A"
    
    # Cria cliente
    cliente = ClienteGRPC(endereco, nome)
    
    # Conecta ao servidor
    if not cliente.conectar():
        print(" Falha ao conectar. Verifique o endereço do Computador B.")
        return
    
    try:
        # Inicia comunicação bidirecional
        cliente.criar_stream_bidirecional()
    except KeyboardInterrupt:
        print("\n\n Encerrando Cliente...")
    finally:
        cliente.desconectar()


if __name__ == "__main__":
    main()
