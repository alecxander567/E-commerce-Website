function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


function fetchProducts() {
    fetch('/get-products/')
        .then(response => response.json())
        .then(data => {
            let productList = document.getElementById("product-list");
            productList.innerHTML = "";

            data.products.forEach(product => {
                let row = document.createElement("tr");

                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>$${product.price}</td>
                    <td>${product.category}</td>
                    <td>${product.quantity}</td>
                    <td>
                        <button class="btn buy-now" onclick="placeOrder('${product.id}', '${product.quantity}')">
                            Buy Now
                        </button>
                        <button class="btn add-to-cart" onclick="addToCart('${product.name}')">Add to Basket</button>
                    </td>
                `;

                productList.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching products:", error));
}


function placeOrder(productId) {
    fetch('/buy-product/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()  // Ensure CSRF protection
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: 1  // Reduce by only one
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Order placed successfully!");
            fetchOrders();  // Refresh order list
            location.reload(); 
        } else {
            alert("❌ Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}


function loadOrdersFromDB() {
    fetch('/get-orders/')
        .then(response => response.json())
        .then(data => {
            let dropdownProductList = document.getElementById("dropdownProductList");
            dropdownProductList.innerHTML = ""; // Clear previous items

            console.log("Received Orders:", data.orders); // Debugging

            if (data.orders.length === 0) {
                let emptyMessage = document.createElement("li");
                emptyMessage.classList.add("dropdown-item", "text-muted");
                emptyMessage.textContent = "No products added";
                dropdownProductList.appendChild(emptyMessage);
            } else {
                data.orders.forEach((order) => {
                    console.log("Order ID:", order.id); // Debugging

                    let newItem = document.createElement("li");
                    newItem.classList.add("dropdown-item", "d-flex", "justify-content-between", "align-items-center");
                    newItem.innerHTML = `
                        ${order.product_name} (x${order.quantity}) - $${order.total_price}
                        <button class="btn btn-sm text-danger remove-item"
                            onclick="console.log('Clicked:', this); removeOrderFromDB(${order.id}, this);">
                                X
                        </button>
                    `;
                    dropdownProductList.appendChild(newItem);
                });
            }
        })
        .catch(error => console.error("❌ Error fetching orders:", error));
}


function removeOrderFromDB(orderId, element) {
    console.log("Deleting Order ID:", orderId); // Debugging

    fetch(`/delete-order/${orderId}/`, { 
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Ensure CSRF protection
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error("❌ Server Response:", text);
                throw new Error(`HTTP ${response.status}: ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("✅ Delete Response:", data); // Debugging
        if (data.message) {
            element.parentElement.remove(); // Remove from UI
            alert("✅ Order deleted successfully!");

            fetchProducts();  // Refresh the product list to update the quantity
        } else {
            alert("Failed to delete order!");
        }
    })
    .catch(error => {
        console.error("❌ Error deleting order:", error);
        alert("An error occurred. Check the console for details.");
    });
}


function updateProductQuantity(productName, newQuantity) {
    console.log(`🔄 Updating ${productName} quantity to:`, newQuantity); // Debugging

    let rows = document.querySelectorAll("#product-list tr");
    rows.forEach(row => {
        let nameCell = row.children[0];
        if (nameCell.textContent.trim() === productName.trim()) {
            let quantityCell = row.children[3]; // 4th column (index 3)
            console.log("✅ Quantity Updated:", quantityCell); // Debugging
            quantityCell.textContent = newQuantity;
        }
    });
}


// Call this function when the page loads
window.onload = function () {
    fetchProducts();  // Load products from the database
    loadOrdersFromDB();  // Load orders from the database
};


  // Function to add product to cart
  function addToCart(productName) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Check if the product already exists in cart
    let existingItem = cart.find(item => item.name === productName);

    if (existingItem) {
        existingItem.quantity += 1; // Increase quantity
    } else {
        cart.push({ name: productName, quantity: 1 }); // Add new product
    }

    // Save updated cart to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Update the cart dropdown
    updateCartDropdown();
    alert(`${productName} has been added to your basket! ✅`);
}


  // Function to remove product from cart
  function removeFromCart(productName) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.name !== productName); // Remove item

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDropdown();
}


 // Function to update the cart dropdown
 function updateCartDropdown() {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let cartList = document.getElementById('cartItemList');
    cartList.innerHTML = '';

    if (cart.length === 0) {
        cartList.innerHTML = '<li class="dropdown-item text-muted">Basket is empty</li>';
    } else {
        cart.forEach(item => {
            let li = document.createElement('li');
            li.classList.add('dropdown-item', 'd-flex', 'justify-content-between', 'align-items-center');

            li.innerHTML = `
                ${item.name} - ${item.quantity}
                <button class="btn text-danger" onclick="removeFromCart('${item.name}')">X</button>
            `;
            cartList.appendChild(li);
        });
    }
}

document.addEventListener("DOMContentLoaded", updateCartDropdown);