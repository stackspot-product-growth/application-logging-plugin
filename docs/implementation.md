This plugin configures the `logback-spring.xml` file on the path `src/main/resources`.
It is possible to enable the generation of different output log formats according to the environment the application is running. E.g:

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

Above, we can see different log output formats, according to the environment whose application is running.
I.e, if the application environment profile is **default** the output log format will be plain text.
For other environment profiles, the output log format will be JSON. 

The plugin also adds the `net.logstash.logback:logstash-logback-encoder` dependency, on the version `7.2` to the project (Gradle/Maven).
For more information about how to customize the logs output, see the [**Logstash Logback Encoder**](https://github.com/logfellow/logstash-logback-encoder).
