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