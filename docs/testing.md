# Testing

## 1. Requirement Analysis ~ User Acceptance Testing
- What the system should do.
- Use Case Diagram

## 2. Functional Specification ~ System Testing
- System's behavior and external interfaces.
- Finalize architecture, database, environment design
- Entity-Relationship Diagram
- High-level blueprint of the entire system.
Application type: web app, mobile app, desktop app, microservices, monolithic...
Overall structural style (architectural pattern): MVC, client-server. n-tier...
The number of tiers/layers in the application: presentation layer, business logic layer, data access layer.
Materials (technologies and frameworks): python with Django,FastAPI,Flask; Java with Spring Boot; Node.js with React; specific database like PostgreSQL/MongoDB.
Deployment environment: on-premise servers, cloud platform like AWS/Azure/GCP, containerization with Docker/k8s.
Communication protocols: REST APIs, message queues...

## 3. High Level Design ~ Integration Testing
- Break down the application into modules and programs and define their interactions.
- The modules are conceptual and logical units of functionality (**abstract grouping of related functionalities**) :
Break down complexity: Divide a large system into manageable, understandable parts.
Degine clear responsibilities.
Establish high-level interfaces: How these conceptual modules will communicate with each other.
Facilitate parallel development: Different teams or developers can work on different modules concurrently.

- These **conceptual modules** are represented **differently** in the actual code structure depending on specific tech stack and framework, architectural patterns... Examples:
FastAPI (Python): dedicated folders 'user' containing routers with endpoints (the controller) + services containing business logic (service layer) + repositories containing database interaction logic (data access layer) + pydantic models for request/response models (DTOs) + SQLAlchemy ORM classes => together they form a "User Management Module"

- Sequence Diagrams

## 4. Detailed Design ~ Unit Testing
- Pseudocode for functions for each module is documented.
- Refine/Create new Sequence Diagrams.

## 5. Implementation


# Unit Testing (component testing)
- Thực hiện trên từng module riêng lẻ để ktra xem có được dev đúng không.
- Example Unit Test for Login Module: (username/id + password)
Enter Valid Login ID & Password
Enter inValid Login ID & Password
Empty Login ID & Click Login

## Tiki engineering (https://engineering.tiki.vn/unit-test-best-practices/)

- Unit test là test ở mức đơn vị (unit), đơn vị có thể là rất nhỏ, hoặc có thể lớn hơn. Đơn vị nhỏ nhất là function. Các class, interface, usecase cũng có thể coi là 1 đơn vị.

- Unit test chỉ test các logic được define bởi đơn vị đó, mà không bao gồm các dependency khác (như database, external service). Unit test có thể chạy độc lập mà ko cần setup test environment.

- Các dependency của Unit test thường được dùng Test-Double (xem thêm bên dưới) để xử lý thay vì sử dụng đối tượng thật.

- Do bản chất Unit Test không quan tâm đến các logic khác, cho nên nó cũng ko thể đảm bảo bug-free cho application.

- Unit test giúp đảm bảo độ ổn định cho từng unit và cung cấp 1 live document về cách thức mà unit này hoạt động (các developer thay vì phải đọc code của các component để xem chúng làm gì, các test case được viết 1 cách rõ ràng của Unit Test có thể làm điều đó tốt hơn, hơn nữa đọc code của developer khác thường là trải nghiệm ko mấy vui vẻ).

## Requirements:
- Unit-test phải ngắn gọn, dễ hiểu, dễ đọc, có thể sẽ phải có đầy đủ mô tả cho từng nhóm dữ liệu input/output.
- Mỗi unit-test cần phát triển riêng biệt, không nên thiết kế output của unit-test này là input của unit-test tiếp theo.
- Khi đặt tên unit-test cần đặt tên gợi nhớ hoặc theo quy chuẩn của từng nhóm phát triển để tường minh việc unit-test này đang test cho unit nào.
- Mỗi unit-test chỉ nên thực hiện test cho một unit, nếu các unit có về input/output hoặc code thì chấp nhận việc duplicate các unit-test.


## Remember
- Design good tests, not just as many as possible.
- Base on the expected output of the unit being tested, including errors.