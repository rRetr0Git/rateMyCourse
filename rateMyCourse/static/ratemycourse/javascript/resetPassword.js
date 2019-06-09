$.validator.setDefaults({
    submitHandler: function() {
        Func_resetPWD();
    }
});

$(document).ready(function() {
    $("#passwordform").validate({
        rules: {
            new_pass: {
                required: true,
                minlength: 5
            },
            new_confirm_pass: {
                required: true,
                minlength: 5,
                equalTo: "#new_password"
            }
        },
        messages: {
            new_pass: {
                required: "请输入密码",
                minlength: "密码长度不能小于5个字符"
            },
            new_confirm_pass: {
                required: "请再次输入密码",
                minlength: "密码长度不能小于5个字符",
                equalTo: "密码输入不一致"
            }
        }
    })
});

function Func_resetPWD(){
  $.ajax("/resetPWD/", {
    dataType: 'json',
    type: 'POST',
    async : false,
    data: {
      "password": $("#new_password").val(),
      "reset_code": window.location.pathname.split('/')[2]
    },
  }).done(function (data) {
    if (data.statCode != 0) {
      alert(data.errormessage);
    }else{
      alert('重置密码成功，请登录。');
    }
  });
  var url = window.location.href;
  var index = url.lastIndexOf("\/");
  var str = url.substring(0,index);
  window.location.href = str;
}