
$('.status-button').on('click', function() {
  let itemId = $(this).data('item-id');
  let status = $(this).data('status');

  const csrftoken = getCookie('csrftoken')

  $.ajaxSetup({
    headers: {
      'X-CSRFToken': csrftoken
    }
  });

  $.ajax({
    url: `/dashboard/order-list/${status}/`,
    type: 'POST',
    data: { itemId: itemId },
    success: function(response) {

      console.log('Item updated successfully');

      window.location.reload();
    },
    error: function(xhr, status, error) {

      console.error('Error updating item:', error);
    }
  });
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}