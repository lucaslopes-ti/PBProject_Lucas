# Desafio: Prática de Python com Containers Docker

## **Objetivo**
O objetivo deste desafio é praticar o uso de Python combinado com Docker, criando imagens, executando containers e desenvolvendo scripts que interajam com o usuário.

---

## **Estrutura do Projeto**
O projeto foi dividido em duas etapas, cada uma armazenada em pastas separadas: `etapa1` e `etapa2`.

### **Arquivos Criados**
- **Etapa 1:**
  - `carguru.py`
  - `Dockerfile` (localizado na pasta `etapa1`)
- **Etapa 2:**
  - `mascara.py`
  - `Dockerfile` (localizado na pasta `etapa2`)

---

## **Etapas do Desafio**

### **Etapa 1: Execução do Código `carguru.py` em um Container**
#### **Passo 1.1: Conteúdo do Script `carguru.py`**
```python
print("Voce deve dirigir um Volkswagen Parati")
```

#### **Passo 1.2: Dockerfile**

````
# Usar uma imagem base do Python
FROM python:3.9-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar o script Python para o container
COPY carguru.py /app/carguru.py

# Configurar o comando de execução do script
CMD ["python", "carguru.py"]
````

#### **Passo 1.3: Comandos para Construção e Execução**

    Navegar para a pasta etapa1:
````
cd etapa1
````
    Construir a imagem Docker:
````
docker build -t carguru-image .
````
    Executar o container:
````
    docker run --name carguru-container carguru-image
````
#### **1.4: Resultado Esperado**

Ao executar o container, o seguinte texto será exibido no terminal:
````
Voce deve dirigir um Volkswagen Parati
````
### **Passo 2: Criar um Container que Recebe Inputs**
#### **2.1: Conteúdo do Script mascara.py**
````
import hashlib

# Receber input do usuário
entrada = input("Digite uma string para mascarar: ")

# Gerar o hash SHA-1
hash_sha1 = hashlib.sha1(entrada.encode())

# Imprimir o hash na tela
print(f"O hash SHA-1 da string é: {hash_sha1.hexdigest()}")
````
#### **2.2: Dockerfile**
````
# Usar uma imagem base do Python
FROM python:3.9-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar o script Python para o container
COPY mascara.py /app/mascara.py

# Configurar o comando de execução do script
CMD ["python", "mascara.py"]
````
#### **2.3: Comandos para Construção e Execução**

Navegar para a pasta etapa2:
````
cd etapa2
````
Construir a imagem Docker:
````
docker build -t mascarar-dados .
````
Executar o container interativamente:
````
docker run -it --name mascarar-container mascarar-dados
````
#### **2.4: Resultado Esperado**

Ao executar o container, ele pedirá uma string de entrada. Por exemplo:
````
Digite uma string para mascarar: Ola, Mundo!
O hash SHA-1 da string é: 7242db5d116f7e8dddb8d89e70bca71d206e26d0
````

### **Passo 3: Reutilização de Containers**

Sim, é possível reutilizar containers parados. Utilize o comando:

Reiniciar o container parado:
```
docker start -ai mascarar-container
```
Caso seja necessário recriar o container, utilize:
```
docker run -it --name mascarar-container mascarar-dados
```

### **Imagens e Evidências**

#### **Exemplo da Execução do Container na Etapa 1:**

#### **Exemplo da Execução do Container na Etapa 2:**


### **Comentários Finais**

Este desafio demonstra como Python pode ser integrado com Docker para criar aplicações portáveis e reutilizáveis. O código, os arquivos Dockerfile e os comandos de execução foram desenvolvidos com base nas melhores práticas.




