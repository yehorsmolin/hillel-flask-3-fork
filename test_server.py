import requests


def test_product_create():
    # Create a product
    response = requests.post('http://localhost:5001/products', json={
        'name': 'Sandora',
        'price': 10,
    })

    print(response.status_code)
    print(response.json())


def test_product_update():
    # Update a product
    response = requests.put('http://localhost:5001/products/4', json={
        'name': 'Моршинська',
        'price': 10,
    })

    print(response.status_code)
    print(response.json())


def test_product_delete():
    # Delete a product
    response = requests.delete('http://localhost:5001/products/2')

    print(response.status_code)
    print(response.content)


def test_product_invalid_price():
    # Create a product
    response = requests.post('http://localhost:5001/products', json={
        'name': 'Ліщина',
        'price': -10,
    })

    print(response.status_code)
    print(response.json())


def test_product_update_invalid_price():
    # Update a product
    response = requests.put('http://localhost:5001/products/4', json={
        'name': 'Моршинська',
        'price': -10,
    })

    print(response.status_code)
    print(response.json())


def test_product_update():
    # Update a product
    response = requests.patch('http://localhost:5001/products/40000', json={
        'name': 'Borjomi',
        'price': 100,
    })

    print(response.status_code)
    print(response.json())


def test_create_beer():
    # Create a product
    response = requests.post('http://localhost:5001/products', json={
        'name': 'Львівське',
        'price': 50,
        'category': 5,
    })

    print(response.status_code)
    print(response.json())


def test_category_create():
    # Create a category
    response = requests.post('http://localhost:5001/categories', json={
        'name': 'Beer',
        'is_adult_only': False,
    })

    if response.status_code == 500:
        print('Server error')
    else:
        print(response.status_code)
        print(response.json())


def test_category_update():
    # Update a category
    response = requests.put(f'http://localhost:5001/categories/2', json={
        'name': 'COD',
        'is_adult_only': False,
    })
    if response.status_code == 404:
        print(f'Category does not exist. Status code: {response.status_code}')
    else:
        print(response.status_code)
        print(response.json())

def test_category_delete(category_id):
    # Delete a category
    response = requests.delete(f'http://localhost:5001/categories/{category_id}')

    if response.status_code == 500:
        print('Server error.')
    else:
        print(response.status_code)
        print('Category deleted.')


if __name__ == "__main__":
    test_category_update()