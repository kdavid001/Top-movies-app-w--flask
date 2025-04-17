from db import session, Movies

# Find the movie by its title (or any unique identifier like ID)
movie_to_delete = session.query(Movies).filter_by(id=4).first()

if movie_to_delete:
    session.delete(movie_to_delete)
    session.commit()
    print(f"Deleted movie: {movie_to_delete.id}")
else:
    print("Movie not found")