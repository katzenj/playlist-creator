$(document).ready(function() {
  $(".submit_button").on('click', function() {
    $("#loading-spinner").css("display", "flex");
    $(".input_container").css("display", "none");
  })
});
