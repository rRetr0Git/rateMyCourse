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
        minlength: "用户名必需由两个字符组成"
      },
      password: {
        required: "请输入密码",
        minlength: "密码长度不能小于 5 个字符"
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
        //$("#menuLogin").hide()
        //$("#menuUser").show()
      $("#navUser").text(data.username)
      $.cookie('username', data.username, {path: '/'})
    }
  })
  return false
}

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
        //$("#menuLogin").hide()
        //$("#menuUser").show()
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

var score=[0,0,0,0];

function chooseScore(id){
  var c0="#B";
  var c1=id.charAt(1);
  var c2=id.charAt(2);
  var i=2;
  score[parseInt(c1)-1]=parseInt(c2);
  for(i=1;i<=parseInt(c2);i++)
  {
    var s=c0.concat(c1.concat(i.toString()));
    $(s).removeClass("fa fa-star-o text-dark");
    $(s).addClass("fa fa-star text-warning");

  }
  for(i=5;i>parseInt(c2);i--)
  {
    var s=c0.concat(c1.concat(i.toString()));
  	$(s).removeClass("fa fa-star text-warning");
   	$(s).addClass("fa fa-star-o text-dark");
  }
}

function choose_term(text){

  //$(this).parent().prev().text($(this).text());
  var termList = $("#termList")
  termList.prev().text(text);
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

function Func_submit() {

  if($.cookie('username') == undefined){
    alert("please log in first!")
    return false
  }
//  if($('#buttonSelectTerm').text() == '选择学期'){
//    alert("please choose your term!")
//  	return false
//  }
  if($('#writeCommentText').val().length < 10){
    alert('please write more for your course!(more than 10 characters)')
	return false
  }
  for(i = 0; i　< score.length; i++){
    if(score[i] == 0){
      alert('please rate for all aspect!')
      return false
    }
  }

  $.ajax("/submitComment/", {
    dataType: 'json',
    type: 'POST',
    traditional: true,
    data: {
      'username': $.cookie('username'),
      'courseteacher': window.location.pathname.split('/')[2],
      'anonymous': document.getElementById('anonymous').checked,
      'comment': $('#writeCommentText').val(),
      'rate':score,
      // rates
    }
  }).done(function (data) {
    if(data.statCode == 0){
      alert("your comment submited succesfully!")
      window.location.href = '../'
    }
    else {
      alert(data.errormessage)
    }
  })
}
