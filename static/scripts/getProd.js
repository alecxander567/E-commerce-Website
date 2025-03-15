function fetchProducts() {
    fetch('/get-products/')  // Update with your actual URL
        .then(response => response.json())
        .then(data => {
            const productTableBody = document.getElementById('productTableBody');
            // Clear any existing rows
            productTableBody.innerHTML = '';

            if (data.products && data.products.length > 0) {
                // Loop through each product and add it to the table
                data.products.forEach(product => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${product.name}</td>
                        <td>${product.category}</td>
                        <td>${product.price}</td>
                        <td>${product.quantity}</td>
                    `;
                    productTableBody.appendChild(row);
                });
            } else {
                // If no products are found, show a message
                productTableBody.innerHTML = '<tr><td colspan="5">No products available</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', function () {
    fetchProducts();
});
