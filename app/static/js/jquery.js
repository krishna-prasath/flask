//always remember Jquery goes in seperate file
$(document).ready(function(){
    $("a#disabled").detach();
    $('#myTable').DataTable();
  }
  );
  
  function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
  }