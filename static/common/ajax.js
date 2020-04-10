var ajax = {
    'get':function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post':function (args) {
        args['method'] = 'post';
        this.ajax(args);
    },
    'ajax':function (args) {  // 将头部信息放到请求
        this._ajaxSetup();
        $.ajax(args);
    },
    '_ajaxSetup':function(){  // 将csrftoken放到头部信息
        // 无论何时发送ajax post请求，都为其添加X-CSRFToken头
        $.ajaxSetup({
           'beforeSend': function (xhr, settings) {
               if(!/^(GET|HEAD|OPTIPNS|TRACE)$/i.test(settings.type) && !this.crossDomain){
                   // 先从meta中获取csrf_token标签
                   var csrf_token = $('meta[name=csrf_token]').attr('content');  // 获取csrf_token
                   // 将csrf_token发送给服务器
                   xhr.setRequestHeader('X-CSRFToken', csrf_token)
               }
           }
       });
    }
};