# Task Manager API 
`ALX Backend capstone` `REST API`

The Task Manager API is a backend application built with Django, designed to help users efficiently manage their tasks. This API provides functionality for users to create, update, and delete tasks, as well as mark them as complete or incomplete. It is developed with scalability and simplicity in mind, making it a great foundation for learning or expanding to more complex applications.

## Core fetaures

- **User Management** 
    - Full CRUD operations for users.
- **Authentication & Authorization**
    - Secure JWT-based authentication.
    - Role-based access control (RBAC) for admin and users.
- **Task Management**
    - CRUD operations for tasks.
    - Mark tasks as complete or incomplete.
    - Filter and sort tasks by status, priority, deadline, and category.
    - Task validation to ensure quality inputs.
- **Error Handling**
    - Standardized error responses for better API consumption.

## Project Structure

- `api/`:
- `project/`: 
- `.gitignore`: Files and directories ignored by Git.
- `README.md`: Project documentation.

## API

### Requests

- All requests must include a valid JWT token for protected endpoints.
- Accepts JSON payloads.

### Responses

- Success responses follow:
```json
{
    "message": "Success",
    "data": {}
}
```

- Error responses follow:
```json
{
    "error": "Error message"
}
```

## Endpoints

### Authentication

<details>
    <summary>
    Sign up  <code>POST /auth/register</code>
    </summary>
    <br>

Endpoint : `POST /auth/register`
Successful response : `201`
Failure responses : `400` 
</details>

<details>
    <summary>
    Sign in <code>POST /auth/login</code>
    </summary>
    <br>

Endpoint : `POST /auth/login`
Successful response : `200`
Failure responses : `400` 
</details>

### User management

<details>
    <summary>
    Get current user <code>GET /user</code>
    </summary>
    <br>

Endpoint : `GET /user`
Successful response : `200`
Failure responses : `400`
</details>

<details>
    <summary>
    Update user details <code>PUT /user</code>
    </summary>
    <br>

Endpoint : `PUT /user`
Successful response : `204`
Failure responses : `400`
</details>

 
<details>
    <summary>
    Delete a user <code>DELETE /user</code>
    </summary>
    <br>

Endpoint : `DELETE /user`
Successful response : `204`
Failure responses : `400` 
</details>

### Tasks management

<details>
    <summary>
    Create a task <code>POST /tasks</code>
    </summary>
    <br>

Create a new task by providing necessary details such as title, description, priority, category, and deadline.

Endpoint : `POST /tasks`
Successful response : `201`
Failure responses : `400` 
</details>

<details>
    <summary>
    Get all tasks <code>GET /tasks</code>
    </summary>
    <br>

Retrieve a list of all tasks. Optional filters and sorting parameters can be applied to narrow down the results.

Endpoint : `GET /tasks`
Successful response : `200`
Failure responses : `400`

__Filtering__

Check task model for accepted values 

- By status : `GET /tasks?status=<status>`
- By priority : `GET /tasks?priority=<priority>`
- By category : `GET /tasks?category=<category>`
- By deadline : `GET /tasks?deadline=<deadline>`

__Sorting__

Sort tasks in ascending or descending order.

- By title ascending : `GET /tasks?sort=title`
- By title desccending : `GET /tasks?sort=-title`
- By deadline ascending : `GET /tasks?sort=deadline`
- By deadline desccending : `GET /tasks?sort=-deadline`
- By priority ascending : `GET /tasks?sort=priority`
- By priority desccending : `GET /tasks?sort=-priority`   

</details>

### Tasks manaegement

<details>
    <summary>
    Get a task <code>GET /task/:id</code>
    </summary>
    <br>

Fetch the details of a specific task by providing the task ID.

Endpoint : `GET /task/<id>`
Successful response : `200`
Failure responses : `400`
</details>

<details>
    <summary>
    Update Task Details <code>PUT /task/:id</code>
    </summary>
    <br>

Update the details of an existing task by specifying the task ID. Only tasks with a pending status can be updated.

Endpoint : `PUT /task/<id>`
Successful response : `204`
Failure responses : `400` 

__Mark task as completed__

Change the status of a task to completed by specifying the task ID.

Endpoint : `PUT /task/<id>/mark-as-completed`

__Mark task as pending__

Revert a completed task back to pending status by specifying the task ID.

Endpoint : `PUT /task/<id>/mark-as-pending`
</details>

<details>
    <summary>
    Delete task <code>DELETE /task/:id</code>
    </summary>
    <br>

Permanently remove a task from the system by specifying the task ID.

Endpoint : `DELETE /task/<id>`
Successful response : `204`
Failure responses : `400`
</details>

