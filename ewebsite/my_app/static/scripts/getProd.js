function fetchProducts() {
    fetch('/get-products/')  // Update with your actual URL
        .then(response => response.json())
        .then(data => {
            console.log(data);
                // Ensure the response contains 'products'
                if (!data || !data.products || !Array.isArray(data.products)) {
                    console.error("Invalid data structure:", data);
                    return;
                }

                const productTableBody = document.getElementById('productTableBody');
                productTableBody.innerHTML = '';

                console.log(productTableBody);

                if (data.products.length === 0) {
                    productTableBody.innerHTML = '<tr><td colspan="5" class="text-center">No products available</td></tr>';
                    return;
                }

             // Loop through products array and populate table
             data.products.forEach(product => {
                console.log("Processing product:", product);  // Debugging log

                const row = document.createElement('tr');
                const editUrl = `/edit_product/${product.id}/`;  // Ensure proper URL form
                // Add other cells...
              
                row.innerHTML = `
                    <td>${product.name || 'N/A'}</td>
                    <td>${product.category || 'N/A'}</td>
                    <td>$${product.price || '0.00'}</td>
                    <td>${product.quantity || 0}</td>
                    <td><a class="btn btn-success" href="${editUrl}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 20 20">
                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                        </svg>Edit
                        </a>
                          <button class="btn btn-danger" onclick="deleteProduct(${product.id})">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-square-fill" viewBox="0 0 20 20">
                                <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm3.354 4.646L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708"/>
                            </svg>Delete
                        </button>
                    </td>
                `;
                productTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', fetchProducts);

function deleteProduct(productId) {
    if (confirm("Are you sure you want to delete this product?")) {
        const csrfToken = document.querySelector("#csrf_token").value; // Get CSRF token

        fetch(`/delete_product/${productId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // CSRF protection
            },
            body: JSON.stringify({}) // Send empty JSON body
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                fetchProducts(); // Refresh product list after deletion
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error deleting product:", error));
    }
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    const name = "csrftoken=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookies = decodedCookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
}

