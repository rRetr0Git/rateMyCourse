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

function generateGrid(imageUrls, userName, text, time) {
    var ScreenGridHtml =
        `
        <div>
            <div>
                <div>
                    <img>
                    <p>
                </div>
                <div>
                    <p>
                </div>
                <div>
                </div>
            </div>
            <div>
                <div>
                    <div>
                        <p>
                        </p>
                    </div>
                    <div>
                    </div>
                    <div>
                        <button>
                        </button>
                    </div>
                    <div>
                        <button>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        `;

        // create div
        var commentGrid = document.createElement("div");
        commentGrid.id = "commentGrid";
        commentGrid.setAttribute("class","list-group-item");
        commentGrid.innerHTML = ScreenGridHtml;
        //insert user image and name
        var imageTag = commentGrid.getElementsByTagName("img");
        imageTag[0].src = "http://wx2.sinaimg.cn/large/0076t302ly1fylgfkon55j30e80e8ab5.jpg";
        imageTag[0].width = "50";
        imageTag[0].height = "50";
        //imageTag[0].setAttribute("style", "margin-bottom:16px;margin-top:16px");

        var pTags = commentGrid.getElementsByTagName("p");
        var userNameNode = document.createTextNode(userName);
        pTags[0].appendChild(userNameNode);
        //pTags[0].setAttribute("class", "userName");

        //insert text
        pTags[1].innerHTML = text;
        pTags[1].setAttribute("class", "center-vertical")
        //inset time
        var timenode = document.createTextNode(time);
        pTags[2].appendChild(timenode);
        //pTags[2].setAttribute("style", "width:100%;text-align:right;margin-top:32px")
        var buttonTag = commentGrid.getElementsByTagName("button");
        buttonTag[0].type = "button";
        buttonTag[0].setAttribute("class","btn btn-sm btn-success");
        buttonTag[0].innerHTML = "👍";
        buttonTag[1].type = "button";
        buttonTag[1].setAttribute("class","btn btn-sm btn-danger");
        buttonTag[1].innerHTML = "👎";
        //css
        var divTags = commentGrid.getElementsByTagName("div");
        divTags[0].setAttribute("class", "col-md-12 column");
        divTags[1].setAttribute("class", "row clearfix");
        divTags[2].setAttribute("class", "col-md-1 column");
        divTags[3].setAttribute("class", "col-md-7 column");
        divTags[4].setAttribute("class", "col-md-4 column");
        divTags[5].setAttribute("class", "col-md-12 column");
        divTags[6].setAttribute("class", "row clearfix");
        divTags[7].setAttribute("class", "col-md-2 column");
        divTags[8].setAttribute("class", "col-md-6 column");
        divTags[9].setAttribute("class", "col-md-2 column");
        divTags[10].setAttribute("class", "col-md-2 column");
        return commentGrid;
}

function setComments() {//get comments list from service
    $.ajax('/getComment/', {
        dataType: "json",
        data: {'courseTeacherId': window.location.pathname.split('/')[2]},
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
            var Grid = generateGrid(imgurl, cmt.userName, cmt.text, cmt.time);
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
