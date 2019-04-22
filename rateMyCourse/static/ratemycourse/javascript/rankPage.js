function validateSignUp() {
  $("#formRegister").validate({
    submitHandler: function() {
      Func_signUp();
    },
    rules: {
      inputEmail: {
        required: true,
	      email: true
      },
      inputUsername: {
        required: true,
	      minlength: 2
	    },
	    inputPassword: {
	      required: true,
	      minlength: 5
	    },
      inputVerify: {
        required: true,
	      minlength: 5,
	      equalTo: "#inputPassword"
      }
    },
    messages: {
      inputEmail: "请输入正确的邮箱地址",
      inputUsername: {
        required: "请输入用户名",
        minlength: "用户名长度不能小于2个字符"
      },
      inputPassword: {
        required: "请输入密码",
        minlength: "密码长度不能小于5个字符"
      },
      inputVerify: {
        required: "请再次输入密码",
        minlength: "密码长度不能小于5个字符",
        equalTo: "密码输入不一致"
      }
    }
  })
}

function validateSignIn() {
  $("#formLogin").validate({
    submitHandler: function() {
      Func_signIn();
    },
    rules: {
      username: {
        required: true,
	      minlength: 2
	    },
	    password: {
	      required: true,
	      minlength: 5
	    }
    },
    messages: {
      username: {
        required: "请输入用户名",
        minlength: "用户名必须由至少2个字符组成"
      },
      password: {
        required: "请输入密码",
        minlength: "密码长度不能小于5个字符"
      }
    }
  })
}

function Func_signUp() {
  $.ajax("/signUp/", {
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#inputUsername").val(),
      "mail": $("#inputEmail").val(),
      "password": $("#inputPassword").val(),
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.errormessage)
    } else {
        $("#menuUser").prop("hidden",false)
        $("#menuLogin").prop("hidden",true)
      // $("#menuLogin").hide()
      // $("#menuUser").show()
      $("#navUser").text(data.username)
      $.cookie('username', data.username, {path: '/'})
    }
  })
  return false
}

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

function Func_signIn() {
  $.ajax("/signIn/", {
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#username").val(),
      "password": $("#password").val()
    }
  }).done(function(data) {
    if(data.statCode != 0) {
      alert(data.errormessage)
    } else {
        $("#menuUser").prop("hidden",false)
        $("#menuLogin").prop("hidden",true)
      // $("#menuLogin").hide()
      // $("#menuUser").show()
      $("#navUser").text(data.username)
      // $("#modalInfo").show()
      $.cookie('username', data.username, {path: '/'})
    }
  })
  return false
}

function Func_signOut() {
    $("#menuUser").prop("hidden",true)
    $("#menuLogin").prop("hidden",false)
  // $("#menuUser").hide()
  // $("#menuLogin").show()
  // $("#modalInfo").hide()
  $.removeCookie('username', {path: '/'})
  return false
}

function Func_toUserInfo(){
    url = '/userInfo/?'
    url += "name=" + $("#navUser").text()
    window.location.href = url
    return false
}

$(document).ready(function() {
  // alert("!!!")
  // Form validation for Sign in / Sign up forms
  //$("#menuLogin").load("./test.html")
  validateSignUp()
  validateSignIn()

  // Login widget set according to cookie
  if($.cookie('username') == undefined) {
      $("#menuUser").prop("hidden",true)
      $("#menuLogin").prop("hidden",false)
    // $("#menuUser").hide()
    // $("#menuLogin").show()
  }
  else{
      $("#menuUser").prop("hidden",false)
      $("#menuLogin").prop("hidden",true)
    // $("#menuLogin").hide()
    // $("#menuUser").show()
    $("#navUser").text($.cookie('username'))
  }
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

