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
        alert("激活邮件已发送至您的邮箱，请及时查收")
        //alert("注册成功！");
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
        if (data.statCode == 1) {
            // todo : jump to admin.html
        }
        else{
            location.replace(location);
        }
    //     $("#menuUser").prop("hidden",false);
    //     $("#menuLogin").prop("hidden",true);
    //   //$("#menuLogin").hide()
    //   //$("#menuUser").show()
    //     $("#navUser").text(data.username);
    //   //$("#modalInfo").show()
    //   //$.cookie('username', data.username, {path: '/'}
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
        captchaImg1.append("<img src=\"" + data.sign_in_captcha_url +"\" title=\"看不清？换一张\" onclick=\"Func_changeCaptcha()\">");
        captchaImg1.append("<ul class=\"list-unstyled\">\n" +
                           "<a href=\"javascript:void(0)\" onclick=\"Func_changeCaptcha()\" class=\"text-muted\">看不清，换一张</a>\n" +
                           "</ul>");
        var captchaImg3 = $("#captchaImg3");
        captchaImg3.children().remove();
        captchaImg3.append("<img src=\"" + data.resetPWD_captcha_url +"\" title=\"看不清？换一张\" onclick=\"Func_changeCaptcha()\">");
        captchaImg3.append("<ul class=\"list-unstyled\">\n" +
                           "<a href=\"javascript:void(0)\" onclick=\"Func_changeCaptcha()\" class=\"text-muted\">看不清，换一张</a>\n" +
                           "</ul>");
        var captchaImg2 = $("#captchaImg2");
        captchaImg2.children().remove();
        captchaImg2.append("<img src=\"" + data.sign_up_captcha_url +"\" title=\"看不清？换一张\" onclick=\"Func_changeCaptcha()\">");
        captchaImg2.append("<ul class=\"list-unstyled\">\n" +
                           "<a href=\"javascript:void(0)\" onclick=\"Func_changeCaptcha()\" class=\"text-muted\">看不清，换一张</a>\n" +
                           "</ul>");
    });
    return false;
}

function Func_changeCaptcha(){
    $.ajax("/getCaptcha/", {
        dataType: 'json',
        type: 'POST',
        data: {}
    }).done(function(data) {
        var captchaImg1 = $("#captchaImg1");
        captchaImg1.children().remove();
        captchaImg1.append("<img src=\"" + data.sign_in_captcha_url +"\" title=\"看不清？换一张\" onclick=\"Func_changeCaptcha()\">");
        captchaImg1.append("<ul class=\"list-unstyled\">\n" +
                           "<a href=\"javascript:void(0)\" onclick=\"Func_changeCaptcha()\" class=\"text-muted\">看不清，换一张</a>\n" +
                           "</ul>");
        var captchaImg3 = $("#captchaImg3");
        captchaImg3.children().remove();
        captchaImg3.append("<img src=\"" + data.resetPWD_captcha_url +"\" title=\"看不清？换一张\" onclick=\"Func_changeCaptcha()\">");
        captchaImg3.append("<ul class=\"list-unstyled\">\n" +
                           "<a href=\"javascript:void(0)\" onclick=\"Func_changeCaptcha()\" class=\"text-muted\">看不清，换一张</a>\n" +
                           "</ul>");
        var captchaImg2 = $("#captchaImg2");
        captchaImg2.children().remove();
        captchaImg2.append("<img src=\"" + data.sign_up_captcha_url +"\" title=\"看不清？换一张\" onclick=\"Func_changeCaptcha()\">");
        captchaImg2.append("<ul class=\"list-unstyled\">\n" +
                           "<a href=\"javascript:void(0)\" onclick=\"Func_changeCaptcha()\" class=\"text-muted\">看不清，换一张</a>\n" +
                           "</ul>");
    });
    return false;
}

function validateResetPwd() {
    $("#formResetPWD").validate({
        submitHandler: function() {
            Func_send_resetPWD_email();
        },
        rules: {
            inputEmail: {
                required: true,
                email: true
            }
        },
        messages: {
            inputEmail: "请输入正确的邮箱地址",
        }
    })
}

function Func_send_resetPWD_email() {
    $.ajax("/send_resetPWD_email/", {
        dataType: 'json',
        type: 'POST',
        async : false,
        data: {
            "email": $("#inputResetEmail").val(),
            "captcha": $("#inputCaptchaResetPWD").val(),
        }
    }).done(function (data) {
        if (data.statCode != 0) {
            alert(data.errormessage);
            location.replace(location);
        } else{
            alert('重置密码邮件已发送至您的邮箱，请在10分钟内查收');
            location.replace(location);
        }
    });
}

function Func_get_mail_num() {
    $.ajax("/getMailNum/",{
        dataType: 'json',
        type: 'POST',
        async : false,
    }).done(function (data) {
        if(data.mail_num != -1){
            var mail_num = document.getElementById("unreadMailMessageNum");
            if(data.mail_num == 0){
                mail_num.innerText = "";
            } else{
                mail_num.innerText = data.mail_num;
            }
        }
    });
}