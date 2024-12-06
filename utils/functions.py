def is_healthy(calories: int, veg: bool) -> bool:
    return (calories < 100 or veg)


def count_calories(ingredients_calories: list[int]) -> float:
    return round(0.95*sum(ingredients_calories), 2)


def costs(ingredients: list[dict]) -> float:
    if len(ingredients) != 3:
        raise ValueError("Ingredients list must contain 3 elements.")
    
    if not all("price" in ingredient for ingredient in ingredients):
        raise ValueError("Ingredients must have a key 'price'")
    
    return sum(ingredient["price"] for ingredient in ingredients)


def profitability(saleprice: int, ingredients: list[dict]) -> float:
    return saleprice - costs(ingredients)


def best_product(products: list[dict]) -> str:
    if len(products) != 4:
        raise ValueError("Products list must contain 4 elements.")
    
    if not all("profitability" in product for product in products):
        raise ValueError("Products must have a key 'profitability'")

    best = max(products, key= lambda product: product.get("profitability"))

    return best.get("name")