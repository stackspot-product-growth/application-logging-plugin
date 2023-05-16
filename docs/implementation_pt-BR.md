Esse Plugin configura o arquivo `logback-spring.xml` no diretório `src/main/resources`.
Nele é possivel habilitar a geração de diferentes formatos de logs de saída conforme o ambiente em que a aplicação está executando. Ex:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <springProfile name="dev,hom,prod">
    <appender name="jsonConsoleAppender" class="ch.qos.logback.core.ConsoleAppender">
      <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
    </appender>
    <root level="{{log_level}}">
      <appender-ref ref="jsonConsoleAppender"/>
    </root>
  </springProfile>
  <springProfile name="default">
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>
    <include resource="org/springframework/boot/logging/logback/console-appender.xml" />
    <root level="{{log_level}}">
      <appender-ref ref="CONSOLE" />
    </root>
    <logger name="org.springframework.web" level="info"/>
  </springProfile>
</configuration>
```

Acima podemos ver diferentes formatos de logs de saída, conforme o ambiente que a aplicação está sendo executada.
Ou seja, se o perfil de ambiente da aplicação for **default**, o formato padrão do log de saída será texto simples.
Para outros perfils de ambiente, o formato do log padrão de saída será JSON.

O Plugin também adiciona a dependência `net.logstash.logback:logstash-logback-encoder` na versão `7.2` ao projeto para Gradle ou Maven.
Para maiores informações sobre como customizar o formato do log de saída, veja a documentação oficial [**Logstash Logback Encoder**](https://github.com/logfellow/logstash-logback-encoder). 

