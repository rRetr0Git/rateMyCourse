$(document).ready(function() {

    validateSignUp()
    validateSignIn()
    validateResetPwd()

})

function Func_adminDeleteComment(commentId){
    console.log(commentId)
  $.ajax("/adminDeleteComment/", {
    dataType: 'json',
    type: 'POST',
    data: {
      'comment': commentId
    }
  }).done(function (data) {
    if(data.statCode == 0){
      alert("删除成功！");
      location.replace(location);
    }
    else {
      alert(data.errormessage);
    }
  })
}