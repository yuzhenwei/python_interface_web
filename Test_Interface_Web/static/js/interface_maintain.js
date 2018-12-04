/**
 * 用例集维护JS
 * __author__石龙子
 * edited by zijing 2018-07-19
 */
$(document).ready(function () {
    // //查询公共参数
    function getpublicpar()
    {
    caselistid=$("#templatelist").find("option:selected").val();
    if(caselistid>0) {
        $.ajax({
            type: "POST",
            url: "/testcase/getPublicPar/",
            data: {caselistid: caselistid},
            dataType: "json",

            success: function (data) {
                var msg_info = data.msg;
                $("#partd").html(msg_info);
                $("#public_par").val(msg_info);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                if (textStatus == 'error')
                    alert("公共参数返回错误");
            }
        })
    }
    }

    //动态获取用例集
    $("#templatelist").change(function (e) {
        getpublicpar();
    });


    //保存公共参数
    $("#savepublicpar").click(function (e) {
       public_par=jQuery.trim($("#public_par").val());
       var templateid = $(templatelist).find("option:selected").val();
       if(templateid!=-1) {
           if (public_par.length > 0) {
                 $.ajax({
                    type: "POST",
                    url: "/testcase/updatePublicPar/",
                    data: {caselistid: templateid,public_par:public_par},
                    dataType: "json",

                    success: function (data) {
                        var msg_info = data.msg;
                        userCasesSearchList();
                        getpublicpar();
                        alert("保存成功");
                        $("#addpublicpar").modal('hide');
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                        if (textStatus == 'error')
                            alert("修改公共参数返回错误");
                    }
                })
           }
           else {
               tishi("#savepublicpar", "公共参数不能为空！", 0);
               window.setTimeout("$('#savepublicpar').popover('destroy');", 3000);
           }
       }
       else
       {
           tishi("#savepublicpar", "请选择用例集！", 0);
           window.setTimeout("$('#savepublicpar').popover('destroy');", 3000);
       }
    });

    //检查点
    var MaxInputs = 50; //最大文本框数
    var InputsWrapper = $("#InputsWrapper"); //输入框包装ID
    var AddButton = $("#AddMoreFileBox"); //添加按钮ID
    var x = InputsWrapper.length; //文本框数
    var FieldCount = 1; //初始化

    //添加事件
    $(AddButton).click(function (e){
        if (x <= MaxInputs){ //允许输入最大框
            FieldCount++; //添加增量的文本框
            // 添加文本框CSS样式

            $(InputsWrapper).append('<li class="input-group" style="padding-right:15px;padding-top: 10px;float:left">' +
                '<input type="text" class="form-control" placeholder="请输入参数名" rel="external nofollow" ' +
                'id="field_' + FieldCount + '" style="width:200px;"/>' +
                '<select id="check_' + FieldCount + '" class="btn btn-default dropdown-toggle" ' +
                'style="float: left;margin:0 5px 0 5px; "><option value="1">=</option><option value="2"><></option>' +
                '<option value="3">包含</option><option value="4">不包含</option></select>' +
                '<input type="text" class="form-control" placeholder="请输入检查值" id="field_value_' + FieldCount +
                '" style="width:200px; float:left"/><span class="removeclass input-group-btn" rel="external nofollow" ' +
                'style="width: 30px;float:left"><button class="btn btn-default" type="button">-</button></span></li>');
            x++; //增加文本框
        }
        return false;
    });

    $("body").on("click", ".removeclass", function (e) { //移除文本框事件
        if (x > 1) {
            $(this).parent('li').remove(); //移除文本框CSS
            x--; //减少文本框
        }
        return false;
    });

    //动态获取用例集
    $("#project_id").change(function (e) {
        var val = $("#project_id").find("option:selected").val();
        var mname = "#templatelist";
        if (val == "-1") {
            $(mname).children().remove()
            var option = $("<option>").val("-1").text("---请选择---");
            $(mname).append(option);
        } else {
            $.ajax({
                type: "POST",
                url: "/testcase/testcase_maintain/",
                data: {btype: 1, pro_id: val},
                dataType: "json",

                success: function (data) {

                    var msg_info = data.template_msg;
                    $(mname).empty();
                    for (var i = 0, l = msg_info.length; i < l; i++) {
                        // 实际的应用中，这里的option一般都是用循环生成多个了
                        var option = $("<option>").val(msg_info[i]["id"]).text(msg_info[i]["templatename"]);
                        $(mname).append(option);
                    }
                    getpublicpar();
                },
                error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                    if (textStatus == 'error')
                        alert("Ajax返回出错了");
                }
            })
        }


    });

    //查找后按项目刷新用例列表
    $('#selectuser').on('click', function () {

            userCasesSearchList();
            $("#TableDetail").empty();
            $("#EdidtButton").empty();
        }
    );

    //动态获取项目模块
    $("#pro_status").change(function (e) {
        getprojectinfo("#pro_status", "#pro_model", 2, 1);
    });

    //根据模块查找接口
    $("#searchinfo").click(function (e) {
        var pro_val = $("#pro_status").find("option:selected").val();  //项目编码
        var pro_model_val = $("#pro_model").find("option:selected").val();  //项目编码
        var interface_name = jQuery.trim($("#interface_name").val());
        if (pro_val == "-1") {
            tishi("#searchinfo", "请选择项目！", 0);
            window.setTimeout("$('#searchinfo').popover('destroy');", 3000);
        }
        else {
            var detail_body = $("#interface_body");
            $.ajax({
                type: "POST",
                url: "/testcase/testcase_maintain/",
                data: {
                    btype: 3,
                    pro_status: pro_val,
                    pro_model: pro_model_val,
                    interface_name: interface_name
                },
                dataType: "json",
                timeout: 15000,
                beforeSend: function (XMLHttpRequest) {
                    detail_body.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
                },
                success: function (data) {
                    var msg_info = data.interface_info;
                    detail_body.empty();

                    for (var i = 0, l = msg_info.length; i < l; i++) {
                        //添加接口信息
                        var proname = msg_info[i]["pname"];  //项目名
                        var promodelname = msg_info[i]["mname"];  //模块名称
                        var interfacename = msg_info[i]["interfacename"]; //接口名称
                        var interfaceurl = msg_info[i]["url"];  //接口url
                        var interfacepar = msg_info[i]["defaultpar"];  //默认参数;
                        var interfaceid = msg_info[i]["id"];       //接口id
                        var interfacetype = msg_info[i]["type"];   //获取类型
                        var interface_type = "";
                        switch (interfacetype) {
                            case 0:
                                interface_type = "GET";
                                break;
                            case 1:
                                interface_type = "POST";
                                break;
                        }
                        //let--去掉，改成var zijing--20180720
                        var detail_str = `
<tr>
<td>${interfaceid}</td>
<td>${proname}/${promodelname}</td>
<td>${interfacename}</td>
<td id="url_${interfaceid}" style="word-break:break-all;">${interfaceurl}</td>
<td style="word-break:break-all;">${interfacepar}</td>
<td>${interface_type}</td>
<td><input type="checkbox" name="p_check" val="${interfaceid}"/></td>
</tr>`;

                        detail_body.append(detail_str);

                    }

                },
                error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                    if (textStatus == 'error')
                        detail_body.empty();
                    detail_body.append("Ajax返回出错了");
                }
            })
        }
    });

    //新增用例到用例集，会直接保存进两个表，用例集明细表和用例表，成功无提示，失败有提示
    // edited by zijing-2018-07-18
    $("#add_interface").click(function (e) {
        if($("#templatelist").find("option:selected").val()=="-1"){
            alert("请在主页面选择用例集！")
            $("#addusercase").modal('toggle')
        }else if ($("#interface_body tr").length > 0) {
            var templateid = $("#templatelist").find("option:selected").val();
            $("input[name='p_check']").each(function () {
                if ($(this).is(":checked")) {
                    var id = $(this).attr("val");    //参数ID
                    var interfaceurl=$.trim($("#url_"+id).text())
                    var case_data=$.trim($("#url_"+id).next().text())
                    // console.log(case_data)
                    //添加template明细
                    $.ajax({
                        type: "POST",
                        url: "/testcase/addCaseToSuite/",
                        data: {templateid: templateid, interfaceid: id,interfaceurl:interfaceurl,case_data:case_data},
                        dataType: "json",

                        success: function (data) {
                            if (data.retcode != 0)
                                alert(data.msg);
                        },
                        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                            if (textStatus == 'error')
                                alert("Ajax返回出错了");
                        }
                    })

                }
            });

            // getusercaselist();
            // window.location.reload()
        }
        else {
            tishi("#add_interface", "请选择明细！", 0);
            window.setTimeout("$('#add_interface').popover('destroy');", 3000);
            return 0
        }
        $("#addusercase").modal('toggle')
        //查询用例集明细
        userCasesSearchList()
    });

    //保存参数
    $("#savecase").click(function (e) {

        //获取检查点
        var paramlist1 = '';
        var param_list1 = [];
        var paramlist2 = '';
        var param_list2 = [];
        var paramlist3 = '';
        var param_list3 = [];
        var paramlist4 = '';
        var param_list4 = [];
        for (var i = 1; i <= FieldCount; i++) {
            var param_name = jQuery.trim($("#field_" + i + "").val());
            var param_value = jQuery.trim($("#field_value_" + i + "").val());
            var param_type = $("#check_" + i + "").find("option:selected").val();
            if (param_name != undefined && param_name != "") {
                if (param_type == "1") {
                    if (param_value.length > 0) {
                        paramlist1 = '{"' + param_name + '"' + ':' + '"' + param_value + '"}';
                        param_list1.push(paramlist1);
                    }
                }
                else if (param_type == "2") {
                    if (param_value.length > 0) {
                        paramlist2 = '{"' + param_name + '"' + ':' + '"' + param_value + '"}';
                        param_list2.push(paramlist2);
                    }
                }
                else if (param_type == "3") {
                    if (param_value.length > 0) {
                        paramlist3 = '{"' + param_name + '"' + ':' + '"' + param_value + '"}';
                        param_list3.push(paramlist3);
                    }
                }
                else if (param_type == "4") {
                    if (param_value.length > 0) {
                        paramlist4 = '{"' + param_name + '"' + ':' + '"' + param_value + '"}';
                        param_list4.push(paramlist4);
                    }
                }
            }
        }

        param_json1 = "[" + param_list1 + "]";
        param_json2 = "[" + param_list2 + "]";
        param_json3 = "[" + param_list3 + "]";
        param_json4 = "[" + param_list4 + "]";

        if (param_json1 == "[]") {
            param_json1 = ""
        }
        if (param_json2 == "[]") {
            param_json2 = ""
        }
        if (param_json3 == "[]") {
            param_json3 = ""
        }
        if (param_json4 == "[]") {
            param_json4 = ""
        }

        var casename = jQuery.trim($("#case_name").val());  //用例名称
        var param_info = jQuery.trim($("#param_info").val()); //参数信息
        re = new RegExp("'", "g");
        param_info = param_info.replace(re, '"');
        var isheader = 0;
        var header_info = "";
        if ($("#isheaderok").is(":checked")) {
            isheader = 1;
            header_info = jQuery.trim($("#header_info").val());  //获取头部信息
        }
        var isjoin = 0;
        if ($("#isjoinok").is(":checked")) {
            isjoin = 1;
            //拼接选中列表
            var trList = $("#jonin_text tr").length;
            var pus_detail = [];
            for (var j = 0; j < trList; j++) {
                var case_id = $("input[name='case_id']").eq(j).val();  //用例ID
                var interface_id = $("input[name='interface_id']").eq(j).val();  //接口ID
                var json_par = '"' + $("input[name='json_par']").eq(j).val() + '"';  //关联字段
                var interface_name = '"' + $("input[name='interface_name']").eq(j).val() + '"';  //接口名称
                var case_name = '"' + $("input[name='case_name']").eq(j).val() + '"';  //用例名称
                var t_id = $("input[name='t_id']").eq(j).val();  //用例集ID
                var detailinfo = `
                {
                "templatedetailid":${t_id},
                "caseid":${case_id},
                "casename":${case_name},
                "interfaceid":${interface_id},
                "interfacename":${interface_name},
                "jsonpar":${json_par}
                }`;
                pus_detail.push(detailinfo);
            }
            var joindetail = '[${pus_detail}]';
        }
        var InterfaceID = $("#InterfaceID").val();  //接口ID
        var id = $("#id").val();   //用例集ID


        $.ajax({
            type: "POST",
            url: "/testcase/testcase_maintain/",
            data: {
                btype: 6,
                case_name: casename,
                param_info: param_info,
                interfaceid: InterfaceID,
                isequal: param_json1,
                isnotequal: param_json2,
                iscontain: param_json3,
                isnotcontain: param_json4,
                isheader: isheader,
                headerinfo: header_info,
                isjoin: isjoin,
                templateid: id,
                join_info: joindetail
            },
            dataType: "json",

            success: function (data) {
                var msg_info = data.msg;

                //查询用例集明细
                userCasesSearchList()
                // getusercaselist();
            },
            error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }
        });


    });

    //获取关联用例集信息
    $("#joinsearch").click(function (e) {
        var templateid = $("#templatelist").find("option:selected").val();
        var casename = $("#case_text").val();
        var join_body = $("#join_body");
        $.ajax({
            type: "POST",
            url: "/testcase/testcase_maintain/",
            data: {btype: 8, t_id: templateid, "casename": casename},
            dataType: "json",
            beforeSend: function (XMLHttpRequest) {
                join_body.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
            },
            success: function (data) {
                join_body.empty();

                var msg_info = data.msg;
                for (var i = 0, l = msg_info.length; i < l; i++) {
                    var interfaceid = msg_info[i]["interfaceid__id"];  //接口id
                    var id = msg_info[i]["id"];  //用例集详情id
                    var interfacename = msg_info[i]["interfaceid__interfacename"];  //接口名称
                    var usercasename = msg_info[i]["usercaseid__usercasename"];  //用例名称
                    var usercaseid = msg_info[i]["usercaseid"];  //用例ID
                    //let 改var zijing 20180720
                    var str = `
<tr>
<td><input type="checkbox" val="${id}" name="joincheck"/><input type="hidden" id="interface_id${id}" value="${interfaceid}"/></td>
<td>${interfacename}<input type="hidden" id="interfacename_${id}" value="${interfacename}"/></td>
<td>${usercasename}<input type="hidden" id="usercasename_${id}" value="${usercasename}"/>
<input type="hidden" id="usercaseid${id}" value="${usercaseid}"/>
</td>
</tr>`;

                    join_body.append(str);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }
        })

    });

    //加载选中关联用例
    $("#addjoin").click(function (e) {
        if ($("#join_body tr").length > 0) {
            $("input[name='joincheck']").each(function () {
                if ($(this).is(":checked")) {
                    var id = $(this).attr("val"); //获取ID
                    var interfaceid = $("#interface_id" + id).val();   //接口ID
                    var interfacename = $("#interfacename_" + id).val();    //接口名称
                    var usercasename = $("#usercasename_" + id).val();    //用例名称
                    var usercaseid = $("#usercaseid" + id).val();    //用例ID
                    //let 改var zijing 20180720
                    var join_info = `
<tr id="join_tr${id}">
<td><input type="checkbox" name="del_box"/></td>
<td>${interfacename}<input type="hidden" name="t_id" value="${id}"/>
<input type="hidden" name="interface_id" value="${interfaceid}"/>
<input type="hidden" name="interface_name" value="${interfacename}"/></td>
<td>${usercasename}<input type="hidden" name="case_id" value="${usercaseid}"/>
<input type="hidden" name="case_name" value="${usercasename}"/></td>
<td><input type="text" id="json_${id}" name="json_par" placeholder="多个字段用,分隔"/></td>
</tr>`;
                    if ($('join_tr' + id).length == 0) {
                        $("#jonin_text").append(join_info);
                    }
                }
            })
        }
    });

    //移除选中关联信息
    $("#deljoin").click(function () {
        $("input[name='del_box']:checked").each(function () { // 遍历选中的checkbox
            n = $(this).parents("tr").index();  // 获取checkbox所在行的顺序
            $("#jonin_text").find("tr:eq(" + n + ")").remove();
        });
    });

    //自动读取当前用例集的用例
    $('#case_info').on('shown.bs.modal', function () {
        var templateid = $("#templatelist").find("option:selected").val();
        var join_body = $("#join_body");
        $.ajax({
            type: "POST",
            url: "/testcase/testcase_maintain/",
            data: {btype: 8, t_id: templateid, "casename": ""},
            dataType: "json",
            beforeSend: function (XMLHttpRequest) {
                join_body.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
            },
            success: function (data) {
                join_body.empty();

                var msg_info = data.msg;
                for (var i = 0, l = msg_info.length; i < l; i++) {
                    var interfaceid = msg_info[i]["interfaceid__id"];  //接口id
                    var id = msg_info[i]["id"];  //用例集详情id
                    var interfacename = msg_info[i]["interfaceid__interfacename"];  //接口名称
                    var usercasename = msg_info[i]["usercaseid__usercasename"];  //用例名称
                    var usercaseid = msg_info[i]["usercaseid"];  //用例ID
                    //let 改var zijing 20180720
                    var str = `
<tr>
<td><input type="checkbox" val="${id}" name="joincheck"/>
<input type="hidden" id="interface_id${id}" value="${interfaceid}"/></td>
<td>${interfacename}<input type="hidden" id="interfacename_${id}" value="${interfacename}"/></td>
<td>${usercasename}<input type="hidden" id="usercasename_${id}" value="${usercasename}"/>
<input type="hidden" id="usercaseid${id}" value="${usercaseid}"/></td>
</tr>`;

                    join_body.append(str);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }
        })
    });

    /*编辑用例*/
    //获取关联用例集信息
    $("#upjoinsearch").click(function (e) {
        var templateid = $("#templatelist").find("option:selected").val();
        var upcase_text = $("#upcase_text").val();
        var join_body = $("#upjoin_body");
        $.ajax({
            type: "POST",
            url: "/testcase/getCasesFromSuiteNameSearch/",
            data: {t_id: templateid, "casename": upcase_text},
            dataType: "json",
            beforeSend: function (XMLHttpRequest) {
                join_body.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
            },
            success: function (data) {
                join_body.empty();

                var msg_info = data.msg2;
                for (var i = 0, l = msg_info.length; i < l; i++) {
                    var interfaceid = msg_info[i]["interfaceid__id"];  //接口id
                    var id = msg_info[i]["id"];  //用例集id
                    var interfacename = msg_info[i]["interfaceid__interfacename"];  //接口名称
                    var usercasename = msg_info[i]["usercaseid__usercasename"];  //用例名称
                    var usercaseid = msg_info[i]["usercaseid"];  //用例ID

                    let str = `<tr>
                                  <td><input type="checkbox" val="${id}" name="upjoincheck"/><input type="hidden" id="upinterface_id${id}" value="${interfaceid}"/></td>
                                  <td>${interfacename}<input type="hidden" id="upinterfacename_${id}" value="${interfacename}"/></td>
                                  <td>
                                    ${usercasename}
                                    <input type="hidden" id="upusercasename_${id}" value="${usercasename}"/>
                                    <input type="hidden" id="upusercaseid${id}" value="${usercaseid}"/>
                                  </td>
                            </tr>`;

                    join_body.append(str);

                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }
        })

    });

    //关联信息tab点击添加按钮-添加选中关联用例
    $("#upaddjoin").click(function (e) {
        if ($("#upjoin_body tr").length > 0) {
            $("input[name='upjoincheck']").each(function () {
                if ($(this).is(":checked")) {
                    var id = $(this).attr("val"); //获取ID
                    var interfaceid = $("#upinterface_id" + id).val();   //接口ID
                    var interfacename = $("#upinterfacename_" + id).val();    //接口名称
                    var usercasename = $("#upusercasename_" + id).val();    //用例名称
                    var usercaseid = $("#upusercaseid" + id).val();    //用例ID

                    let join_info = `
                                <tr id="upjoin_tr${id}">
                                    <td><input type="checkbox" name="updel_box"/></td>
                                    <td>
                                        ${interfacename}
                                        <input type="hidden" name="upt_id" value="${id}"/>
                                        <input type="hidden" name="upinterface_id" value="${interfaceid}"/>
                                        <input type="hidden" name="upinterface_name" value="${interfacename}"/>
                                    </td>
                                    <td>
                                        ${usercasename}
                                        <input type="hidden" name="upcase_id" value="${usercaseid}"/>
                                        <input type="hidden" name="upcase_name" value="${usercasename}"/>
                                    </td>
                                    <td><input type="text" id="upjson_${id}" name="upjson_par" placeholder="多个字段用,分隔"/></td>
                                </tr>
                                `;
                    if ($('upjoin_tr' + id).length == 0) {
                        $("#upjonin_text").append(join_info);
                    }
                    //js控制添加后左侧会隐藏，达到一个接口只能添加一次效果

                }
            })
        }
    });

    //移除选中关联信息
    $("#updeljoin").click(function () {
        $("input[name='updel_box']:checked").each(function () { // 遍历选中的checkbox
            n = $(this).parents("tr").index();  // 获取checkbox所在行的顺序
            $("#upjonin_text").find("tr:eq(" + n + ")").remove();
        });
    });

    /**
     * 编辑用例集，打开页面时，通过“/testcase/testcase_maintain/”获取用例详情
     * 并把数据填充到对应的input框中
     */

    $('#updatecase_info').on('shown.bs.modal', function () {
        var caseid = $("#upcase_id").attr("value");
        var templateid = $("#templatelist").find("option:selected").val();
        var join_body = $("#upjoin_body");
        console.log(caseid,templateid,join_body);
        $.ajax({
            type: "POST",
            url: "/testcase/testcase_maintain/",
            data: {btype: 9, caseid: caseid, "casename": "", "t_id": templateid},
            dataType: "json",
            success: function (data) {
                //读取默认关联用例
                join_body.empty();

                var msg_info2 = data.msg2;
                for (var y = 0, z = msg_info2.length; y < z; y++) {
                    var interfaceid = msg_info2[y]["interfaceid__id"];  //接口id
                    var id = msg_info2[y]["id"];  //用例集id
                    var interfacename = msg_info2[y]["interfaceid__interfacename"];  //接口名称
                    var usercasename = msg_info2[y]["usercaseid__usercasename"];  //用例名称
                    var usercaseid = msg_info2[y]["usercaseid"];  //用例ID


                    let str = `<tr>
                                  <td><input type="checkbox" val="${id}" name="upjoincheck"/><input type="hidden" id="upinterface_id${id}" value="${interfaceid}"/></td>
                                  <td>${interfacename}<input type="hidden" id="upinterfacename_${id}" value="${interfacename}"/></td>
                                  <td>
                                    ${usercasename}
                                    <input type="hidden" id="upusercasename_${id}" value="${usercasename}"/>
                                    <input type="hidden" id="upusercaseid${id}" value="${usercaseid}"/>
                                  </td>
                            </tr>`;

                    join_body.append(str);

                }


                /**
                 * 填充数据到编辑页面的各个字段中
                 */
                var case_info = data.case_infomsg;
                for (var i = 0, l = case_info.length; i < l; i++) {
                    $("#template_detail_id").val(case_info[i]["interfaceid__template_detail__id"]); //用例集详情ID
                    $("#upcase_name").val(case_info[i]["usercasename"]);  //用例名称
                    $("#upparam_info").val(case_info[i]["paraminfo"]);  //参数内容
                    $("#isNeededText").val(case_info[i]["rejoin_key"])//被依赖字段--zijing--20180719
                    $("#run_order").val(case_info[i]["run_order"]) //排序

                    $("#case_url").val(case_info[i]["interfaceurl"]) //URL

                    console.log(case_info[i]["rejoin_key"]=="")
                    if((case_info[i]["rejoin_key"]=="")||(case_info[i]["rejoin_key"]==null))
                        $("#isNeededNO").prop("checked", true);
                    else
                        $("#isNeededOK").prop("checked", true);
                    //头部选择
                    if (case_info[i]["isheader"] == 1) {
                        $("#upisheaderok").prop("checked", true);
                    }
                    else {
                        $("#upisheaderno").prop("checked", true);
                    }
                    $("#upheader_info").val(case_info[i]["headerinfo"]);  //参数内容

                    //获取检查点
                    $("#isequaltext").val(case_info[i]["isequal"]);
                    $("#isnotequaltext").val(case_info[i]["isnotequal"]);
                    $("#iscontaintext").val(case_info[i]["iscontain"]);
                    $("#isnotcontaintext").val(case_info[i]["isnotcontain"]);

                    //是否关联
                    if (case_info[i]["isjoin"] == 1) {
                        $("#upisjoinok").prop("checked", true);

                        $("#upjonin_text").empty();

                        //关联信息
                        var joininfo = eval("(" + case_info[i]["joininfo"] + ")");
                        for (var e = 0, f = joininfo.length; e < f; e++) {
                            var detailid = joininfo[e]["templatedetailid"];
                            var case_id = joininfo[e]["caseid"];
                            var case_name = joininfo[e]["casename"];
                            var interface_id = joininfo[e]["interfaceid"];
                            var interface_name = joininfo[e]["interfacename"];
                            var json_par = joininfo[e]["jsonpar"];

                            let upjoin_info = `
                                    <tr id="upjoin_tr${detailid}">
                                        <td><input type="checkbox" name="updel_box"/></td>
                                        <td>
                                            ${interface_name}
                                            <input type="hidden" name="upt_id" value="${detailid}"/>
                                            <input type="hidden" name="upinterface_id" value="${interface_id}"/>
                                            <input type="hidden" name="upinterface_name" value="${interface_name}"/>
                                        </td>
                                        <td>
                                            ${case_name}
                                            <input type="hidden" name="upcase_id" value="${case_id}"/>
                                            <input type="hidden" name="upcase_name" value="${case_name}"/>
                                        </td>
                                        <td><input type="text" id="upjson_${detailid}" name="upjson_par" 
                                        value="${json_par}" placeholder="多个字段用,分隔"/></td>
                                    </tr>
                                    `;
                            $("#upjonin_text").append(upjoin_info);
                        }


                    }
                    else {
                        $("#upisjoinno").prop("checked", true);//wangfan edit 2018-07-16
                        $("#upjonin_text").empty();
                    }
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }
        })
    });

    //编辑用例，后保存
    // edited by zijing-2018-07-19
    $("#upsavecase").click(function (e) {

        var upcase_id = $("#upcase_id").val();    //用例ID
        var casename = jQuery.trim($("#upcase_name").val());  //用例名称
        var param_info = jQuery.trim($("#upparam_info").val()).replace(/\s+/g, ""); //参数信息
        re = new RegExp("'", "g");
        param_info = param_info.replace(re, '"');
        var isheader = 0;
        var header_info = "";
        if ($("#upisheaderok").is(":checked")) {
            isheader = 1;
            // header_info = jQuery.trim($("#upheader_info").val()).replace(/\s+/g, "");  //获取头部信息
                var contentType = jQuery.trim($("#header_value_01").val());//请求头
            // console.log(contentType)
            if (contentType == 1)
                contentType = "application/x-www-form-urlencoded";
            else
                contentType = "application/json";
             header_info = jQuery.trim($("#upheader_info").val()).replace(/\s+/g, "");
            if (header_info.length <= 0) {
                header_info = "{" + "\"Content-Type\":\"" + contentType + "\"" + "}"
            }

            else if (header_info.length>0&header_info.indexOf("Content-Type")>-1) {
                  header_info = jQuery.trim($("#upheader_info").val()).replace(/\s+/g, "");
            }
            else{
                var headers = ",\"Content-Type\":\"" + contentType + "\"";
                // console.log(headers)
                header_info = jQuery.trim($("#upheader_info").val()).replace(/\s+/g, "").slice(0, -1) + headers + "}";  //获取头部信息和请求头
                console.log(header_info)}


        }

        var isNeeded = 0;
        // var rejoin_keys = "";
        // if ($("#isNeededOK").is(":checked")) {
        isNeeded = 1;
        var rejoin_keys = jQuery.trim($("#isNeededText").val());  //获取被依赖信息

        var run_order  = $("#run_order").val();//获取排列序号
        var case_url = $("#case_url").val();//获取url
        // }

        //检查点内容
        var isequaltext = jQuery.trim($("#isequaltext").val());  //是否相等
        var isnotequaltext = jQuery.trim($("#isnotequaltext").val());  //是否相等
        var iscontaintext = jQuery.trim($("#iscontaintext").val());  //是否包含
        var isnotcontaintext = jQuery.trim($("#isnotcontaintext").val());  //是否不包含

        var isjoin = 0;
        if ($("#upisjoinok").is(":checked")) {
            isjoin = 1;
            //拼接选中列表
            var trList = $("#upjonin_text tr").length;
            var pus_detail = [];
            for (var j = 0; j < trList; j++) {
                var case_id = $("input[name='upcase_id']").eq(j).val();  //用例ID
                var interface_id = $("input[name='upinterface_id']").eq(j).val();  //接口ID
                var json_par = '"' + $("input[name='upjson_par']").eq(j).val() + '"';  //关联字段
                var interface_name = '"' + $("input[name='upinterface_name']").eq(j).val() + '"';  //接口名称
                var case_name = '"' + $("input[name='upcase_name']").eq(j).val() + '"';  //用例名称
                var t_id = $("input[name='upt_id']").eq(j).val();  //用例集详情ID
                var detailinfo = `{"templatedetailid":${t_id},
                "caseid":${case_id},"casename":${case_name},
                "interfaceid":${interface_id},
                "interfacename":${interface_name},
                "jsonpar":${json_par}}`;
                pus_detail.push(detailinfo);
            }
            var joindetail = `[${pus_detail}]`;
        }

        if (casename.length == 0) {
            alert("用例名称不能为空！")
        }else if((run_order != null || run_order !=" ")&& (isNaN(run_order))){
            alert("执行顺序，只能为数字！")
        }
        else {
            $.ajax({
                type: "POST",
                url: "/testcase/updateCaseToUserCase/",
                data: {
                    case_name: casename,
                    param_info: param_info,
                    isequal: isequaltext,
                    isnotequal: isnotequaltext,
                    iscontain: iscontaintext,
                    isnotcontain: isnotcontaintext,
                    isheader: isheader,
                    headerinfo: header_info,
                    isNeeded: isNeeded,
                    rejoin_keys: rejoin_keys,
                    isjoin: isjoin,
                    join_info: joindetail,
                    upcase_id: upcase_id,
                    run_order:run_order,
                    case_url:case_url
                },
                dataType: "json",

                success: function (data) {
                    alert(data.msg)
                    if(data.retcode==0){
                        $('#updatecase_info').modal('toggle')
                        //查询用例集明细
                        userCasesSearchList()
                        // getusercaselist();
                    }

                },
                error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                    if (textStatus == 'error')
                        alert("Ajax返回出错了");
                }
            });
        }
    });
    //批量删除
    $('#btn_delete').on('click', function () {
        var rows = $("#testtable").bootstrapTable("getSelections");
        var case_ids=new Array();
        if (rows.length<1)
            alert("请选择要删除的行")
        else{
            for(i = 0;i<rows.length;i++){
                case_ids.push(rows[i].usercaseid__id)
            }
            console.log(case_ids)
            $.ajax({
                type: "POST",
                url: "/testcase/batchDelete/",
                data: {
                    case_ids:case_ids
                },
                traditional: true,
                timeout: 15000,
                success: function (data) {
                    data=JSON.parse(data)
                    if(data.code==200){
                        alert(data.msg)
                        userCasesSearchList()
                    }
                    else
                        alert(data.msg+"；用例编号："+data.data)
                }
            })
        }

    })
    userCasesSearchList()

});

//查询用例集
function getusercaselist2() {
    var templateid = $(templatelist).find("option:selected").val();
    var interface_info = $("#interface_info");
    $.ajax({
        type: "POST",
        url: "/testcase/testcase_maintain/",
        data: {btype: 5, templateid: templateid},
        dataType: "json",
        beforeSend: function (XMLHttpRequest) {
            interface_info.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
        },
        success: function (data) {
            interface_info.empty();

            var msg_info = data.msg;
            var case_msg = data.casemsg;
            for (var i = 0, l = msg_info.length; i < l; i++) {


                //循环获取用例集名称
                var usercasename = "";
                for (var j = 0, k = case_msg.length; j < k; j++) {
                    if (case_msg[j]["id"] == msg_info[i]["usercaseid"]) {
                        usercasename = case_msg[j]["usercasename"];   //用例名称
                    }
                }

                var interfaceid = msg_info[i]["interfaceid__id"];  //接口id
                var id = msg_info[i]["id"];  //用例集id
                var temlatename = msg_info[i]["templateid__templatename"];   //用例集名称
                var pname = msg_info[i]["interfaceid__pname"];  //项目名称
                var mname = msg_info[i]["interfaceid__mname"];  //模块名称
                var interfacename = msg_info[i]["interfaceid__interfacename"];  //接口名称
                var url = msg_info[i]["interfaceid__url"];  //URL
                var defaultpar = msg_info[i]["interfaceid__defaultpar"];  //默认参数
                var interfacetype = msg_info[i]["interfaceid__type"];   //获取类型
                var interface_type = "";   //请求方式
                switch (interfacetype) {
                    case 0:
                        interface_type = "GET";
                        break;
                    case 1:
                        interface_type = "POST";
                        break;
                }
                var usercaseid = msg_info[i]["usercaseid"];
                let usercase_id;
                if (usercaseid == -1) {
                    usercase_id = `<a style="cursor: pointer" target="_blank" data-toggle="modal" data-target="#case_info" onclick="values(${id},${interfaceid})"><span class="glyphicon glyphicon-plus-sign" style="color: rgb(255, 0, 0);">新建</span></a>`
                }
                else {
                    usercase_id = `<a style="cursor: pointer" target="_blank" data-toggle="modal" data-target="#updatecase_info" onclick="getcasevalue(${usercaseid})"><span class="glyphicon glyphicon-edit" style="color: rgb(0, 0, 255);">编辑</span></a>`
                }
                let str = `<tr>
                                  <td>${id}</td>
                                  <td>${pname}/${mname}</td>
                                  <td>${temlatename}</td>
                                  <td>${usercasename}</td>
                                  <td>${interfacename}</td>
                                  <td style="width:300px;word-break:break-all;">${url}</td>
                                  <td style="width:300px;word-break:break-all;">${defaultpar}<input type="hidden" id="defpar_${id}" value="${defaultpar}"/></td>
                                  <td>${interface_type}</td>
                                  <td>${usercase_id}</td>
                                  <td><a class="glyphicon glyphicon-remove" onclick="removecase(${id})" style="color: rgb(255, 0, 0);cursor:pointer"></a></td>
                              </tr>`;

                interface_info.append(str);

            }

        },
        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
            if (textStatus == 'error')
                alert("Ajax返回出错了");
        }
    })
}

//删除用例
function removecase(id) {
    if (confirm("确定删除数据")) {
        $.ajax({
            type: "POST",
            url: "/testcase/deleteCaseFromSuite/",
            data: {id: id},
            dataType: "json",

            success: function (data) {
                alert(data.msg)
                userCasesSearchList()
                // getusercaselist();//20180719 zijing edited
            },
            error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }
        });
    }
}

//根据项目查找模块
function getprojectinfo(pname, mname, btype, fulltype) {

    var val = $(pname).find("option:selected").val();
    $.ajax({
        type: "POST",
        url: "/testcase/testcase_maintain/",
        data: {btype: btype, pro_type: val},
        dataType: "json",

        success: function (data) {
            var msg_info = data.msg;
            $(mname).empty();
            if (fulltype == 1) {
                $(mname).append($("<option>").val("-1").text("全部模块"));
            }
            for (var i = 0, l = msg_info.length; i < l; i++) {
                // 实际的应用中，这里的option一般都是用循环生成多个了
                var option = $("<option>").val(msg_info[i]["mnumber"]).text(msg_info[i]["modelname"]);
                $(mname).append(option);
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
            if (textStatus == 'error')
                alert("Ajax返回出错了");
        }
    })
}

function values(ID, InterfaceID) {
    $("#id").val(ID);
    $("#InterfaceID").val(InterfaceID);
    // console.log($("#defpar_"+ID).text().replace(/(^\s*)|(\s*$)/g, ""))
    $("#param_info").val($.trim($("#defpar_" + ID).text()).replace(/\s+/g, ""));
}

// 读取用例信息
function getcasevalue(caseid) {
    console.log(caseid)
    $("#upcase_id").val(caseid);
}

//提示语公共方法
function tishi(name, info, type) {
    if (type == 0) {
        $(name).attr("data-content", "<span class='glyphicon glyphicon-question-sign' " +
            "style='color: rgb(255, 0, 0);'>" + info + "</span>");
        $(name).popover('show');
    }
    else {
        $(name).attr("data-content", "<span class='glyphicon glyphicon-ok-sign' " +
            "style='color: rgb(0, 162, 65);'>" + info + "</span>");
        $(name).popover('show');
    }
}

//添加template明细
function addtemplatedetail(templateid, interfaceid, btype) {
    $.ajax({
        type: "POST",
        url: "/testcase/testcase_maintain/",
        data: {btype: btype, templateid: templateid, interfaceid: interfaceid},
        dataType: "json",

        success: function (data) {
            var msg_info = data.addmsg;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
            if (textStatus == 'error')
                alert("Ajax返回出错了");
        }
    })
}

/**
 * 查询按钮调用
 * @params get请求后的参数字典；主要是分页及查询用
 * @author zijing 2018-08-06
 */
function userCasesSearchList() {
    if($("#pro_name").find("option:selected"))
        limitNumber=10
    else
        limitNumber=$.trim($(".page-size").text())
    if ($('.page-item.active a'))
        pageNumberSet=1;
    else
        pageNumberSet=$.trim($('.page-item.active a').text())
    var params={
        pageNumber: pageNumberSet,
        limit: limitNumber,   //页面大小params.limit
        suite_id: $(templatelist).find("option:selected").val(),
        query_name: $('#query_name').val()
    }
    $('#testtable').bootstrapTable('destroy');
    var oTable = new TableInit();
    oTable.Set(params);
    $("#case_right_resul2").empty();
    $("#EdidtButton").empty();

}
/**
 * 分页主要调用函数
 * @params get请求后的参数字典；主要是分页及查询用
 * @author zijing 2018-08-08
 */
var TableInit = function (params) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Set = function (params) {
        console.log(params)
        $('#testtable').bootstrapTable({
            url: '/testcase/getCasesFromSuite/',     //请求后台的URL（*）
            method: 'POST',                      //请求方式（*）
            dataType:'json',
            contentType: "application/x-www-form-urlencoded",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: false,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                    //是否启用排序
            sortOrder: "desc",               //排序方式 asc顺序，desc倒序
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: params.pageNumber,                      //初始化加载第一页，默认第一页
            pageSize: params.limit,                       //每页的记录行数（*）
            pageList: [5, 10, 15, 20],        //可供选择的每页的行数（*）
            search: false,                      //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: false,                 //是否显示所有的列
            showRefresh: false,                 //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 400,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showToggle: false,                  //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                  //是否显示父子表
            columns: [{
                checkbox: true,
                width: '5%'
            }, {
                field: 'usercaseid__id',
                title: '用例编号',
                align: 'center',
                width: '10%'
            }, {
                field: 'usercaseid__usercasename',
                title: '用例名称',
                align: 'left',
                width: '15%'
            },{
                field: 'interfaceid__interfacename',
                title: '接口名称',
                align: 'left',
                width: '15%'
            }, {
                field: 'usercaseid__interfaceurl',
                title: '接口URL',
                align: 'left',
                width: '25%'
            }],
            responseHandler:function (res) {
                if(res==0||res['retcode']!=0){
                    alert("查询出问题！")
                }else{
                    return res
                }
            },
            onLoadError:function (status) {
                $('#testtable').bootstrapTable('removeAll');
            }
        });
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一致
            limit: $.trim($(".page-size").text()),   //页面大小params.limit
            offset: params.offset,  //页码
            suite_id: $(templatelist).find("option:selected").val(),
            query_interface_name: $('#query_interface_name').val(),
            query_case_name: $('#query_case_name').val(),
        };
        return temp;
    };
    return oTableInit;
};

/**
 * 获取用例详情
 * @author shasha 20180810
 */
$(document).on('click',"#testtable tr",function() {
    var templateid = $(templatelist).find("option:selected").val();
    var caseId = $(this).find("td").eq(1).text();
    $.ajax({
        type:'POST',
        url:'/testcase/caseDetail/',
        dataType:'json',
        data:{
            id:caseId
        },
        success: function (data) {
            var msg_info = data.msg;
            for (var i = 0, l = msg_info.length; i < l; i++) {


                var interfaceid = msg_info[i]["interfaceid__id"];  //接口id
                var id = msg_info[i]["usercaseid__id"];  //用例id

                var interfacename = msg_info[i]["interfaceid__interfacename"];  //接口名称
                var casename = msg_info[i]["usercaseid__usercasename"];  //用例名称
                var defaultpar = msg_info[i]["usercaseid__paraminfo"];  //用例参数
                var interfacetype = msg_info[i]["interfaceid__type"];   //获取类型
                var interface_type = "";   //请求方式
                switch (interfacetype) {
                    case 0:
                        interface_type = "GET";
                        break;
                    case 1:
                        interface_type = "POST";
                        break;
                }
                var usercaseid = msg_info[i]["usercaseid"];
                let usercase_id;
                if (usercaseid == -1) {
                    usercase_id = `<button  class='btn editbutton' target="_blank" data-toggle="modal"
                    data-target="#case_info" onclick="values(${id},${interfaceid})">
                        新建</button>`
                }
                else {
                    usercase_id = `<button  class='btn editbutton' target="_blank" data-toggle="modal"
                    data-target="#updatecase_info" onclick="getcasevalue(${usercaseid})">
                        编辑</button>`
                }
                let str = `<tr><th>用例编号：</th></tr>
                <tr><td>${id}</td></tr>
                <tr><th>用例名称：</th></tr>
                <tr><td>${casename}</td></tr>
                <tr><th>接口名称：</th></tr>
                <tr><td>${interfacename}</td></tr>
                <tr><th>请求方式：</th></tr>
                <tr><td>${interface_type}</td></tr>
                <tr><th>参数：</th></tr>
                <tr><td style="width:300px;word-break:break-all;">${APP.format(defaultpar)}</td></tr>`;

                let edit =`<tr><td>${usercase_id}</td></tr>`
                $("#case_right_resul2").html(str);
                $("#EdidtButton").html(edit);

            }

        }

    });

});