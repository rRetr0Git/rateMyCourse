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

function fixBr(text){
    return text.replace(RegExp("&lt;br&gt;", "g"),"<br>");
}


function generateGrid(imageUrls, userName, userid, text, time) {
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
    divTags[4].setAttribute("class","col-md-4 column");
    var userNameNode = document.createTextNode(userName);
    aTags[0].appendChild(userNameNode);
    if (userid !== '') {
        aTags[0].setAttribute('href', '/userInfo/?name=' + userName);
    }

    // insert time
    divTags[5].setAttribute("class","col-md-2 column")
    var timenode = document.createTextNode(time);
    pTags[0].appendChild(timenode);

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
    pTags[1].innerHTML = fixBr(htmlEscape(text));
    pTags[1].setAttribute("style","word-wrap:break-word")
    pTags[1].setAttribute("class", "center-vertical")

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
            var Grid = generateGrid(cmt.avator, cmt.userName, cmt.userid, cmt.text, cmt.time);
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