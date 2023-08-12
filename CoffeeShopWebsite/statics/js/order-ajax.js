//
// $('.delete-button').on('click', function() {
//   var itemId = $(this).data('item-id');
//
//   $.ajax({
//     url: '/delete-item',
//     type: 'POST',
//     data: { itemId: itemId },
//     success: function(response) {
//
//       console.log('Item deleted successfully');
//
//       $(this).closest('.item').remove();
//     },
//     error: function(xhr, status, error) {
//
//       console.error('Error deleting item:', error);
//     }
//   });
// });