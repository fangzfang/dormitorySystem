// 所有页面加载后才执行这个代码
$(function () {
    //获取按钮
    $("#submit").click(function (event) {
        //是为了阻止按钮默认的提交表单的行为
        event.preventDefault();
         // 获取三个输入框中的值,必须在点击按钮后才会执行
        //先获取三个输入框中的标签
        var oldpwdE = $("input[name='oldpwd']")
        var newpwdE = $("input[name='newpwd']")
        var newpwd2E = $("input[name='newpwd2']")

        //根据标签获取相应的值
        var oldpwd = oldpwdE.val()
        var newpwd = newpwdE.val()
        var newpwd2 = newpwd2E.val()

        //将数据发送给服务器
        // ajax与csfx配合使用

        //1、在模版的meta标签中渲染一个csrf-token
        //2、在ajax请求的头部中设置X-CSRFtoken
        ajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd':oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2,
            },
            //回调函数
            'success': function (data) {
                //code: 200   请求成功
                if (data['code'] == 200) {
                    //如果code为200， 用toast提示成功
                    dmtalert.alertSuccessToast("恭喜！密码修改成功！")
                    //修改成后，清空输入框
                    oldpwdE.val("")
                    newpwdE.val("")
                    newpwd2E.val("")
                }else {
                    var message = data['message']
                    dmtalert.alertInfo(message)
                }
            },
            //请求失败，提示网络错误
            'fail': function (error) {
                dmtalert.alertNetworkError();
            }
        })
    });
})