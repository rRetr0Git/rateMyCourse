$(function(){
  $(":radio").click(function(){
      if($(this).val()=="option1"){
        $("#top_courses").show()
        $("#top_teachers").hide()
      }
      else{
        $("#top_teachers").show()
        $("#top_courses").hide()
      }
  });
 });

$(document).ready(function() {
  // alert("!!!")
  // Form validation for Sign in / Sign up forms
  //$("#menuLogin").load("./test.html")
  validateSignUp()
  validateSignIn()
    validateResetPwd()

  // Login widget set according to cookie
  // if($.cookie('userid') == undefined || $.cookie('username') == undefined) {
  //     $("#menuUser").prop("hidden",true)
  //     $("#menuLogin").prop("hidden",false)
  //   // $("#menuUser").hide()
  //   // $("#menuLogin").show()
  // }
  // else{
  //     $("#menuUser").prop("hidden",false)
  //     $("#menuLogin").prop("hidden",true)
  //   // $("#menuLogin").hide()
  //   // $("#menuUser").show()
  //   $("#navUser").text($.cookie('username'))
  // }
  $("#top_courses").show()
  $("#top_teachers").hide()

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


function generateCompareTRs(iCol, sDataType) {
     return   function  compareTRs(oTR1, oTR2) {
        vValue1 = convert(oTR1.cells[iCol].firstChild.nodeValue, sDataType);
        vValue2 = convert(oTR2.cells[iCol].firstChild.nodeValue, sDataType);
         if (vValue1 < vValue2) {
             return  -1;
        } else if(vValue1 > vValue2) {
             return  1;
        } else{
             return  0;
        }
    };
}

function convert(sValue, sDataType) {
     switch (sDataType) {
     case "int" :
         return parseInt(sValue);
     case "float" :
         return parseFloat(sValue);
     case "date" :
         return new Date(Date.parse(sValue));
     default:
         return sValue.toString();
    }
}

function sortTable(sTableID, iCol, sDataType) {
     var oTable = document.getElementById(sTableID);
     var oTBody = oTable.tBodies[0];
     var colDataRows = oTBody.rows;
     var aTRs =  new Array;
     for (var i = 0; i < colDataRows.length; i++) {
        aTRs[i] = colDataRows[i];
    }
     if  (oTable.sortCol == iCol) {
        aTRs.reverse();
    } else {
        aTRs.sort(generateCompareTRs(iCol, sDataType));
    }
     var oFragment = document.createDocumentFragment();
     for(var j = 0; j < aTRs.length; j++) {
        oFragment.appendChild(aTRs[j]);
    }
    oTBody.appendChild(oFragment);
    oTable.sortCol = iCol;
}

