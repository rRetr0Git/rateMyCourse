$(function(){
  $(":radio").click(function(){
      if($(this).val()=="option1"){
        $("#top_courses").show()
        $("#top_teachers").hide()
      }
      else{
        $("#top_teachers").show()
        $("#top_courses").hide()
      }
  });
 });

$(document).ready(function() {
  // alert("!!!")
  // Form validation for Sign in / Sign up forms
  //$("#menuLogin").load("./test.html")
  validateSignUp()
  validateSignIn()

  // Login widget set according to cookie
  // if($.cookie('userid') == undefined || $.cookie('username') == undefined) {
  //     $("#menuUser").prop("hidden",true)
  //     $("#menuLogin").prop("hidden",false)
  //   // $("#menuUser").hide()
  //   // $("#menuLogin").show()
  // }
  // else{
  //     $("#menuUser").prop("hidden",false)
  //     $("#menuLogin").prop("hidden",true)
  //   // $("#menuLogin").hide()
  //   // $("#menuUser").show()
  //   $("#navUser").text($.cookie('username'))
  // }
  $("#top_courses").show()
  $("#top_teachers").hide()

//  $.ajax('/getTeachers/', {
//    dataType:'json',
//    data:{
//      'courseTeacherId':window.location.pathname.split('/')[2]
//    }
//  }).done(function(data) {
//    var teacherList = $("#teacherList")
//    for (var i = 0; i < data.teachers.length; i++) {
//      teacherList.append("<a class='dropdown-item btn btn-primary teacher' href='javascript:void(0)'>" + data.teachers[i] + "</a>")
//    }
//    $(".dropdown-item.teacher").click(function() {
//      $(this).parent().prev().text($(this).text())
//    })
//  })
})

