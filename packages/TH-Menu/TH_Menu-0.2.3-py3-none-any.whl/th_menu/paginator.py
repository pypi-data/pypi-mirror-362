def paginate_items(items: list, per_page: int = 25) -> list[list]:
    return [items[i:i + per_page] for i in range(0, len(items), per_page)]
