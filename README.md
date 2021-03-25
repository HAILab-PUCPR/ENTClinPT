# ENTClinPT - Uma API para Extração de Entidades Clínicas em Português

** *trabalho em andamento* **

# Table of Contents
1. [Como executar localmente](#como-executar)
2. [Executando via docker](#executando-via-docker)
3. [Como citar](#como-citar)

## Como executar
1. Clone o repositório
2. Instale as biblitecas necessárias (se preferir, use [Anaconda](anaconda.com))
```
pip install numpy
pip install transformers == 4.3.0
pip install torch==1.8.0+cpu torchvision==0.9.0+cpu torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html
pip install flask == 4.3.0
```
ou através do comnando:
```
pip install -r requirements.txt
```
3. Execute o app.py
```
python app.py
```
4. No navegador, acesse http://localhost:5000/

<img src="https://github.com/lisaterumi/EntClinBr/blob/main/prints/entclinbr1.jpg">

<img src="https://github.com/lisaterumi/EntClinBr/blob/main/prints/entclinbr2.jpg">

## Executando via docker

ra que serve o Docker?

O Docker serve para facilitar o dia a dia dos desenvolvedores e profissionais de infra, criando, de forma simplificada, um ambiente onde possam trabalhar alinhados com sua equipe e infraestrutura de servidores e fique simples criar e re-utilizar containers com “serviços” pré-configurados, simples de alterar e que possam ser versionados e mantidos através de simples arquivos de configuração.

## Como citar

* em breve *
