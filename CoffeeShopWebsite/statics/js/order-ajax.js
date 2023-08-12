
$('.status-button').on('click', function() {
  let itemId = $(this).data('item-id');
  let status = $(this).data('status');

  $.ajax({
    url: `/dashboard/order-list/${status}/`,
    type: 'POST',
    data: { itemId: itemId },
    success: function(response) {

      console.log('Item deleted successfully');

      window.location.reload();
    },
    error: function(xhr, status, error) {

      console.error('Error deleting item:', error);
    }
  });
});