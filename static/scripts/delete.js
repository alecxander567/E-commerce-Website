function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`/delete-product/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Product deleted successfully');
            } else {
                alert('Error deleting product: ' + data.error);
            }
        });
    }
}
