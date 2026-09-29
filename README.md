# Product Inventory API

A RESTful Product Inventory API built with Java 17 and Spring Boot 3.3.5. The application provides CRUD operations for products and persists product data in an H2 in-memory database.

## Features

- Create, retrieve, update, and delete products
- H2 database persistence through Spring Data JPA
- Bean validation and structured error responses
- Spring Boot Actuator health endpoint
- Integration tests using Spring Boot Test, JUnit 5, MockMvc, and H2

## Technology Stack

- Java 17, Spring Boot 3.3.5, Spring Web, Spring Data JPA
- Spring Boot Validation, Actuator, H2 Database, Maven
- JUnit 5, MockMvc, AssertJ

## Project Structure

```text
product-inventory-api/
├── pom.xml
├── README.md
└── src/
    ├── main/java/com/example/productinventory/
    │   ├── ProductInventoryApplication.java
    │   ├── controller/ProductController.java
    │   ├── dto/ProductRequest.java
    │   ├── exception/{ApiError,GlobalExceptionHandler,ResourceNotFoundException}.java
    │   ├── model/Product.java
    │   ├── repository/ProductRepository.java
    │   └── service/ProductService.java
    ├── main/resources/application.properties
    └── test/java/com/example/productinventory/ProductInventoryApplicationTests.java
```

## REST API

Base path: `/api/products`

- `POST /api/products` creates a product and returns `201 Created` with a `Location` header.
- `GET /api/products` retrieves all products.
- `GET /api/products/{id}` retrieves a product or returns `404 Not Found`.
- `PUT /api/products/{id}` fully replaces mutable product fields.
- `DELETE /api/products/{id}` returns `204 No Content` on success.
- `GET /actuator/health` returns the application health status.

Product fields are `id`, `name`, `description`, `price`, `quantity`, and `category`. Names, descriptions, and categories are required; price and quantity must be non-negative.

## Configuration

The application uses an in-memory H2 database and runs on port 8080:

```properties
spring.application.name=product-inventory-api
server.port=8080
spring.datasource.url=jdbc:h2:mem:productdb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=update
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
management.endpoints.web.exposure.include=health
```

## Build, Run, and Test

Prerequisites: Java 17+ and Maven 3.8+.

```bash
mvn clean package
mvn spring-boot:run
mvn test
```

The API is available at `http://localhost:8080`; H2 data is lost when the application stops.

## Assumptions

- Product IDs are generated `Long` values and price uses `BigDecimal`.
- `PUT` performs a full replacement and invalid requests return `400 Bad Request`.
- No authentication, pagination, filtering, sorting, images, or inventory history was specified.

# Test App

A sample microservice built for testing EliteA automated documentation synchronization.
