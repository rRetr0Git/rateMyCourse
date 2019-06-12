function htmlEscape(text){
  return text.replace(/[<>"&]/g, function(match, pos, originalText){
    switch(match){
    case "<": return "&lt;";
    case ">":return "&gt;";
    case "&":return "&amp;";
    case "\"":return "&quot;";
  }
  });
}

function Func_addLike(commentId){
    $.ajax("/addLike/", {
        dataType: 'json',
        type: 'POST',
        async : false,
        data: {
          "commentId": commentId
        }
    });
    document.getElementById("goodTime"+commentId).innerHTML=parseInt(document.getElementById("goodTime"+commentId).innerHTML)+1;
    return false;
}

function Func_addDislike(commentId){
    $.ajax("/addDislike/", {
        dataType: 'json',
        type: 'POST',
        async : false,
        data: {
          "commentId": commentId
        }
    });
    document.getElementById("badTime"+commentId).innerHTML=parseInt(document.getElementById("badTime"+commentId).innerHTML)+1;
    return false;
}

function fixBr(text){
    return text.replace(RegExp("&lt;br&gt;", "g"),"<br>");
}


function generateGrid(imageUrls, userName, userid, text, time, goodTimes, badTimes, commentId, scores) {
    var ScreenGridHtml =
        `
        <div>
            <div>
                <div>
                    <div>
                        <img>
                    </div>
                    <div>
                        <a></a>
                    </div>
                    <div>
                        <p></p>
                    </div>
                    <div>
                        <p></p>
                    </div>
                    <div>
                        <button></button>
                    </div>
                    <div>
                        <p></p>
                    </div>
                    <div>
                        <button></button>
                    </div>
                    <div>
                        <p></p>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div>
                <div>
                    <div>
                        <p></p>
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
    var aTags = commentGrid.getElementsByTagName("a");

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
    divTags[4].setAttribute("class","col-md-2 column");
    var userNameNode = document.createTextNode(userName);
    aTags[0].appendChild(userNameNode);
    if (userid !== '') {
        aTags[0].setAttribute('href', '/userInfo/?name=' + userName);
    }

    // insert time
    divTags[5].setAttribute("class","col-md-2 column")
    var timenode = document.createTextNode(time);
    pTags[0].appendChild(timenode);

    // insert scores
    divTags[6].setAttribute("class","col-md-2 column")
    var scoresnode = document.createTextNode('[' + scores.homework.toString() + ',' + scores.difficulty.toString() + ',' + scores.knowledge.toString() + ',' + scores.satisfaction.toString() + ']');
    pTags[1].appendChild(scoresnode);

    var buttonTag = commentGrid.getElementsByTagName("button");
    // insert vote-up
    divTags[7].setAttribute("class","col-md-1 column")
    buttonTag[0].type = "button";
    buttonTag[0].setAttribute("class","btn btn-sm btn-success");
    buttonTag[0].setAttribute("onclick", "this.disabled=true;Func_addLike('"+commentId+"')");
    buttonTag[0].innerHTML = "👍";
    divTags[8].setAttribute("class","col-md-1 column")
    pTags[2].setAttribute("id","goodTime"+commentId+"");
    pTags[2].appendChild(document.createTextNode(goodTimes));

    // insert vote-down
    divTags[9].setAttribute("class","col-md-1 column")
    buttonTag[1].type = "button";
    buttonTag[1].setAttribute("class","btn btn-sm btn-danger");
    buttonTag[1].setAttribute("onclick", "this.disabled=true;Func_addDislike('"+commentId+"')");
    buttonTag[1].innerHTML = "👎";
    divTags[10].setAttribute("class","col-md-1 column")
    var badnode = document.createTextNode(badTimes);
    pTags[3].setAttribute("id","badTime"+commentId+"");
    pTags[3].appendChild(badnode);
    divTags[11].setAttribute("class","list-group-item");
    divTags[12].setAttribute("class","col-md-12 column");
    divTags[13].setAttribute("class","row clearfix");

    // insert comment
    divTags[14].setAttribute("class","col-md-12 column")
    pTags[4].innerHTML = fixBr(htmlEscape(text));
    pTags[4].setAttribute("style","word-wrap:break-word")
    pTags[4].setAttribute("class", "text-left")

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
            var Grid = generateGrid(cmt.avator, cmt.userName, cmt.userid, cmt.text, cmt.time, cmt.goodTimes, cmt.badTimes, cmt.commentId, cmt.scores);
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
    validateResetPwd()

    // Login widget set according to cookie
    // if ($.cookie('username') == undefined || $.cookie('userid') == undefined) {
    //     $("#menuUser").prop("hidden",true)
    //     $("#menuLogin").prop("hidden",false)
    //     // $("#menuUser").hide()
    //     // $("#menuLogin").show()
    // }
    // else {
    //     $("#menuUser").prop("hidden",false)
    //     $("#menuLogin").prop("hidden",true)
    //     // $("#menuLogin").hide()
    //     // $("#menuUser").show()
    //     $("#navUser").text($.cookie('username'))
    // }
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
