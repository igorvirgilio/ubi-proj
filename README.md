# REST API para Gestão de Ocorrências em Perímetro Urbano

## Escopo
A proposta deste projeto é desenvolver uma plataforma de gestão de ocorrências para um ambiente urbano, baseado em uma API REST. Basicamente o projeto prevê que seja inserida ocorrências com um descrição breve, localização geográfica, autor, data de criação, data de actualização, estado (por validar, validado, resolvido) e possuir as seguintes categorias:

- CONSTRUCTION: Eventos planeados de obras nas estradas;

- SPECIAL_EVENT: eventos especiais (concertos, feiras, etc);

- INCIDENT: acidentes ou outros eventos inesperados;

- WEATHER_CONDITION: eventos meteorológicos que afetam as estradas

- ROAD_CONDITION: estados das estradas que afetem quem circula nestas (piso degradado, buracos, etc).

Novas ocorrências deverão ser criadas sempre com o estado “Por Validar”, que poderão ser alteradas somente por utilizadores com acesso “admin”, e também deverão ser identificadas com o autor que criou tal ocorrência.

A plataforma ainda deverá possibilitar o cadastro de utilizadores, via interface de administração, podendo definir se estes terão nível de permissão de admin *is_staff* ou geral.

A API REST deverá ainda permitir a filtragem das ocorrências por autor, por categoria e por localização (raio de alcance).


## Repositório de imagens criadas

Segue os repositórios de imagem Docker Hub que possuem corelação com este repositório Git

- https://hub.docker.com/r/igorvirgilio/ubi_restapi

- https://hub.docker.com/r/igorvirgilio/ubi_db

## Documentação utilizada

As documentações utilizadas foram:

- https://www.django-rest-framework.org/

- https://www.djangoproject.com/start/

- https://docs.docker.com/



## Pre-requisitos 

Os códigos foram implementados em ambiente virtual hospedado em Linux Ubuntu 18.04.

Segue a lista dos itens que foram instalados na imagem **ubi_restapi**:


``` bash
apt-get install libpq-dev -y

apt-get install python-dev -y 

apt-get install gdal-bin -y
``` 

``` bash
asgiref==3.2.7
astroid==2.3.3
Django==3.0.5
django-filter==2.2.0
djangorestframework==3.11.0
isort==4.3.21
lazy-object-proxy==1.4.3
Markdown==3.2.1
mccabe==0.6.1
psycopg2==2.8.5
pylint==2.4.4
pypi-install==0.0.5
pytz==2019.3
six==1.14.0
sqlparse==0.3.1
typed-ast==1.4.1
wrapt==1.11.2
```

## Construção Docker

### Dockerfile

Para a criação da imagem que contém a REST API Django foi utilizada uma imagem base **Python-3.6-Buster**.

Foi adicionado esse repositório Git em seu diretório principal

Abaixo segue o Dockerfile na íntegra:
 ``` docker
FROM python:3.6-buster

RUN git clone https://github.com/igorvirgilio/Ubiwhere-igor.git
WORKDIR /Ubiwhere-igor
COPY requirements.txt .

RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install libpq-dev -y &&\
    apt-get install python-dev -y &&\ 
    pip install -r requirements.txt &&\
    apt-get install gdal-bin -y

EXPOSE 8000
 ``` 
### docker-compose.yml

``` yml
version: '3'

services:
  ubi_rest:
    build: .
    
    volumes:
      - ./Docker:/opt
    ports:
      - 8000:8000
 ```  

## Deploy da REST API

Após configurar e fazer o depoly da Base de Dados e ter baixado a imagem *igorvirgilio/ubi_restapi* pode-se prosseguir para os passos de incialização do conteiner e em seguida os comandos para serem executados dentro da console do conteiner *ubi_restapi*

### Inicialização do conteiner *ubi_restapi*

Para a incicialização do conteiner é sugerido o seguinte comando:
*[link da imagem](https://hub.docker.com/r/igorvirgilio/ubi_restapi)*
``` bash
docker run -it -p 8000:8000 --name ubi_restapi igorvirgilio/ubi_restapi:v1 /bin/bash
``` 

### Comandos de preparação do ambiente

Caso ainda não tenha sido criado um superuser ou ainda não possua o registro na Base de dados, basta executar o comando a seguir para criar um utilizador admin, e preencher o email(caso queira) e por fim a senha:
``` bash
python manage.py createsuperuser
``` 

Após a criação do superuser, basta executar os comandos de migração, que validará os ficheiros e associar com a base de dados.
``` bash
python manage.py makemigrations

python manage.py migrate
```

E por fim iniciar o servidor, apontando o IP e porta desejados (recomenda-se utilizar 0.0.0.0:8000)
``` bash
python manage.py runserver 0.0.0.0:8000
```

Então basta aceder este endereço em um navegador com o endpoint */occur/*, ficando da seguinte forma *http://0.0.0.0:8000/occur/*

# /ubi_proj

## /ubi_proj /settings.py
Esse arquivo possui as configurações principais da estrutura do projeto. Nele adicionamos a referência dos APP’s que utilizamos no projeto, as informações para que a Framework aceda e vincule a base de dados. Basicamente são esses as alterações que foram feitas no arquivo original do projeto. A seguir estão explicitadas essas alterações:
 
Após a configuração da base de dados pode ser executado os comandos a seguir para fazer as migrações necessárias e seguida iniciar o servidor:

## /ubi_proj /urls.py
O ficheiro urls.py do projeto principal, define o caminho para aceder ao painel Django Admin, e também para apontar para outras aplicações, por exemplo, como foi feito neste caso. 

# /occurrence

## /occurrence/models.py
Nesse ficheiro são definidos todos os campos em que os objetos (ocorrências) de nossa API deverão conter, que neste projeto compreende pelos seguintes campos:
- Categoria;
- Descrição;
- Localização geográfica;
- Autor;
- Data de criação;
- Data de actualização;
- Estado.
Para cada parâmetro é definido o tipo de dados de cada campo, se será do tipo campo de texto, menu de escolha, data entre outros, e além disso pose-se definir se há uma resposta padrão para ser utilizada, se deve ser de preenchimento obrigatório ou não, e ainda se caso não seja preenchido considera o campo como null.

## /occurrence/urls.py
Neste ficheiro são definidos as URLs com os endpoints que conterão cada método HTTP

## /occurrence/serializers.py
Outro ficheiro que possui grande importância é o serializers.py, que faz conversão dos queryset em Python e possam ser renderizados para JSON.
Foram criadas as seguintes classes:

### OccurrenceSerializer
Esta classe disponibiliza todos os campos que foram definidos na classe do ficheiro models.py através de uma subclasse Meta, assim como as demais a seguir, porém nesta são serializados todos os campos para que sejam utilizados por outras classes deste projeto.

### OccurrenceSerializerPut
Nessa classe foi limitado os campos aos quais queremos que sejam considerados para o método PUT, ou seja, que serão apresentados e destes quais serão apenas para leitura, os demais poderão ser editados.
As datas como estão definidas com o parâmetro auto_now, já são apenas para leitura e não permitem edição.

### OccurrenceSerializerPost
A classe OccurrenceSerializerPost, segue o mesmo conceito que a anterior, porém nesta limitamos quais campos serão disponíveis para criação de um novo objeto via método POST
Abaixo pode-se ver, que a diferença com relação a classe OccurrenceSerializerPut é que adicionamos o campo ‘status’ aos campos que são read-only.

## /occurrence/view.py
Neste ficheiro são declaradas as classes que irão formatar a estrutura backend da API REST para uma interface web. A grande vantagem de utilizar tais classes são que elas já são pré-contruídas com um padrão específico para APIs de forma que possa ser utilizado para um rápido deploy de uma API.

No projeto atual foi utilizado o GenericAPIView que estende da classe REST framework APIView e combina com as classes Mixins.

Há atributos que controlam o comportamento básico de visualização:

- queryset – utilizado para retornar os objetos desse view

- serializer_class – aponta para a classe serializadora que é utilizada para validação de deserialização de entrada e serialização de saída.

- lookup_field – é o campo do model que é utilizado para fazer o lookup de uma instância (ocorrência)

- filter_backends – é uma lista de classes de filtragem backend utilizada para filtrar as querysets.

Além desses atributos foram utilizados os métodos Mixins, a seguir estão tais métodos que forma utilizados:

- .list( ) – implementa a listagem das queryset

- .create( ) – implementa criação de salvamento de uma nova instância (ocorrência)

- .retrieve( ) – implementa o return de uma instância existente em um response

- .update( ) – implementa a atualização e salvamento de uma instância existente

- .destroy( ) – implementa a deleção de uma instância existente.

No projeto foram criadas 4 classes que utilizam tais atributos e métodos para serem construídos. A seguir segue o exemplo dessas classes:

### OccurenceList
 Nessa classe foi utilizada, além dos atributos “mandatórios” queryset e serializer_class, utilizou-se o filter_backends, que permite que declaremos os campos que desejamos poder filtrar, que conforme especificado no escopo são o autor, categoria da ocorrência e a localização. Nota-se ainda que no atributo serializer_class é apontado à classe OccurrenceSerializer, faz a serialização/deserialização para todos os campos de model:

### GenericDetailAPIView

Já na classe GenericDetailAPIView é estendido das classes Mixins. Nessa classe optou-se por listar apenas uma instância por vez, e assim associar os métodos .update( ), .destroy( ) e também o .list( ) para tomar ações direcionadas à uma instância específica com id={id}, cada métod está associado as funções put( ), delete( ) e get (), respetivamente.

Mais particularmente sobre as funções put( ) e delete( ), foi adicionada a condição de validação para verificar se o utilizador que está associado a query tem privilégios de administrador (is_staff) ou não. Caso não possua tal privilégio a requisição não é aceita além de retornar um HttpResponseForbidden, caso seja, é executado o método associado.

Para verificação das validações de autenticação e autorização, são utilizados os atributos authentication_classes e permission_classes. Com tais informações extraídas via classes declaradas por esses atributos é possível avaliar via o argumento is_staff, se de fato o utilizador está autenticado e se de fato é privilegiado. 

*Obs.: no atributo authentication_classes é declarado 3 formas de verificação de autenticação, que é verificado na ordem que se apresenta. Desta forma permite que possa utiliza-se de autenticação inclusive via token, comum em dispositivos IoT por exemplo, para uma futura implementação*

### GenericPOSTAPIView

Na classe GenericPOSTAPIView segue a mesma estrutura da classe GenericDetailAPIView. Possui atributos com valores iguais com exceção do serializer_classe, que se refere à classe OccurenceSerializePost ao invés da OccurenceSerializePost. O que muda é a forma que é tratada a serialização/deserialização dos queries e além disso que nesta classe GenericPOSTAPIView, há somente os métodos .create( ) e .list( )/.retrieve( ), e também a função perform_create( ).

### OccurenceOrder

Por fim, a classe OccurenceOrder basicamente permite a listagem dos objetos de forma ordenada de forma ascendente ou decrescente baseado no autor, categoria da ocorrência ou pela localização.

