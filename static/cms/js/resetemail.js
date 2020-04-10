$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        console.log(email);
        if (!email) {
            dmtalert.alertInfoToast('请输入邮箱');
            return;
        }
        // 通过ajax形式发送消息获取验证码
        ajax.get({
            'url':'/cms/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    dmtalert.alertSuccessToast('邮件发送成功！请注意查收！');
                }else{
                    dmtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
            dmtalert.alertNetworkError();
        }
        });
    });
});

$(function () {
    $("#submit").click(function (event) {
        //组织默认提交形式
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        ajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if(data['code'] == 200){
                    emailE.val("");
                    captchaE.val("");
                    dmtalert.alertSuccessToast('恭喜！邮箱修改成功！');
                }else{
                    dmtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                dmtalert.alertNetworkError();
            }
        })
    })
})