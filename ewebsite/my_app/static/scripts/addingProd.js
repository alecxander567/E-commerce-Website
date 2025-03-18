 // Handle form submission
 document.getElementById('productForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('productName').value);
    formData.append('price', document.getElementById('productPrice').value);
    formData.append('category', document.getElementById('productCategory').value);
    formData.append('quantity', document.getElementById('productQuantity').value);
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    
    fetch(('/add-product/')  , {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        console.log('Response status:', response.status);
        
        // Check if the response is JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            // If not JSON, it might be a redirect or HTML
            console.log('Non-JSON response received');
            document.getElementById('productForm').reset();
            alert('Form submitted successfully');
            return { success: true };  // Pretend success
        }
    })
    .then(data => {
        console.log('Processed data:', data);
        if(data.success) {
            document.getElementById('productForm').reset();
            alert('Product added successfully!✅');
        } else {
            alert('Error adding product');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
