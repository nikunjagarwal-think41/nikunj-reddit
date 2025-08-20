from server.database import SessionLocal, engine, Base
from server.crud import user as user_crud, subreddit as subreddit_crud, post as post_crud, comment as comment_crud, vote as vote_crud
from server.schemas import user as user_schema, subreddit as subreddit_schema, post as post_schema, comment as comment_schema, vote as vote_schema

def seed_data():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Create users
        users_in = [
            user_schema.UserCreate(username="testuser1", email="testuser1@example.com", password="password123"),
            user_schema.UserCreate(username="testuser2", email="testuser2@example.com", password="password456"),
            user_schema.UserCreate(username="testuser3", email="testuser3@example.com", password="password789"),
        ]
        users = []
        for user_in in users_in:
            db_user = user_crud.get_user_by_email(db, email=user_in.email)
            if not db_user:
                db_user = user_crud.create_user(db, user_in)
                print(f"User {db_user.username} created")
            else:
                print(f"User {db_user.username} already exists")
            users.append(db_user)

        # Create subreddits
        subreddits_in = [
            subreddit_schema.SubredditCreate(name="python", description="All about Python"),
            subreddit_schema.SubredditCreate(name="fastapi", description="A framework for building APIs with Python 3.7+"),
        ]
        subreddits = []
        for subreddit_in in subreddits_in:
            db_subreddit = subreddit_crud.get_subreddit_by_name(db, name=subreddit_in.name)
            if not db_subreddit:
                db_subreddit = subreddit_crud.create_subreddit(db, subreddit_in, creator_id=users[0].id)
                print(f"Subreddit {db_subreddit.name} created")
            else:
                print(f"Subreddit {db_subreddit.name} already exists")
            subreddits.append(db_subreddit)

        # Create posts
        posts_in = [
            post_schema.PostCreate(title="My first post in Python", content="This is my first post in the Python subreddit.", subreddit_name="python"),
            post_schema.PostCreate(title="FastAPI is awesome!", content="I am really enjoying using FastAPI.", subreddit_name="fastapi"),
        ]
        posts = []
        for i, post_in in enumerate(posts_in):
            db_post = post_crud.create_post(db, post_in, user_id=users[i % len(users)].id, subreddit_id=subreddits[i % len(subreddits)].id)
            print(f"Post '{db_post.title}' created")
            posts.append(db_post)

        # Create comments
        comments_in = [
            comment_schema.CommentCreate(content="Great post!"),
            comment_schema.CommentCreate(content="I agree, FastAPI is fantastic."),
        ]
        comments = []
        for i, comment_in in enumerate(comments_in):
            db_comment = comment_crud.create_comment(db, comment_in, user_id=users[(i + 1) % len(users)].id, post_id=posts[i % len(posts)].id)
            print(f"Comment '{db_comment.content}' created")
            comments.append(db_comment)

        # Create votes
        votes_in = [
            vote_schema.VoteCreate(post_id=posts[0].id, vote_type="upvote"),
            vote_schema.VoteCreate(post_id=posts[1].id, vote_type="upvote"),
            vote_schema.VoteCreate(comment_id=comments[0].id, vote_type="upvote"),
            vote_schema.VoteCreate(comment_id=comments[1].id, vote_type="downvote"),
        ]
        for vote_in in votes_in:
            vote_crud.create_vote(db, vote_in, user_id=users[2].id)
            print(f"Vote created")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()