$(document).ready(function() {
  // alert("!!!")
  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()

  // Login widget set according to cookie
  if ($.cookie('username') == undefined) {
      $("#menuUser").hide()
      $("#menuLogin").show()
  }
  else {
      $("#menuLogin").hide()
      $("#menuUser").show()
      $("#navUser").text($.cookie('username'))
  }
})
