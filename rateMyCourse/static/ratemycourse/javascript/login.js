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
      $("#menuLogin").hide()
      $("#menuUser").show()
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
      $("#menuLogin").hide()
      $("#menuUser").show()
      $("#navUser").text(data.username)
      $.cookie('username', data.username, {path: '/'})
    }
  })
  return false
}

function Func_signOut() {
  $("#menuUser").hide()
  $("#menuLogin").show()
  $.removeCookie('username', {path: '/'})
  return false
}
