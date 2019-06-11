var jQuery = $(document).ready(function() {
  //alert("!!!")
  //$("#navbarContainer").load("./components/indexNavbarContainer.html")

  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()
  validateResetPwd()

  // Login widget set according to cookie
  // if($.cookie('username') == undefined || $.cookie('userid') == undefined) {
  //     $("#menuUser").prop("hidden",true)
  //     $("#menuLogin").prop("hidden",false)
  //   //$("#menuUser").hide()
  //   //$("#menuLogin").show()
  // }
  // else{
  //     $("#menuUser").prop("hidden",false)
  //     $("#menuLogin").prop("hidden",true)
  //   //$("#menuLogin").hide()
  //   //$("#menuUser").show()
  //   $("#navUser").text($.cookie('username'))
  // }
})

$(function(){
    initCropperInModal($('#photo'),$('#photoInput'),$('#changeModal'));
});
//进行模态框的初始化
var initCropperInModal = function(img, input, modal){
    var $image = img;
    var $inputImage = input;
    var $modal = modal;
    var options = {
        aspectRatio: 1, // 纵横比，头像采用1:1
        viewMode: 2, //cropper的视图模式
        preview: '.img-preview' // 预览图的class名
    };
    // 模态框隐藏后需要保存的数据对象
    var saveData = {};
    var URL = window.URL || window.webkitURL;
    var blobURL;
    $modal.on('shown.bs.modal', function () {
        // 重新创建
        $image.cropper(
            $.extend(options, {
                ready: function () {
                    // 当剪切界面就绪后，恢复数据
                    if(saveData.canvasData){
                        $image.cropper('setCanvasData', saveData.canvasData);
                        $image.cropper('setCropBoxData', saveData.cropBoxData);
                    }
                }
            }
        ));
    }).on('hidden.bs.modal', function () {
        // 保存相关数据
        saveData.cropBoxData = $image.cropper('getCropBoxData');
        saveData.canvasData = $image.cropper('getCanvasData');
        // 销毁并将图片保存在img标签
        $image.cropper('destroy').attr('src',blobURL);
    });
    if (URL) {
        //检测用户上传了图片，将图片显示到裁剪框中，然后处理相关的内容，如预览图和提示语句
        $inputImage.change(function() {
            var files = this.files;
            var file;
            if (!$image.data('cropper')) {
                return;
            }
            if (files && files.length) {
                file = files[0];
                //验证文件是否为图片文件
                if (/^image\/\w+$/.test(file.type)) {
                    if(blobURL) {
                        URL.revokeObjectURL(blobURL);
                    }
                    blobURL = URL.createObjectURL(file);
                    // 重置cropper，将图像替换
                        $image.cropper('reset').cropper('replace', blobURL);
                    // 选择文件后，显示和隐藏相关内容
                    //bootstrap4取消了.hidden，因此采用JQ的show()和hide()来实现，等同于css中的display属性
                    $('.img-container').show();
                    $('.img-preview-box').show();
                    $('#changeModal .disabled').removeAttr('disabled').removeClass('disabled');
                    $('#changeModal .tip-info').hide();
                } else {
                    window.alert('请选择一个图像文件！');
                }
            }
        });
    } else {
        //没有上传头像时是无法提交的
        $inputImage.prop('disabled', true).addClass('disabled');
    }
}

var sendPhoto = function(){
    //获取到图片的内容，采用toBlob()生成Blob对象，再将Blob对象添加到formData对象中去，最终实现上传，也可以采用toDataURL()来获取BASE64对象，如果服务器支持BASE64的话
    var photo = $('#photo').cropper('getCroppedCanvas', {
        width: 300,
        height: 300
    }).toBlob(function (blob) {
        formData=new FormData();
        formData.append('smfile',blob);
        $.ajax({
            type:"POST",
            url:"/saveUserPic/",
            data:formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                alert("修改成功！");
                location.replace(location);
            },
            error: function (data) {
                alert("修改失败！");
                location.replace(location);
            }
        });
    });
}

function Func_userDeleteComment(commentId){
  $.ajax("/userDeleteComment/", {
    dataType: 'json',
    type: 'POST',
    data: {
      'commentId': commentId
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