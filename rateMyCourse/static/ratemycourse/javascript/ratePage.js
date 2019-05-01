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
