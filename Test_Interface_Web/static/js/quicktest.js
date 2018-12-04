/**
 * 初始化加载
 */
$(document).ready(function () {
    var MaxInputs = 50; //最大文本框数
    var HeaderWrapper = $('#interface_headers');//header输入框包装ID
    var HeaderAddButton = $("#headerAddMoreFileBox"); //header添加按钮ID
    var InputsWrapper = $("#InputsWrapper"); //输入框包装ID
    var AddButton = $("#AddMoreFileBox"); //添加按钮ID
    var x = InputsWrapper.length; //文本框数
    var y = HeaderWrapper.length; //文本框数
    var HeaderFieldCount = 2;//header初始化
    var FieldCount = 1; //初始化

    /*
    $(AddButton).click(function (e) //添加事件
    {
        if (x <= MaxInputs) //允许输入最大框
        {
            FieldCount++; //添加增量的文本框
            // 添加文本框CSS样式
            $(InputsWrapper).append('<li class="input-group" style="width: 100%;padding-top: 10px">' +
                '<input type="text" class="form-control" placeholder="请输入参数名" rel="external nofollow" id="field_'
                + FieldCount + '" style="width:30%;"/>' +
                '<select id="check_' + FieldCount + '" class="btn btn-default dropdown-toggle" style="float: left;margin:0 5px 0 5px;">' +
                '<option value="1">=</option>' +
                '<option value="2"><></option>' +
                '<option value="3">包含</option>' +
                '<option value="4">不包含</option></select>' +
                '<input type="text" class="form-control" placeholder="请输入检查值" id="field_value_'
                + FieldCount + '" style="width:41%; float:left"/>' +
                '<span class="removeclass input-group-btn" rel="external nofollow" style="width: 30px;float:left">' +
                '<button class="btn btn-default" type="button" rel="external nofollow">-</button>' +
                '</span></li>');
            x++; //增加文本框
        }
        return false;
    });*/

    $(HeaderAddButton).click(function (e) //添加事件
    {
        if (y <= MaxInputs) //允许输入最大框
        {
            HeaderFieldCount++; //添加增量的文本框
            // 添加文本框CSS样式
            $(HeaderWrapper).append('<li class="input-group" style="width: 100%;padding-top: 10px">' +
                '<input type="text" class="form-control" placeholder="请输入请求头" rel="external nofollow" ' +
                'id="header_field_' + HeaderFieldCount + '" style="width:30%;"/>' +
                '<select class="btn btn-default dropdown-toggle" id="check_header">' +
                '<option value="1" selected>=</option></select>' +
                '<input type="text" class="form-control" placeholder="请输入值" id="header_value_' +
                HeaderFieldCount + '" style="width:47%; float:left"/>' +
                '<span class="removeclass input-group-btn" rel="external nofollow" style="width: 30px;float:left">' +
                '<button class="btn btn-default" type="button" rel="external nofollow">-</button>' +
                '</span></li>');
            y++; //增加文本框
        }
        return false;
    });
    $("body").on("click", ".removeclass", function (e) { //移除文本框事件
        if (x > 1) {
            $(this).parent('li').remove(); //移除文本框CSS
            x--; //减少文本框
        }
        if (y > 1) {
            $(this).parent('li').remove(); //移除文本框CSS
            y--; //减少文本框
        }
        return false;
    });
    $("[data-toggle='popover']").popover('hide');
//点击保存按钮模态框操作
    $("#saveBTN").unbind('click').bind('click', function () {
        //模态框数值初始化为页面值
        $("#type").val($('#interface_type').val())
        $("#url_id").val($('#interface_url').val())
        $("#defaultpar").val($('#param_info').val())

        $('#update_Modle').modal('show')
        //动态获取模块的值
        $("#pname").change(function () {
            $("#mname").children().remove()
            var pnumber = $("#pname").find("option:selected").val() //获取项目选中的值
            //请求模块接口
            $.getJSON(
                "/interface/search/?pnumber=" + pnumber,
                function (data) {
                    var msg = data.msg
                    // console.log(msg)
                    var options = '';
                    for (var i in msg) {
                        options += "<option  value='" + msg[i].mnumber + "' > " + msg[i].modelname + "</option>";
                        // console.log(msg[i].modelname);
                    }
                    $("#mname").html(options)
                });
        })
    });
    <!-- 动态获取项目模块 -->
    $("#pro_status").change(function (e) {
        getprojectinfo("#pro_status", "#pro_model", 2);
    });
    <!-- 模态框确认按钮点击保存接口数据 -->
    $("#oks_id").unbind('click').bind('click', function () {
        var id = null

        submit_page();
        $('#update_Modle').modal('hide');
    })
    //初始化模态框数据
    $('#update_Modle').on('hidden.bs.modal', function () {
        $("#pname").val("--请选择--")
        $("#mname").val("--请选择--")
        $('#templateName').val("")
        $("#interfacename").val("")
        $("#url_id").val("")
        $("#defaultpar").val("")
        $("#type").val("")
        $("#remark").val("")
        $("#interface_id").val("")
    });
//执行接口
    $(submitBTN).click(function () {
        var interface_url = jQuery.trim($("#interface_url").val());
        var param_info = jQuery.trim($("#param_info").val());
        var interface_method = jQuery.trim($("#interface_type").val())
        // var request_data_type=jQuery.trim($("#interface_data_type").val())
        var contentType = jQuery.trim($("#header_value_01").val())
        var checkequal = jQuery.trim($("#checkequal").val());
        var checknotequal=jQuery.trim($("#checknotequal").val());

        if (contentType == 1)
            contentType = "application/x-www-form-urlencoded"
        else
            contentType = "application/json"
        var headers = "{" + "\"Content-Type\":\"" + contentType + "\""
        for (var i = 1; i <= HeaderFieldCount; i++) {
            var header_name = jQuery.trim($("#header_field_" + i + "").val());
            var header_value = jQuery.trim($("#header_value_" + i + "").val());

            if (header_name != undefined && header_name != "") {
                console.log('刚进入' + i)
                if (header_name.length > 0) {
                    // console.log(i)
                    headers = headers + ',"' + header_name + '"' + ":" + '"' + header_value + '"'
                }
            }
            // console.log(headers)
        }
        headers = headers + "}"
// console.log(headers)
        if (interface_url.length == 0) {
            tishi("#submitBTN", "请输入接口URL！", 0);
            window.setTimeout("$('#submitBTN').popover('destroy');", 3000);
        }
        else if (param_info.length == 0 && interface_method == 1) {
            tishi("#submitBTN", "请输入接口参数！", 0);
            window.setTimeout("$('#submitBTN').popover('destroy');", 3000);
        }
        else {
            var json_result = $("#json_result");
            var check_body = $("#check_body");
            $.ajax({
                type: "POST",
                url: "/interface/run/",
                data: {
                    btype: 1,
                    headers: headers,
                    // request_data_type:request_data_type,
                    interface_url: interface_url,
                    interface_method: interface_method,
                    param: param_info,
                    checkequal:checkequal,
                    checknotequal:checknotequal
                },
                dataType: "json",
                timeout: 15000,
                beforeSend: function (XMLHttpRequest) {
                    json_result.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
                    check_body.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
                },
                success: function (data) {
                    var resulttype = data.resulttype;
                    if (resulttype == 200) {
                        var msg_info = JSON.parse(data.msg);
                        json_result.empty();
                        json_result.append(APP.format(msg_info));

                        //检查点
                        check_body.empty();
                        var checkequal_info=data.checkequal_info;
                        var checknotequal_info=data.checknotequal_info;

                        //加载等于检查点
                        if(checkequal_info.length>0)
                        {
                            for(var i = 0, l = checkequal_info.length; i < l; i++)
                            {
                                check_body.append(checkequal_info[i]);
                            }
                        }

                         //加载等于检查点
                        if(checknotequal_info.length>0)
                        {
                            for(var j = 0, k = checknotequal_info.length; j <k; j++)
                            {
                                check_body.append(checknotequal_info[j]);
                            }
                        }

                        /*
                        //检查点
                        check_body.empty();
                        var str_info = data.msg;
                        re = new RegExp(null, "g"); //定义正则表达式
                        str_info = str_info.replace(re, '"null"');
                        var msginfo = JSON.parse(str_info);
                        //获取检查点
                        for (var i = 1; i <= FieldCount; i++) {
                            var param_name = jQuery.trim($("#field_" + i + "").val());
                            var param_value = jQuery.trim($("#field_value_" + i + "").val());
                            var param_type = $("#check_" + i + "").find("option:selected").val();
                            if (param_name != undefined && param_name != "") {
                                if (param_type == "1") {
                                    if (param_name.length > 0) {
                                        recursionJSON(msginfo, param_name, param_value, 1);
                                    }
                                }
                                else if (param_type == "2") {
                                    if (param_name.length > 0) {
                                        recursionJSON(msginfo, param_name, param_value, 2);
                                    }
                                }
                                else if (param_type == "3") {
                                    if (param_name.length > 0) {
                                        recursionJSON(msginfo, param_name, param_value, 3);
                                    }
                                }
                                else if (param_type == "4") {
                                    if (param_name.length > 0) {
                                        recursionJSON(msginfo, param_name, param_value, 4);
                                    }
                                }
                            }
                        }*/
                    }
                    else {
                        json_result.empty();
                        check_body.empty();
                        json_result.append(data.msg);
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    if (textStatus == 'error') {
                        json_result.empty();
                        check_body.empty();
                        json_result.append(errorThrown);
                    }
                }
            });
        }
    });
})
//迭代解析json
    function recursionJSON(data, name, value, type) {
        if (typeof(data) == "object") {
            $.each(data, function (i, n) {
                if (typeof(n) == "object") {
                    recursionJSON(n, name, value, type)
                } else {
                    if (i == name && type == "1") {
                        if (n == value)
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "==" + value + "</td>" +
                                "<td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                        else
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "==" + value + "</td>" +
                                "<td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                    }
                    if (i == name && type == "2") {
                        if (n != value)
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "<>" + value + "</td>" +
                                "<td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                        else
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "<>" + value + "</td>" +
                                "<td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                    }
                    if (i == name && type == "3") {
                        if (n.indexOf(value) > -1)
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "包含" + value + "</td>" +
                                "<td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                        else
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "包含" + value + "</td>" +
                                "<td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                    }
                    if (i == name && type == "4") {
                        if (n.indexOf(value) == -1)
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "不包含" + value + "</td>" +
                                "<td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                        else
                            $("#check_body").append("<tr><td>" + i + ":" + n + "</td>" +
                                "<td>" + name + "不包含" + value + "</td><" +
                                "td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                    }
                }
            })
        }
    }

//提示语公共方法
function tishi(name, info, type) {
    if (type == 0) {
        $(name).attr("data-content", "<span class='glyphicon glyphicon-question-sign' style='color: rgb(255, 0, 0);'>" + info + "</span>");
        $(name).popover('show');
    }
    else {
        $(name).attr("data-content", "<span class='glyphicon glyphicon-ok-sign' style='color: rgb(0, 162, 65);'>" + info + "</span>");
        $(name).popover('show');
    }
}