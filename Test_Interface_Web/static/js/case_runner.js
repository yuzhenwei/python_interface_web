/**
 * Created by Administrator on 2018/6/20.
 */


$(document).ready(function () {
    //获取用例集
    $("#project_id").change(function (e) {
        var val=$("#project_id").find("option:selected").val();
        var templatename="#template_id";
        if(val == "-1"){
            $(templatename).children().remove();
            var option = $("<option>").val("-1").text("---请选择---");
            $(templatename).append(option);
        }else(
            $.ajax({
                type:"POST",
                url:"/testcase/testcaserunner/",
                data:{btype:1,proid:val},
                dataType:"json",

                success: function(data) {

                    var msg_info= data.template_msg;
                    $(templatename).empty();
                    for(var i=0,l=msg_info.length;i<l;i++) {
                        // 实际的应用中，这里的option一般都是用循环生成多个了
                        var option = $("<option>").val(msg_info[i]["id"]).text(msg_info[i]["templatename"]);
                        $(templatename).append(option);
                    }
                },
                error: function(XMLHttpRequest, textStatus, errorThrown,data){
                    if (textStatus == 'error')
                        alert("Ajax返回出错了");
                }})
        )

    });

    //根据用例集ID查询用例信息
    $("#selectuser").click(function (e) {
        var val=$("#template_id").find("option:selected").val();
        var caseinfo=$("#caseinfo");
        $.ajax({
            type:"POST",
            url:"/testcase/testcaserunner/",
            data:{btype:2,templateid:val},
            dataType:"json",
            beforeSend: function (XMLHttpRequest) {
                caseinfo.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
            },
            success: function(data) {
                caseinfo.empty();
                var msg_info= data.caseinfo;
                for(var j=0,k=msg_info.length;j<k;j++) {
                    //添加用例内容
                    let str = ``;
                    var id = msg_info[j]["usercaseid_id"];
                    var interfacename = msg_info[j]["interfaceid__interfacename"];   //接口名称
                    var usercasename = msg_info[j]["usercaseid__usercasename"];      //用例名称
                    var caseid=msg_info[j]["usercaseid_id"];                           //用例ID
                    var isequal = msg_info[j]["usercaseid__isequal"];                //是否相等
                    var isnotequal = msg_info[j]["usercaseid__isnotequal"];         //是否不相等
                    var url = msg_info[j]["usercaseid__interfaceurl"];                      //url
                    var paraminfo = msg_info[j]["usercaseid__paraminfo"];          //用例参数
                    str = `<tr class="warning" name="content_info">
                                  <td>${caseid}</td>
                                  <td>${interfacename}</td>
                                  <td>${usercasename}</td>
                                  <td style="width:300px;word-break:break-all;">${url}</td>
                                  <td style="width:300px;word-break:break-all;">${paraminfo}</td>
                                  <td id="load_${id}"></td>
                                  <td>
                                        <a style="cursor: pointer" data-toggle="collapse" data-target="#result_info${id}">查看结果</a>
                                        <input type="hidden" name="sortnum" value="${id}">
                                        <input type="hidden" name="caseid" value="${caseid}">
                                        <input type="hidden" name="isequal" value=${isequal}>
                                        <input type="hidden" name="isnotequal" value=${isnotequal}>
                                  </td>
                                </tr>
                                  <tr name="result_info" id="result_info${id}" class="collapse">
                                         <td colspan="7">
                                            <ul id="myTab" class="nav nav-tabs">
                                                 <li class="active"><a href="#json_result${id}" data-toggle="tab">报文结果</a></li>
                                                 <li><a href="#check_result${id}" data-toggle="tab">检查点结果</a></li>
                                                 <li><a href="#actual_param${id}" data-toggle="tab">实际请求参数</a></li>
                                            </ul>
                                             <div id="myTabContent" class="tab-content">
                                                 <div class="tab-pane in active scroll_bar" id="json_result${id}" style="text-align:left;height:330px;overflow: auto;font-size: 13px">
                                                 </div>
                                                  <div class="tab-pane" id="check_result${id}" style="text-align:left;height:330px;overflow: auto;font-size: 13px">
                                                      <table class="table table-hover" style="width: 100%">
                                                        <thead>
                                                            <tr>
                                                                <th>报文内容</th>
                                                                <th>检查条件</th>
                                                                <th>校验结果</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody id="check_body_${id}">
                                                        </tbody>
                                                    </table>
                                                  </div>
                                                  <div class="tab-pane" id="actual_param${id}" style="text-align:left;height:330px;overflow: auto;font-size: 13px">
                                                      <table class="table table-hover" style="width: 100%; table-layout: fixed;word-wrap:break-word;">
                                                        <thead>
                                                            <tr>
                                                                <th>URL</th>
                                                                <th>请求头</th>
                                                                <th>请求参数</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody id="actual_body_${id}">
                                                        </tbody>
                                                    </table>
                                                  </div>
                                              </div>
                                         </td>
                                     </tr>
                                   `;
                    caseinfo.append(str);
                }

            },
            error: function(XMLHttpRequest, textStatus, errorThrown,data){
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }})
    });



//执行接口
    $('#runnerbtn').click(function(e){
        $(this).attr("disabled","disabled");
        var count=$(".warning").length;
        var templetids=$("#template_id").find("option:selected").val();

        for(var m=0;m<count;m++){
            var sortnum = $("#caseinfo tr[name='content_info']").eq(m).find("input[name='sortnum']").val();
            $("#load_"+sortnum).html("<img src='/static/images/loading2.gif' />");
        }

        $.when(toInitTemplate(templetids)).done(function(){
            // console.log("222")
            for(var i=0;i<count;i++) {
                var sortnum = $("#caseinfo tr[name='content_info']").eq(i).find("input[name='sortnum']").val();
                var caseid = $("#caseinfo tr[name='content_info']").eq(i).find("input[name='caseid']").val();
                var isequal = $("#caseinfo tr[name='content_info']").eq(i).find("input[name='isequal']").val();
                var isnotequal = $("#caseinfo tr[name='content_info']").eq(i).find("input[name='isnotequal']").val();
                if (sortnum > 0) {
                    try {
                        loadaajax(caseid,sortnum,templetids, isequal, isnotequal);
                    }
                    catch (err)
                    {
                        $("#json_result" + sortnum).empty();
                        $("#json_result" + sortnum).append(err);
                        $("#load_" + sortnum).empty();
                        $("#load_" + sortnum).append("<span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span>");
                    }
                }
            }
            $('#runnerbtn').removeAttr("disabled");
        });

        //初始化模板用例集为未执行状态
        // $.getJSON("/testcase/start_init/?templetid="+templetids);


    });
    function toInitTemplate(templetids) {
        var defer = $.Deferred();
        $.ajax({
            type: "GET",
            url: "/testcase/start_init/",
            data: {
                templetid: templetids
            },
            dataType: "json",
            error:function(){
                alert("数据传输错误");
            },
            success: function (data) {
                defer.resolve();
            }

        })
        return defer;
    }

//返回结果 紫荆20180719修改添加templateid，更改调用接口
    function  loadaajax(caseid,num,templetids,isequalinfo,isnotequalinfo,iscontaiinfo,isnotcontaininfo) {
        $.ajax({
            type: "POST",
            url: "/testcase/checkrun/",
            data: {
                btype: 3,
                caseid: caseid,
                templetid:templetids
            },
            dataType: "json",
            async:false,
            timeout:995000,

            success: function(data) {
                var resulttype=data.resulttype;
                if(resulttype==200) {
                    var msg_info = data.msg;
                    $("#json_result" + num).empty();
                    $("#json_result" + num).append(APP.format(msg_info));
                    $("#load_" + num).empty();
                    if(data.check_type==1)
                    {
                        $("#load_" + num).append("<span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span>");
                    }
                    else
                    {
                        $("#load_" + num).append("<span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span>");
                    }


                    //检查点
                    var check_body = $("#check_body_" + num);
                    check_body.empty();

                    var checkequal_info=data.check_isequal;
                    var checknotequal_info=data.check_isnotequal;
                    console.log(checkequal_info)
                    console.log(checknotequal_info)

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

                    //实际参数
                    var actual_body = $("#actual_body_" + num);
                    actual_body.empty();

                    var actual_data=data.r_data

                    actual_body.append(actual_data)

                }
                else
                {
                    var error_info =data.msg;
                    $("#json_result" + num).empty();
                    $("#json_result" + num).append(error_info);
                    $("#check_body_" + num).empty();
                    $("#check_body_" + num).append(error_info);
                    $("#actual_body_" + num).empty();
                    $("#actual_body_" + num).append(error_info);
                    $("#load_" + num).empty();
                    $("#load_" + num).append("<span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span>");
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                if (textStatus == 'error') {
                    $("#load_"+num).empty();
                    $("#json_result" + num).empty();
                    $("#json_result" + num).append(errorThrown);
                    $("#check_body_" + num).empty();
                    $("#check_body_" + num).append(errorThrown);
                    $("#actual_body_" + num).empty();
                    $("#actual_body_" + num).append(errorThrown);
                    $("#load_"+num).append("<span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span>");
                }
            }
        })
    }


//生成测试报告
    $("#resultbtn").click(function (e) {
        var spanclass=$("#caseinfo tr[name='content_info']").eq(0).find("span").attr("class");
        if(spanclass!=undefined)
        {
            //获取报告参数
            var pnumber=$("#project_id").find("option:selected").val();
            var totalcount=$("#caseinfo tr[name='content_info']").length;
            var templateid=$("#template_id").find("option:selected").val();
            var okcount=0;
            var failcount=0;
            var errorcount=0;
            var result_pra="";

            for(var i=0;i<totalcount;i++)
            {
                var typeclass=$("#caseinfo tr[name='content_info']").eq(i).find("span").attr("class");
                var stornum = $("#caseinfo tr[name='content_info']").eq(i).find("input[name='sortnum']").val();  //ID序号
                var checkid=$("#check_body_"+stornum+" tr");
                //判断是否运行通过
                if(typeclass=="glyphicon glyphicon-ok")
                {
                    if(checkid.length==0)
                    {
                        okcount++;
                    }
                    else
                    {
                        if($("#check_body_"+stornum).html().indexOf("glyphicon-remove")>-1)
                            failcount++;
                        else
                            okcount++;
                    }
                }
                else
                {
                    errorcount++;
                }

                //报告详情
                result_pra=`{`;
            }
            var now_time=nowtime();
            var result_list=`{"templateid":"${templateid}","totalcount":${totalcount},"okcount":${okcount},"failcount":${failcount},"errorcount":${errorcount},"runnertime":"${now_time}","pnumber":${pnumber}}`;
            //测试报告主表插入结果
            $.ajax({
                type: "POST",
                url: "/testcase/testcaserunner/",
                data: {
                    btype: 4,
                    result_list: result_list
                },
                dataType: "json",
                async:false,
                timeout:15000,
                success: function(data) {
                    var resultid=data.msg;      //返回测试报告ID

                    var result_detail=[];
                    var result_param="";
                    for(var i=0;i<totalcount;i++)
                    {
                        var typeclass=$("#caseinfo tr[name='content_info']").eq(i).find("span").attr("class");
                        var stornum = $("#caseinfo tr[name='content_info']").eq(i).find("input[name='sortnum']").val();  //排序号
                        var json_result=$("#json_result"+stornum).html(); //json结果
                        var checkid=$("#check_body_"+stornum+" tr");
                        var checkinfo=$("#check_body_"+stornum).html();  //检查点内容
                        var actual_data=$("#actual_body_"+stornum).html(); //实际请求参数
                        var caseid=$("#caseinfo tr[name='content_info']").eq(i).find("input[name='caseid']").val();
                        var resulttype=-1;
                        //判断是否运行通过
                        if(typeclass=="glyphicon glyphicon-ok")
                        {
                            if(checkid.length==0)
                            {
                                resulttype=1;
                            }
                            else
                            {
                                if($("#check_body_"+stornum).html().indexOf("glyphicon-remove")>-1)
                                    resulttype=2;
                                else
                                    resulttype=1;
                            }
                        }
                        else
                        {
                            resulttype=0;
                        }
                        result_param=`{"resultid":${resultid},"type":${resulttype},"resultinfo":"""${json_result}""","checkinfo":"""${checkinfo}""","actual_data":"""${actual_data}""","caseid":${caseid}}`;
                        result_detail.push(result_param);
                    }
                    var resultdetail=`[${result_detail}]`;
                    //测试报告明细表插入数据
                    $.ajax({
                        type: "POST",
                        url: "/testcase/testcaserunner/",
                        data: {
                            btype: 5,
                            resultdetail: resultdetail
                        },
                        dataType: "json",
                        async:false,
                        timeout:15000,
                        success: function(data) {
                            var msginfo2=data.msg2;
                            tishi("#resultbtn", "生成报告成功！", 1);
                            window.setTimeout("$('#resultbtn').popover('destroy');", 3000);
                        },
                        error: function(XMLHttpRequest, textStatus, errorThrown,data){
                            if (textStatus == 'error') {
                                tishi("#resultbtn", "生成报告明细失败！", 0);
                                window.setTimeout("$('#resultbtn').popover('destroy');", 3000);
                            }
                        }})

                },
                error: function(XMLHttpRequest, textStatus, errorThrown,data){
                    if (textStatus == 'error') {
                        tishi("#resultbtn","生成报告失败！",0);
                        window.setTimeout("$('#resultbtn').popover('destroy');",3000);
                    }
                }
            })
        }
        else
        {
            tishi("#resultbtn","请先执行用例集！",0);
            window.setTimeout("$('#resultbtn').popover('destroy');",3000);
        }
    });


//读取测试报告列表
    $('#reportmodel').on('shown.bs.modal', function () {
        var templateid=$("#template_id").find("option:selected").val();
        $.ajax({
            type:"POST",
            url:"/testcase/testcaserunner/",
            data:{btype:6,templateid:templateid},
            dataType:"json",
            beforeSend: function (XMLHttpRequest) {
                $("#report_body").html("<img src='/static/images/loading2.gif' />"); //在后台返回success之前显示loading图标
            },
            success: function(data) {
                var msg_info= data.reportinfo;
                $("#report_body").empty();

                for(var i=0,l=msg_info.length;i<l;i++) {
                    var id=msg_info[i]["id"];      //id
                    var pname=msg_info[i]["templateid__pnumber__pname"];
                    var templatename=msg_info[i]["templateid__templatename"];
                    var totalcount=msg_info[i]["totalcount"];
                    var okcount=msg_info[i]["okcount"];
                    var failcount=msg_info[i]["failcount"];
                    var errorcount=msg_info[i]["errorcount"];
                    var runnertime=msg_info[i]["runnertime"];
                    let reportinfo=`
                        <tr>
                           <td>${id}</td>
                           <td>${pname}</td>
                           <td>${templatename}</td>
                           <td>${totalcount}</td>
                           <td>${okcount}</td>
                           <td>${failcount}</td>
                           <td>${errorcount}</td>
                           <td>${runnertime}</td>
                           <td><a href="/report/testreport?id=${id}" target="_blank">查看详情</a></td>
                       </tr>`;
                    $("#report_body").append(reportinfo);
                }


            },
            error: function(XMLHttpRequest, textStatus, errorThrown,data){
                if (textStatus == 'error')
                    alert("Ajax返回出错了");
            }})

    });


//迭代解析json
    function  recursionJSON(data,name,value,type,num) {
        if(num!=undefined) {
            var check_body = $("#check_body_" + num);
            if (typeof(data) == "object") {
                $.each(data, function (i, n) {
                    if (typeof(n) == "object") {
                        recursionJSON(n, name, value, type,num);
                    } else {
                        if (i == name && type == "1") {

                            if (n == value) {
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "==" + value + "</td><td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                            }
                            else
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "==" + value + "</td><td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                        }
                        if (i == name && type == "2") {
                            if (n != value)
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "<>" + value + "</td><td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                            else
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "<>" + value + "</td><td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                        }
                        if (i == name && type == "3") {
                            if (n.indexOf(value) > -1)
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "包含" + value + "</td><td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                            else
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "包含" + value + "</td><td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                        }
                        if (i == name && type == "4") {
                            if (n.indexOf(value) == -1)
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "不包含" + value + "</td><td><span class='glyphicon glyphicon-ok' style='color: rgb(0, 167, 0);'></span></td><tr>");
                            else
                                check_body.append("<tr><td>" + i + ":" + n + "</td><td>" + name + "不包含" + value + "</td><td><span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);'></span></td><tr>");
                        }
                    }
                })
            }
        }
    }





//获取当前时间
    function nowtime()
    {
        var mydate = new Date();
        var str = "" + mydate.getFullYear() + "-";
        str += (mydate.getMonth()+1) + "-";
        str += mydate.getDate() + " ";
        str += mydate.getHours() + ":";
        str += mydate.getMinutes() + ":";
        str += mydate.getSeconds();
        return str;
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

});