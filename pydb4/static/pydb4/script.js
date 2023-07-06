// // Get the necessary elements
// var profileButton = document.getElementById("profileButton");
// var dropdownOptions = document.getElementById("dropdownOptions");

// // Add event listeners for mouseover and mouseout
// profileButton.addEventListener("mouseover", function() {
//   dropdownOptions.style.display = "block";
// });

// profileButton.addEventListener("mouseout", function() {
//   setTimeout(function() {
//   dropdownOptions.style.display = "none";
// }, 3000); // Delay execution for 2000 milliseconds (2 seconds)
// });


// var itemEdits = document.getElementById("modTable")
// var history = document.getElementById("history")

var historyButton = document.getElementById("history");
var itemEdits = document.getElementById("modTable");


if (historyButton && itemEdits) {

  historyButton.addEventListener("mouseover", function() {
    itemEdits.style.display = "block";
  });

  historyButton.addEventListener("mouseout", function() {
    setTimeout(function() {
      itemEdits.style.display = "none";
    }, 3000);
  });
}



// const products = document.querySelectorAll('.product');
// // Add event listeners for drag events
// products.forEach(product => {
//   product.addEventListener('dragstart', dragStart);
//   product.addEventListener('dragover', dragOver);
//   product.addEventListener('dragenter', dragEnter);
//   product.addEventListener('dragleave', dragLeave);
//   product.addEventListener('drop', drop);
//   product.addEventListener('dragend', dragEnd);
//   product.addEventListener('dragstart', dragStart);
// });
// // Drag event handlers
// function dragStart(event) {
//   event.dataTransfer.setData('text/plain', event.target.id);
//   event.target.classList.add('dragging');
// }
// function dragOver(event) {
//   event.preventDefault();
// }
// function dragEnter(event) {
//   event.target.classList.add('hovered');
// }
// function dragLeave(event) {
//   event.target.classList.remove('hovered');
// }
// function drop(event) {
//   event.preventDefault();
//   const data = event.dataTransfer.getData('text/plain');
//   const draggableElement = document.getElementById(data);
//   event.target.appendChild(draggableElement);
//   event.target.classList.remove('hovered');
// }
// function dragEnd(event) {
//   event.target.classList.remove('dragging');
// }
// // JavaScript code for drag and drop functionality
// // Get the reference to the hovering container
// var cartContainer = document.getElementById('cart-container');
// // Add event listeners for drag and drop events
// cartContainer.addEventListener('dragenter', dragEnter, false);
// cartContainer.addEventListener('dragover', dragOver, false);
// cartContainer.addEventListener('dragleave', dragLeave, false);
// cartContainer.addEventListener('drop', drop, false);
// // Event handlers for drag and drop events
// function handleDragEnter(event) {
//   // Add CSS class or styles to indicate the hovering container is active
//   cartContainer.classList.add('drag-over');
// }
// function handleDragOver(event) {
//   // Prevent the default behavior which is to not allow dropping
//   event.preventDefault();
// }
// function handleDragLeave(event) {
//   // Remove CSS class or styles to indicate the hovering container is not active
//   cartContainer.classList.remove('drag-over');
// }
// function handleDrop(event) {
//   // Prevent the default behavior which is to open the dropped item as a link
//   event.preventDefault();
//   // Process the dropped item and add it to the cart or perform any desired actions
//   var droppedItem = event.dataTransfer.getData('text/plain');
//   // Perform your logic here to handle the dropped item
//   // Remove CSS class or styles to indicate the hovering container is not active
//   cartContainer.classList.remove('drag-over');
// }