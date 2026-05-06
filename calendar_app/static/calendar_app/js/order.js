const list = document.getElementById('sortable-list');
const input = document.getElementById('orderInput');
const form = document.getElementById('orderForm');

new Sortable(list, {
    animation: 150,
    ghostClass: "bg-light",
    onSort: updateOrder
});

function updateOrder() {
    const order = [];

    document.querySelectorAll('#sortable-list li').forEach(li => {
        order.push(li.dataset.id);
    });

    input.value = order.join(',');
}

// inicializar
updateOrder();

// asegurar envío correcto
form.addEventListener('submit', updateOrder);