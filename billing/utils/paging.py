def paginate(query, page: int = 1, per_page: int = 50):
    return query.offset((page - 1) * per_page).limit(per_page)