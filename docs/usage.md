**Step 1.** Go to the root path of your Spring Boot project.

**Step 2.** Execute the command below:

```bash
stk-alpha apply plugin test/graphene/graphene-logging-plugin
```

**Step 3.** Add the requested information

- Select only the log level if the project had been created using Stackspot. See the available options:
  - trace
  - debug
  - info
  - warn
  - error

See the official doc to get more information about the [**log level options**](https://logback.qos.ch/manual/architecture.html).

- The plugin will request additional information if the project hadn't been created via StackSpot. See below:
  - **Project name**
  - **Spring Boot version**
  - **Java version**
  - **Project artifact ID**
  - **Project group ID.**  Don't add the project's name at the end of the group ID. StackSpot already requested this information via the input you informed.

**Step 4.** Application output log format:

- The output log format will be JSON if the application environment profile is dev (development), hom (homologation), or prod (production).
- The default output log format will be plain text if the application environment profile is without attribution.
- You can pass the application environment profile through the parameter `--spring.profiles.active=default,dev,hom or prod`, or the environment variable
  `SPRING_PROFILES_ACTIVE=default,dev,hom or prod`
- If your application had been created via Stackspot you can set up the `SPRING_PROFILES_ACTIVE` via docker-compose.
- Check the file `logback-spring.xml` to get more information about the implementation.

**Step 5.** Build the project according to your OS:

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

**Step 6.** Run the application:
 
- Run the command below to put the application up:
```bash
#Parameter profile
java -jar path_your_app.jar --spring.profiles.active=default,dev,hom,prod
#OR
#Environment variable profile
export SPRING_PROFILES_ACTIVE=default,dev,hom or prod
java -jar path_your_app.jar
```

**Step 7.** Check the output log on the application console.
