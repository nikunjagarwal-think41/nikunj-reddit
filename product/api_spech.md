# API Specifications for GOS (Reddit #2)

This document outlines the API endpoints for the GOS application.

## Authentication

### POST /api/auth/register

*   **Description:** Registers a new user.
*   **Request Body:**
    *   `username` (string, required)
    *   `email` (string, required)
    *   `password` (string, required)
*   **Responses:**
    *   `201 Created`: User registered successfully.
    *   `400 Bad Request`: Invalid input (e.g., missing fields, invalid email).
    *   `409 Conflict`: Username or email already exists.

### POST /api/auth/login

*   **Description:** Logs in a user and returns a JWT.
*   **Request Body:**
    *   `email` (string, required)
    *   `password` (string, required)
*   **Responses:**
    *   `200 OK`: Login successful. Returns `{ "token": "your_jwt_token" }`.
    *   `401 Unauthorized`: Invalid credentials.

### POST /api/auth/verify-email

*   **Description:** Verifies a user's email address.
*   **Request Body:**
    *   `token` (string, required)
*   **Responses:**
    *   `200 OK`: Email verified successfully.
    *   `400 Bad Request`: Invalid or expired token.

### POST /api/auth/forgot-password

*   **Description:** Sends a password reset email to the user.
*   **Request Body:**
    *   `email` (string, required)
*   **Responses:**
    *   `200 OK`: Password reset email sent.
    *   `404 Not Found`: User with that email does not exist.

### POST /api/auth/reset-password

*   **Description:** Resets a user's password.
*   **Request Body:**
    *   `token` (string, required)
    *   `newPassword` (string, required)
*   **Responses:**
    *   `200 OK`: Password reset successfully.
    *   `400 Bad Request`: Invalid or expired token.

## Users

### GET /api/users/:username

*   **Description:** Gets a user's public profile.
*   **Parameters:**
    *   `username` (string, path, required)
*   **Responses:**
    *   `200 OK`: Returns user profile information.
    *   `404 Not Found`: User not found.

### PUT /api/users/:username

*   **Description:** Updates a user's profile.
*   **Authentication:** Required.
*   **Parameters:**
    *   `username` (string, path, required)
*   **Request Body:**
    *   `avatar_url` (string)
*   **Responses:**
    *   `200 OK`: Profile updated successfully.
    *   `401 Unauthorized`: Not authenticated.
    *   `403 Forbidden`: Not authorized to update this profile.
    *   `404 Not Found`: User not found.

## Subreddits

### GET /api/subreddits

*   **Description:** Gets a list of all subreddits.
*   **Query Parameters:**
    *   `sort` (string, optional, e.g., "popular", "new")
*   **Responses:**
    *   `200 OK`: Returns a list of subreddits.

### POST /api/subreddits

*   **Description:** Creates a new subreddit.
*   **Authentication:** Required.
*   **Request Body:**
    *   `name` (string, required)
    *   `description` (string, required)
*   **Responses:**
    *   `201 Created`: Subreddit created successfully.
    *   `400 Bad Request`: Invalid input.
    *   `401 Unauthorized`: Not authenticated.
    *   `409 Conflict`: Subreddit name already exists.

### GET /api/subreddits/:name

*   **Description:** Gets a specific subreddit.
*   **Parameters:**
    *   `name` (string, path, required)
*   **Responses:**
    *   `200 OK`: Returns subreddit information.
    *   `404 Not Found`: Subreddit not found.

## Posts

### GET /api/posts

*   **Description:** Gets a list of posts.
*   **Query Parameters:**
    *   `sort` (string, optional, e.g., "latest", "trending", "popular")
    *   `subreddit` (string, optional)
*   **Responses:**
    *   `200 OK`: Returns a list of posts.

### POST /api/subreddits/:name/posts

*   **Description:** Creates a new post in a subreddit.
*   **Authentication:** Required.
*   **Parameters:**
    *   `name` (string, path, required)
*   **Request Body:**
    *   `title` (string, required)
    *   `content` (string, optional)
    *   `media_url` (string, optional)
    *   `link_url` (string, optional)
    *   `poll` (object, optional)
*   **Responses:**
    *   `201 Created`: Post created successfully.
    *   `400 Bad Request`: Invalid input.
    *   `401 Unauthorized`: Not authenticated.
    *   `404 Not Found`: Subreddit not found.

### GET /api/posts/:id

*   **Description:** Gets a specific post.
*   **Parameters:**
    *   `id` (integer, path, required)
*   **Responses:**
    *   `200 OK`: Returns post information.
    *   `404 Not Found`: Post not found.

### PUT /api/posts/:id

*   **Description:** Updates a post.
*   **Authentication:** Required (must be owner or moderator).
*   **Parameters:**
    *   `id` (integer, path, required)
*   **Request Body:**
    *   `title` (string)
    *   `content` (string)
*   **Responses:**
    *   `200 OK`: Post updated successfully.
    *   `401 Unauthorized`: Not authenticated.
    *   `403 Forbidden`: Not authorized to update this post.
    *   `404 Not Found`: Post not found.

### DELETE /api/posts/:id

*   **Description:** Deletes a post.
*   **Authentication:** Required (must be owner or moderator).
*   **Parameters:**
    *   `id` (integer, path, required)
*   **Responses:**
    *   `204 No Content`: Post deleted successfully.
    *   `401 Unauthorized`: Not authenticated.
    *   `403 Forbidden`: Not authorized to delete this post.
    *   `404 Not Found`: Post not found.

## Comments

### GET /api/posts/:id/comments

*   **Description:** Gets all comments for a post.
*   **Parameters:**
    *   `id` (integer, path, required)
*   **Responses:**
    *   `200 OK`: Returns a list of comments.
    *   `404 Not Found`: Post not found.

### POST /api/posts/:id/comments

*   **Description:** Creates a new comment on a post.
*   **Authentication:** Required.
*   **Parameters:**
    *   `id` (integer, path, required)
*   **Request Body:**
    *   `content` (string, required)
    *   `parent_comment_id` (integer, optional)
*   **Responses:**
    *   `201 Created`: Comment created successfully.
    *   `400 Bad Request`: Invalid input.
    *   `401 Unauthorized`: Not authenticated.
    *   `404 Not Found`: Post not found.

## Votes

### POST /api/posts/:id/vote

*   **Description:** Votes on a post.
*   **Authentication:** Required.
*   **Parameters:**
    *   `id` (integer, path, required)
*   **Request Body:**
    *   `vote_type` (string, required, "upvote" or "downvote")
*   **Responses:**
    *   `200 OK`: Vote cast successfully.
    *   `400 Bad Request`: Invalid input.
    *   `401 Unauthorized`: Not authenticated.
    *   `404 Not Found`: Post not found.

### POST /api/comments/:id/vote

*   **Description:** Votes on a comment.
*   **Authentication:** Required.
*   **Parameters:**
    *   `id` (integer, path, required)
*   **Request Body:**
    *   `vote_type` (string, required, "upvote" or "downvote")
*   **Responses:**
    *   `200 OK`: Vote cast successfully.
    *   `400 Bad Request`: Invalid input.
    *   `401 Unauthorized`: Not authenticated.
    *   `404 Not Found`: Comment not found.
