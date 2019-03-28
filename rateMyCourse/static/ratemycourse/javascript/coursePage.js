'use strict'
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

function generateGrid(imageUrls, userName, iTerm, iTeacher, iToal, text, time) {
    var ScreenGridHtml = `
        <div>
            <img>
            <p>
        </div>
            <table>
                <tr>
                    <td><p></td>
                    <td><p></td>
                    <td><p></td>
                </tr>
                <tr>
                    <td><p></td>
                    <td><p></td>
                    <td><p></td>
                </tr>
            <table>
        <div>
            <p>
        </div>
        <div>
            <p>
        </div>
        <br/>
        <br/>
        <br/>
        `;

        // create div
        var commentGrid = document.createElement("div");
        commentGrid.id = "commentGrid";
        commentGrid.innerHTML = ScreenGridHtml;
        //insert user image and name
        var imageTag = commentGrid.getElementsByTagName("img");
        imageTag[0].src = imageUrls;
        imageTag[0].width = "86";
        imageTag[0].height = "86";
        imageTag[0].setAttribute("style", "margin-bottom:16px;margin-top:16px");

        var pTags = commentGrid.getElementsByTagName("p");
        var userNameNode = document.createTextNode(userName);
        pTags[0].appendChild(userNameNode);
        pTags[0].setAttribute("class", "userName");

        // insert information
        var term = document.createTextNode("学期");
        var teacher = document.createTextNode("上课老师");
        var total = document.createTextNode("总评");
        var vTerm = document.createTextNode(iTerm);
        var vTeacher = document.createTextNode(iTeacher);
        var vTotal = document.createTextNode(iToal.toFixed(1));
        pTags[1].appendChild(term);
        pTags[2].appendChild(teacher);
        pTags[3].appendChild(total);
        pTags[4].appendChild(vTerm);
        pTags[5].appendChild(vTeacher);
        pTags[6].appendChild(vTotal);

        //insert text
        pTags[7].innerHTML = text;
        pTags[7].setAttribute("style", "margin-top:16px;text-align:left; width:70%")
        //inset time
        var timenode = document.createTextNode(time);
        pTags[8].appendChild(timenode);
        pTags[8].setAttribute("style", "width:100%;text-align:right;margin-top:32px")

        //css
        var divTags = commentGrid.getElementsByTagName("div");
        divTags[0].setAttribute("class", "row text-center");
        divTags[1].setAttribute("class", "row text-center");
        divTags[2].setAttribute("class", "row");
        divTags[0].setAttribute("style", "width:70%;border-bottom:1px #e4e4e4 solid;");
        divTags[2].setAttribute("style", "width:100%;border-bottom:1px #e4e4e4 solid;");
        var tableTag = commentGrid.getElementsByTagName("table");
        tableTag[0].setAttribute("style", "width:70%; margin-top:16px;border-bottom:1px #e4e4e4 solid");
        return commentGrid;
}

function setComments() {//get comments list from service
    $.ajax('/getComment', {
        dataType: 'json',
        data: {'course_number': window.location.pathname.split('/')[2]},
    }).done(function(data){
        var imgurl = "../../static/ratemycourse/images/user.png";
        var parents = document.getElementById("commentDiv");
        var comment = document.getElementById("commentGrid");
        if (comment) {
            parents.removeChild(comment);
        }
        for(var i=0; i<data.comments.length; i++){
            //generate a new row
            var cmt = data.comments[i]
            var Grid = generateGrid(imgurl, cmt.userName, cmt.iTerm, cmt.iTeacher, cmt.iTotal, cmt.text, cmt.time);
            //insert this new row
            parents.appendChild(Grid);
        }
    })
}
//var imgurl = {{userimg_list|safe}};
//var userName = {{userName_list|safe}};
//var iTerm = {{term_list|safe}};
//var iTeacher = {{teacher_list|safe}};
//var iTotal = {{total_list|safe}};
//var text = {{text_list|safe}};
//var time = {{time_list|safe}};

$(document).ready(function () {
    // Form validation for Sign in / Sign up forms
    $("#menuLogin").load("test.html")
    validateSignUp()
    validateSignIn()

    // Login widget set according to cookie
    if ($.cookie('username') == undefined) {
        $("#menuUser").hide()
        $("#menuLogin").show()
    }
    else {
        $("#menuLogin").hide()
        $("#menuUser").show()
        $("#navUser").text($.cookie('username'))
    }
    // $.ajax('/getOverAllRate', {
    // 	dataType: 'json',
    // 	data: {
    // 		'course_number': $('#courseNumber').text()
    // 		 },
    // 	}).done(function (data) {
    //     setScores(data.rate)
    // })
    setComments();
})

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
