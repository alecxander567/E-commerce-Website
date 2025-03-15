function editProduct(productId) {
    const name = document.getElementById('product-name').value;
    const price = document.getElementById('product-price').value;
    const category = document.getElementById('product-category').value;
    const quantity = document.getElementById('product-quantity').value;

    const data = {
        name: name,
        price: price,
        category: category,
        quantity: quantity
    };

    fetch(`/edit-product/${productId}/`, {
        method: 'POST',
        body: new URLSearchParams(data),
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product updated successfully');
        } else {
            alert('Error updating product: ' + data.error);
        }
    });
}
