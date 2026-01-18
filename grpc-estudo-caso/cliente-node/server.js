const express = require("express");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const path = require("path");

const app = express();
app.use(express.json());

const packageDefinition = protoLoader.loadSync(
  "../proto/mensagem.proto"
);
const mensagemProto = grpc.loadPackageDefinition(packageDefinition).mensagem;

const grpcClient = new mensagemProto.MensagemService(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

app.post("/enviar", (req, res) => {
  grpcClient.EnviarMensagem(
    { texto: req.body.texto },
    (error, response) => {
      if (error) {
        res.status(500).json({ erro: error.message });
      } else {
        res.json({ resposta: response.resposta });
      }
    }
  );
});

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(3000, () => {
  console.log("Interface disponível em http://localhost:3000");
});
