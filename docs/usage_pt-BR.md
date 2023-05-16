**Passo 1.** Navegue até a raiz do seu projeto Spring Boot.

**Passo 2.** Execute o comando abaixo:
```bash
stk-alpha apply plugin test/graphene/graphene-logging-plugin
```

**Passo 3.** Adicione as informações solicitadas:

- Selecione somente o nível do log se o projeto tiver sido criado usando o Stackspot. Veja as opções disponíveis para seleção:
    - trace
    - debug
    - info
    - warn
    - error

Veja a documentação oficial para obter mais informações a respeito das opções dos [**níveis de log**] (https://logback.qos.ch/manual/architecture.html).

- O plugin irá solicitar informações adicionais se o projeto não tiver sido criado via StackSpot. Veja abaixo: 
    - **Project name**
    - **Spring Boot version**
    - **Java version**
    - **Project artifact ID**
    - **Project group ID.**  Não informe o nome do projeto no final do **Project group ID**. A StackSpot já solicitou essa informação pelo input que você informou.

**Passo 4.** Formato de saída do log da aplicação:

- O formato padrão do log de saída será JSON se o perfil de ambiente da aplição for dev (desenvolvimento), hom (homologação), or prod (produção).
- O formato padrão do log de saída será texto simples se o perfil de ambiente da aplicação estiver sem atribuição.
- Você pode passar o perfil de ambiente da aplicação por meio do parâmetro `--spring.profiles.active=default,dev,hom or prod`, ou variável de ambiente
  `SPRING_PROFILES_ACTIVE=default,dev,hom or prod`.
- Se sua aplicação foi criada via Stackspot, você pode configurar o `SPRING_PROFILES_ACTIVE` via docker-compose.
- Verifique o arquivo `logback-spring.xml` para obter mais informações sobre a impelementação.

**Passo 5.** Construa o projeto (Build the project) de acordo com seu sistema operacional:

- Linux
```bash
#Maven:
./mvnw clean install
#OR Gradle
./gradlew build
```
- Windows
```bash
#Maven: 
mvnw clean install
#OR Gradle: 
gradlew build
```

**Passo 6.** Execute a aplicação:

- Execute o comando abaixo para subir a aplicação.
```bash
#Parameter profile
java -jar path_your_app.jar --spring.profiles.active=default,dev,hom,prod
#OR
#Environment variable profile
export SPRING_PROFILES_ACTIVE=default,dev,hom or prod
java -jar path_your_app.jar
```

**Passo 7.** Verifique o log de saida no console da aplicação.
