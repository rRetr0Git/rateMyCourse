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
      "captcha": $("#inputCaptcha").val()
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.errormessage);
    } else {
        $("#menuUser").prop("hidden",false)
        $("#menuLogin").prop("hidden",true)
      //$("#menuLogin").hide()
      //$("#menuUser").show()
      //$("#navUser").text(data.username)
      //$.cookie('userid', data.userid, {path: '/'})
        alert("激活邮件已发送至您的邮箱，请及时查看")
        location.replace(location);
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
      "password": $("#password").val(),
      "captcha": $("#captcha").val()
    }
  }).done(function(data) {
    if(data.statCode !== 0) {
      alert(data.errormessage);
    }
    else {
    //     $("#menuUser").prop("hidden",false);
    //     $("#menuLogin").prop("hidden",true);
    //   //$("#menuLogin").hide()
    //   //$("#menuUser").show()
    //     $("#navUser").text(data.username);
    //   //$("#modalInfo").show()
    //   //$.cookie('username', data.username, {path: '/'})
          location.replace(location);
    }
  });
  return false
}

function Func_signOut() {
  $.ajax("/signOut/", {
    dataType: 'json',
    type: 'POST',
    data: {}
  }).done(function(data) {
    if(data.statCode !== 0) {
      alert(data.errormessage);
    }
    else {
        //$("#menuUser").prop("hidden",true)
        //$("#menuLogin").prop("hidden",false)
        location.replace(location);
    }
  });
  return false
}

function Func_toUserInfo(){
    url = '/userInfo/?'
    url += "name=" + $("#navUser").text()
    window.location.href = url
    return false
}

function Func_saveUserInfo(){
    // if($.cookie('userid') == undefined || $.cookie('username') == undefined){
    //     alert("please log in first!")
    //     return false
    // }
    // else if($.cookie('userid') !=$("#nickName").text()){
    //     alert("you cannot change other's info!")
    //     return false
    // }
    url = this.href
    $.ajax("/saveUserInfo/", {
        dataType: 'json',
        type: 'POST',
        async : false,
        data: {
          "school": $("#school").val(),
          "department": $("#department").val(),
          //"username": $("#navUser").text(),
        }
    });
    location.replace(location);
    return false;
}

function Func_saveUserPic(){
    // if($.cookie('userid') == undefined || $.cookie('username') == undefined){
    //     alert("please log in first!")
    //     return false
    // }
    // else if($.cookie('username') !=$("#nickName").text()){
    //     alert("you cannot change other's info!")
    //     return false
    // }
    Url = this.href;
    var formData = new FormData();
    formData.append("file",$("#inputfile")[0].files[0]);
    //formData.append("username",$("#navUser").text());
    $.ajax("/saveUserPic/", {
        url : Url,
        type : 'POST',
        data : formData,
        async : false,
        processData : false,
        contentType : false,
    });
    location.replace(location);
    return false;
}

function Func_getCaptcha(){
    $.ajax("/getCaptcha/", {
        dataType: 'json',
        type: 'POST',
        data: {}
    }).done(function(data) {
        var captchaImg1 = $("#captchaImg1");
        captchaImg1.children().remove();
        captchaImg1.append("<img src=\"" + data.sign_in_captcha_url +"\">");
        var captchaImg2 = $("#captchaImg2");
        captchaImg2.children().remove();
        captchaImg2.append("<img src=\"" + data.sign_up_captcha_url +"\">");
    });
    return false;
}