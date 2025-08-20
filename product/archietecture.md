# Application Architecture and Database Schema (Enhanced Security)

This document outlines the proposed architecture and database schema for the GOS (Reddit #2) application, based on the product specifications. This version includes enhanced security considerations.

## 1. System Architecture

A standard three-tier architecture is recommended:

*   **Presentation Layer (Client):** A web-based front-end built with a modern JavaScript framework (e.g., React, Vue, or Angular) to provide a responsive and interactive user experience.
*   **Application Layer (Server):** A back-end API built with a robust framework (e.g., Node.js with Express, Python with Django/FastAPI, or Go) to handle business logic, user authentication, and data processing.
*   **Data Layer (Database):** A relational database (e.g., PostgreSQL or MySQL) to store and manage the application's data.

## 2. Security Considerations

### 2.1. Authentication and Authorization
*   **Password Hashing:** Use a strong, slow hashing algorithm like **Argon2** or **bcrypt** to store passwords. The `password_hash` column should be `TEXT` to accommodate the full hash string, which includes the salt.
*   **Email Verification:** New user accounts should require email verification to be activated.
*   **Password Reset:** Implement a secure password reset mechanism using single-use tokens with a short expiration time.
*   **Role-Based Access Control (RBAC):** Introduce `roles` and `user_roles` tables to manage user permissions (e.g., `admin`, `moderator`, `user`).

### 2.2. API Security
*   **Input Validation:** All user input must be validated and sanitized on the server-side to prevent **XSS**, **SQL injection**, and other injection attacks.
*   **Rate Limiting:** Implement rate limiting on the API to prevent brute-force attacks and denial-of-service.
*   **HTTPS:** Use HTTPS for all communication between the client and server to encrypt data in transit.
*   **CORS:** Configure Cross-Origin Resource Sharing (CORS) to only allow requests from trusted domains.
*   **Security Headers:** Use security headers like `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, and `Strict-Transport-Security`.

## 3. Database Schema (Enhanced Security)

The following schema is designed to be secure, scalable, and normalized to minimize data redundancy.

### Users

Stores user account information.

| Column                   | Data Type     | Constraints               | Description                                      |
| ------------------------ | ------------- | ------------------------- | ------------------------------------------------ |
| `id`                     | `SERIAL`      | `PRIMARY KEY`             | Unique identifier for the user.                  |
| `username`               | `VARCHAR(255)`| `UNIQUE`, `NOT NULL`      | User's unique username.                          |
| `email`                  | `VARCHAR(255)`| `UNIQUE`, `NOT NULL`      | User's unique email address.                     |
| `password_hash`          | `TEXT`        | `NOT NULL`                | Hashed password for security.                    |
| `avatar_url`             | `VARCHAR(255)`|                           | URL to the user's avatar image.                  |
| `karma`                  | `INTEGER`     | `DEFAULT 0`               | User's reputation score.                         |
| `is_verified`            | `BOOLEAN`     | `DEFAULT false`           | Whether the user has verified their email.       |
| `verification_token`     | `VARCHAR(255)`|                           | Token for email verification.                    |
| `reset_password_token`   | `VARCHAR(255)`|                           | Token for password reset.                        |
| `reset_password_expires` | `TIMESTAMP`   |                           | Expiration time for the password reset token.    |
| `created_at`             | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of when the user was created.          |
| `updated_at`             | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`| Timestamp of when the user was last updated.     |

### Roles and UserRoles

For Role-Based Access Control (RBAC).

**roles**

| Column | Data Type     | Constraints  | Description                                      |
| ------ | ------------- | ------------ | ------------------------------------------------ |
| `id`   | `SERIAL`      | `PRIMARY KEY`| Unique identifier for the role.                  |
| `name` | `VARCHAR(255)`| `UNIQUE`, `NOT NULL` | The name of the role (e.g., 'admin', 'moderator', 'user'). |

**user_roles**

| Column    | Data Type | Constraints                  | Description                                      |
| --------- | --------- | ---------------------------- | ------------------------------------------------ |
| `user_id` | `INTEGER` | `FOREIGN KEY (users.id)`     | The user associated with the role.               |
| `role_id` | `INTEGER` | `FOREIGN KEY (roles.id)`     | The role assigned to the user.                   |

### Subreddits

Stores information about communities or pages.

| Column        | Data Type     | Constraints                          | Description                                         |
| ------------- | ------------- | ------------------------------------ | --------------------------------------------------- |
| `id`          | `SERIAL`      | `PRIMARY KEY`                        | Unique identifier for the subreddit.                |
| `name`        | `VARCHAR(255)`| `UNIQUE`, `NOT NULL`                 | Unique name of the subreddit.                       |
| `description` | `TEXT`        |                                      | A brief description of the subreddit.               |
| `creator_id`  | `INTEGER`     | `FOREIGN KEY (users.id) ON DELETE SET NULL` | The user who created the subreddit.                 |
| `created_at`  | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`          | Timestamp of when the subreddit was created.        |
| `updated_at`  | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`          | Timestamp of when the subreddit was last updated.   |

### Posts

Stores information about posts made by users.

| Column         | Data Type     | Constraints                                | Description                                      |
| -------------- | ------------- | ------------------------------------------ | ------------------------------------------------ |
| `id`           | `SERIAL`      | `PRIMARY KEY`                              | Unique identifier for the post.                  |
| `title`        | `VARCHAR(255)`| `NOT NULL`                                 | The title of the post.                           |
| `content`      | `TEXT`        |                                            | The main content of the post (e.g., text, markdown).|
| `media_url`    | `VARCHAR(255)`|                                            | URL to any associated media (image, video).      |
| `link_url`     | `VARCHAR(255)`|                                            | URL for link-based posts.                        |
| `poll_id`      | `INTEGER`     | `FOREIGN KEY (polls.id) ON DELETE CASCADE` | Foreign key to the poll associated with the post.|
| `user_id`      | `INTEGER`     | `FOREIGN KEY (users.id) ON DELETE CASCADE` | The user who created the post.                   |
| `subreddit_id` | `INTEGER`     | `FOREIGN KEY (subreddits.id) ON DELETE CASCADE` | The subreddit the post belongs to.               |
| `created_at`   | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`                | Timestamp of when the post was created.          |
| `updated_at`   | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`                | Timestamp of when the post was last updated.     |

### Comments

Stores comments on posts.

| Column            | Data Type | Constraints                                   | Description                                         |
| ----------------- | --------- | --------------------------------------------- | --------------------------------------------------- |
| `id`              | `SERIAL`  | `PRIMARY KEY`                                 | Unique identifier for the comment.                  |
| `content`         | `TEXT`    | `NOT NULL`                                    | The content of the comment.                         |
| `user_id`         | `INTEGER` | `FOREIGN KEY (users.id) ON DELETE CASCADE`    | The user who wrote the comment.                     |
| `post_id`         | `INTEGER` | `FOREIGN KEY (posts.id) ON DELETE CASCADE`    | The post the comment belongs to.                    |
| `parent_comment_id`| `INTEGER` | `FOREIGN KEY (comments.id) ON DELETE CASCADE` | For threaded replies, the parent comment.           |
| `created_at`      | `TIMESTAMP`| `DEFAULT CURRENT_TIMESTAMP`                   | Timestamp of when the comment was created.          |
| `updated_at`      | `TIMESTAMP`| `DEFAULT CURRENT_TIMESTAMP`                   | Timestamp of when the comment was last updated.     |

### Votes

Stores upvotes and downvotes for posts and comments.

| Column       | Data Type     | Constraints                                   | Description                                         |
| ------------ | ------------- | --------------------------------------------- | --------------------------------------------------- |
| `id`         | `SERIAL`      | `PRIMARY KEY`                                 | Unique identifier for the vote.                     |
| `user_id`    | `INTEGER`     | `FOREIGN KEY (users.id) ON DELETE CASCADE`    | The user who cast the vote.                         |
| `post_id`    | `INTEGER`     | `FOREIGN KEY (posts.id) ON DELETE CASCADE`    | The post being voted on (nullable).                 |
| `comment_id` | `INTEGER`     | `FOREIGN KEY (comments.id) ON DELETE CASCADE` | The comment being voted on (nullable).              |
| `vote_type`  | `VARCHAR(10)` | `CHECK (vote_type IN ('upvote', 'downvote'))` | The type of vote (upvote or downvote).             |
| `created_at` | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`                   | Timestamp of when the vote was cast.                |