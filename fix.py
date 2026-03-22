import re

with open('repo/main.py', 'r') as f:
    content = f.read()

# Remove search_movies function from the end
search_func = r"""#  SEARCH \+ PAGINATION
@app\.get\("/movies/search"\)
def search_movies\(
    keyword: Optional\[str\] = None,
    min_rating: Optional\[float\] = None,
    page: int = 1,
    limit: int = 5
\):
    results = movies

    if keyword:
        results = \[m for m in results if keyword\.lower\(\) in m\["name"\]\.lower\(\)\]

    if min_rating is not None:
        results = \[m for m in results if m\["rating"\] >= min_rating\]

    start = \(page - 1\) \* limit
    end = start \+ limit

    return {
        "total": len\(results\),
        "data": results\[start:end\]
    }"""

content = re.sub(search_func, '', content)

# Insert it before get_movie
insert_point = r"""@app\.get\("/movies/\{movie_id\}"\)
def get_movie\(movie_id: int\):"""

search_func_unquoted = """#  SEARCH + PAGINATION
@app.get("/movies/search")
def search_movies(
    keyword: Optional[str] = None,
    min_rating: Optional[float] = None,
    page: int = 1,
    limit: int = 5
):
    results = movies

    if keyword:
        results = [m for m in results if keyword.lower() in m["name"].lower()]

    if min_rating is not None:
        results = [m for m in results if m["rating"] >= min_rating]

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": len(results),
        "data": results[start:end]
    }

"""

content = re.sub(insert_point, search_func_unquoted + insert_point.replace('\\', ''), content)

# fix the empty requireents.txt by renaming it and adding actual requirements
with open('repo/requirements.txt', 'w') as f:
    f.write('fastapi\nuvicorn\npydantic\n')

with open('repo/main.py', 'w') as f:
    f.write(content)
