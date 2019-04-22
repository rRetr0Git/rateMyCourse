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
        minlength: "用户名必须由至少2个字符组成"
      },
      password: {
        required: "请输入密码",
        minlength: "密码长度不能小于5个字符"
      }
    }
  })
}

function generateGrid(imageUrls, userName, text, time) {
    var ScreenGridHtml =
        `
        <div>
            <div>
                <div>
                    <div>
                        <img>
                    </div>
                    <div>
                        <p></p>
                    </div>
                    <div>
                        <p></p>
                    </div>
                    <div>
<!--                        <button></button>-->
                    </div>
                    <div>
<!--                        <button></button>-->
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div>
                <div>
                    <div>
                        <p>cc</p>
                    </div>
                </div>
            </div>
        </div>
        `

    // create div
    var commentGrid = document.createElement("div");
    commentGrid.id = "commentGrid";
    commentGrid.setAttribute("class","list-group-item");
    commentGrid.innerHTML = ScreenGridHtml;

    var divTags = commentGrid.getElementsByTagName("div");
    var pTags = commentGrid.getElementsByTagName("p");

    divTags[0].setAttribute("class","list-group-item");
    divTags[1].setAttribute("class","col-md-12 column");
    divTags[2].setAttribute("class","row clearfix");

    // insert picture
    divTags[3].setAttribute("class","col-md-2 column");
    var imageTag = commentGrid.getElementsByTagName("img");
    imageTag[0].src = imageUrls;
    imageTag[0].width = "35";
    imageTag[0].height = "35";

    // insert user name
    divTags[4].setAttribute("class","col-md-4 column");
    var userNameNode = document.createTextNode(userName);
    pTags[0].appendChild(userNameNode);

    // insert time
    divTags[5].setAttribute("class","col-md-2 column")
    var timenode = document.createTextNode(time);
    pTags[1].appendChild(timenode);

    var buttonTag = commentGrid.getElementsByTagName("button");
    // insert vote-up
    divTags[6].setAttribute("class","col-md-2 column")
    // buttonTag[0].type = "button";
    // buttonTag[0].setAttribute("class","btn btn-sm btn-success");
    // buttonTag[0].innerHTML = "👍";

    // insert vote-down
    divTags[7].setAttribute("class","col-md-2 column")
    // buttonTag[1].type = "button";
    // buttonTag[1].setAttribute("class","btn btn-sm btn-danger");
    // buttonTag[1].innerHTML = "👎";

    divTags[8].setAttribute("class","list-group-item");
    divTags[9].setAttribute("class","col-md-12 column");
    divTags[10].setAttribute("class","row clearfix");

    // insert comment
    divTags[11].setAttribute("class","col-md-12 column")
    pTags[2].innerHTML = text;
    pTags[2].setAttribute("class", "center-vertical")

    return commentGrid;
}

function setComments() {//get comments list from service
    $.ajax('/getComment/', {
        dataType: "json",
        data: {'courseTeacherId': window.location.pathname.split('/')[2]},
    }).done(function(data){
        var parents = document.getElementById("commentDiv");
        var comment = document.getElementById("commentGrid");
        if (comment) {
            parents.removeChild(comment);
        }
        for(var i=0; i<data.comments.length; i++){
            //generate a new row
            var cmt = data.comments[i];
            var Grid = generateGrid(cmt.avator, cmt.userName, cmt.text, cmt.time);
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
    //$("#menuLogin").load("test.html")
    validateSignUp()
    validateSignIn()

    // Login widget set according to cookie
    if ($.cookie('username') == undefined) {
        $("#menuUser").prop("hidden",true)
        $("#menuLogin").prop("hidden",false)
        // $("#menuUser").hide()
        // $("#menuLogin").show()
    }
    else {
        $("#menuUser").prop("hidden",false)
        $("#menuLogin").prop("hidden",true)
        // $("#menuLogin").hide()
        // $("#menuUser").show()
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
  $.removeCookie('username', {path: '/'})
  return false
}
