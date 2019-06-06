function Func_search() {
    url = '/search/?'
    // if($("#buttonSelectSchool").text() != "选择学校"){
    //   url += "school=" + $("#buttonSelectSchool").text() + "&"
    // }
    if($("#buttonSelectDepartment").text() != "选择专业"){
      url += "department=" + $("#buttonSelectDepartment").text() + "&"
    }
    url += "keywords=" + $("#searchboxCourse").val() + "&"
    url += "page=" + "1"
    window.location.href = url
}

function clickSearchButton() {
  //alert("!!!")
  $("#searchboxCourse").select()
}

$(document).ready(function() {
  //alert("!!!")
  //$("#navbarContainer").load("./components/indexNavbarContainer.html")
    //$("#menuUser").hide()
    //$("#menuLogin").hide()
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
    console.log($("#buttonSelectSchool").text())
    $.ajax('/getDepartment/',{
      dataType:'json',
      data:{'school':$("#buttonSelectSchool").text()}
    }).done(function(data) {
      var departmentList = $("#departmentList")
      departmentList.children().remove()
      departmentList.prev().text("选择专业")
      for (var i = 0; i < data.department.length; i++) {
        departmentList.append("<a class='dropdown-item btn btn-primary department' href='javascript:void(0)'>" +
         data.department[i] + "</a>")
      }
      $(".dropdown-item.department").click(function() {
        $(this).parent().prev().text($(this).text())
      })
    })
    $("#searchboxCourse").keyup(function(event) {
        if (event.keyCode == 13) {
            Func_search()
        }
      })
  })
