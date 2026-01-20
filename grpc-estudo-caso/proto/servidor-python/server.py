import grpc
from concurrent import futures
import mensagem_pb2
import mensagem_pb2_grpc


class MensagemService(mensagem_pb2_grpc.MensagemServiceServicer):

    def EnviarMensagem(self, request, context):
        print("Mensagem recebida:", request.texto)
        return mensagem_pb2.MensagemResponse(
            resposta=f"Servidor Python recebeu: {request.texto}"
        )


def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mensagem_pb2_grpc.add_MensagemServiceServicer_to_server(
        MensagemService(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC Python rodando na porta 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    servir()
