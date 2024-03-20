// Ensure all DOM elements are loaded before executing scripts
document.addEventListener("DOMContentLoaded", function() {
    // Function to handle adding an item
    const addItem = () => {
        const nameInput = document.querySelector("#itemName");
        const quantityInput = document.querySelector("#itemQuantity");
        const priceInput = document.querySelector("#itemPrice");

        // Validate inputs for emptiness and positive values
        if (!nameInput.value.trim() || !quantityInput.value.trim() || !priceInput.value.trim()) {
            alert("Please fill in all fields.");
            return;
        }
        if (parseInt(quantityInput.value, 10) < 0 || parseFloat(priceInput.value) < 0) {
            alert("Quantity and price must be positive numbers.");
            return;
        }

        // Construct item object
        const item = {
            name: nameInput.value.trim(),
            quantity: parseInt(quantityInput.value, 10),
            price: parseFloat(priceInput.value)
        };

        // Send item to server using Fetch API
        fetch("/add-item", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(item),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Clear input fields
                nameInput.value = "";
                quantityInput.value = "";
                priceInput.value = "";

                // Reload items list
                loadItems();
            } else {
                alert("Failed to add item. Please try again.");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to add item due to a network error. Please try again.');
        });
    };

    // Function to load items and display them in the table
    const loadItems = () => {
        const itemsTableBody = document.querySelector("#itemsTable tbody");

        // Fetch items from server
        fetch("/get-items")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Clear existing items
            itemsTableBody.innerHTML = "";

            // Add items to table
            data.items.forEach(item => {
                const row = itemsTableBody.insertRow();
                row.innerHTML = `<td>${item.name}</td><td>${item.quantity}</td><td>${item.price.toFixed(2)}</td>`;
            });
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to load items due to a network error. Please try again.');
        });
    };

    // Attach event listeners
    document.querySelector("#addItemButton").addEventListener("click", addItem);

    // Initial load of items
    loadItems();
});
