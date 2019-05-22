function Func_search_course() {
    url = '/search/?'
    url += "keywords=" + $("#searchCourse").val()
    url += "&page=1"
    window.location.href = url
}

$(document).ready(function() {
  // alert("!!!")
  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()
  $("#searchCourse").keyup(function(event) {
          if (event.keyCode == 13) {
              Func_search_course()
          }
        })
  // Login widget set according to cookie
  // if ($.cookie('username') == undefined || $.cookie('userid') == undefined) {
  //     $("#menuUser").prop("hidden",true)
  //     $("#menuLogin").prop("hidden",false)
  //     // $("#menuUser").hide()
  //     // $("#menuLogin").show()
  // }
  // else {
  //     $("#menuUser").prop("hidden",false)
  //     $("#menuLogin").prop("hidden",true)
  //     // $("#menuLogin").hide()
  //     // $("#menuUser").show()
  //     $("#navUser").text($.cookie('username'))
  // }
})
