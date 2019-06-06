var jQuery = $(document).ready(function() {
  //alert("!!!")
  //$("#navbarContainer").load("./components/indexNavbarContainer.html")

  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()
  validateResetPwd()

  // Login widget set according to cookie
  // if($.cookie('username') == undefined || $.cookie('userid') == undefined) {
  //     $("#menuUser").prop("hidden",true)
  //     $("#menuLogin").prop("hidden",false)
  //   //$("#menuUser").hide()
  //   //$("#menuLogin").show()
  // }
  // else{
  //     $("#menuUser").prop("hidden",false)
  //     $("#menuLogin").prop("hidden",true)
  //   //$("#menuLogin").hide()
  //   //$("#menuUser").show()
  //   $("#navUser").text($.cookie('username'))
  // }
});