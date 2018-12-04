/**
 * 作者：小华
 *描述：定时任务JS
 */
$(document).ready(function () {
//动态获取用例集
$("#proinfo").change(function (e) {
    var proid = $("#proinfo").find("option:selected").val();
    var mname = "#caseinfo";
    if (proid == "-1") {
        $(mname).children().remove();
        var option = $("<option>").val("-1").text("请选择用例集");
        $(mname).append(option);
    } else {
        $.ajax({
            type: "POST",
            url: "/job/job/",
            data: {btype: 1, proid: proid},
            dataType: "json",

            success: function (data) {

                var msg_info = data.template_msg;
                $(mname).empty();
                for (var i = 0, l = msg_info.length; i < l; i++) {
                        // 实际的应用中，这里的option一般都是用循环生成多个了
                        var option = $("<option>").val(msg_info[i]["id"]).text(msg_info[i]["templatename"]);
                        $(mname).append(option);
                }
            },
                error: function (XMLHttpRequest, textStatus, errorThrown, data) {
                    if (textStatus == 'error')
                        alert("Ajax返回出错了");
                }
            })
        }
    });


//添加定时任务
$("#savejob").click(function (e){
    var job_name = jQuery.trim($("#job_name").val());  //任务名称
    var mail = jQuery.trim($("#mail").val());  //EMAIL
    var day_of_week=$("#day_of_week").find("option:selected").val();  //时间段
    var hour=$("#hour").find("option:selected").val();  //小时
    var minute=$("#minute").find("option:selected").val();  //分
    var second=$("#second").find("option:selected").val();  //秒
    var runnertime=hour+":"+minute+":"+second;   //时分秒

    var jobtype=$("#jobtype").find("option:selected").val();  //任务类型
    var caseinfo=$("#caseinfo").find("option:selected").val();  //用例集ID
    var jobcontent=jQuery.trim($("#jobcontent").val());     //JOB描述
    var jobtarget=jQuery.trim($("#jobtarget").val());       //JOB目标

    $.ajax({
        type: "POST",
        url: "/job/job/",
        data: {btype:2,job_name: job_name, mail: mail,day_of_week:day_of_week,runnertime:runnertime,jobtype:jobtype,caseinfo:caseinfo,jobcontent:jobcontent,jobtarget:jobtarget},
        dataType: "json",

        success: function (data) {
            msginfo=data.msg;
            //清空
            $("#job_name").val("");
            alert("OK");
            getjobinfo();
            $('#myModal_addin').modal('hide');
        },
        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
            if (textStatus == 'error')
                alert("Ajax返回出错了");
        }
    })

});


//编辑定时任务
$("#updatejob").click(function (e){
    var id = jQuery.trim($("#j_id").val());  //ID
    var job_name = jQuery.trim($("#upjob_name").val());  //任务名称
    var mail = jQuery.trim($("#upmail").val());  //EMAIL
    var day_of_week=$("#upday_of_week").find("option:selected").val();  //时间段
    var hour=$("#uphour").find("option:selected").val();  //小时
    var minute=$("#upminute").find("option:selected").val();  //分
    var second=$("#upsecond").find("option:selected").val();  //秒
    var runnertime=hour+":"+minute+":"+second;   //时分秒

    var jobtype=$("#upjobtype").find("option:selected").val();  //任务类型
    var jobcontent=jQuery.trim($("#upjobcontent").val());     //JOB描述
    var jobtarget=jQuery.trim($("#upjobtarget").val());       //JOB目标

    $.ajax({
        type: "POST",
        url: "/job/job/",
        data: {btype:5,job_name: job_name, mail: mail,day_of_week:day_of_week,runnertime:runnertime,jobtype:jobtype,id:id,jobcontent:jobcontent,jobtarget:jobtarget},
        dataType: "json",

        success: function (data) {
            msginfo=data.msg;
            getjobinfo();
            alert("OK");
            $('#upmyModal').modal('hide');
        },
        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
            if (textStatus == 'error')
                alert("Ajax返回出错了");
        }
    })
});



//开启定时任务
$("#startjob").click(function (e){
    alert("启动成功!");
    $.ajax({
        type: "POST",
        url: "/job/job/",
        data: {btype:4},
        dataType: "json",

        success: function (data) {
            msginfo=data.msg;
            alert(msginfo);
        }
    })

});


//查询
$("#selectjob").click(function (e){
    var jobkey=jQuery.trim($("#jobkey").val());  //任务ID
    getjobinfo(jobkey)
});


//根据条件搜索或更新
function getjobinfo(jobkey) {
    var jobinfo=$("#jobinfo");
    $.ajax({
        type: "POST",
        url: "/job/job/",
        data: {btype: 3, jobkey: jobkey},
        dataType: "json",
        beforeSend: function (XMLHttpRequest) {
            jobinfo.empty();
            jobinfo.html("<img src='/static/images/loading.gif' />"); //在后台返回success之前显示loading图标
        },
        success: function (data) {
            jobinfo.empty();
            var msg_info = data.msg;
            jobinfo.empty();
            for (var i = 0, l = msg_info.length; i < l; i++) {
                    var id = msg_info[i]["id"];  //序号
                    var jobid = msg_info[i]["jobid"];  //任务ID
                    var mailaddress = msg_info[i]["mailaddress"];  //邮箱地址
                    var day_of_week = msg_info[i]["day_of_week"];  //时间段
                    var day_of_week2='';
                    if(day_of_week=="mon-fri")
                    {
                        day_of_week2='星期一到五';
                    }
                    else
                    {
                        day_of_week2='星期一到日';
                    }
                    var runnertime = msg_info[i]["runnertime"];  //执行时间
                    var caselist = msg_info[i]["caselist"];  //用例集ID
                    var jobtype=msg_info[i]["jobtype"];     //任务状态
                    var jobname=msg_info[i]["jobname"];     //任务名称
                    var job_type='';
                    if(jobtype==1)
                    {
                        job_type='暂停';
                    }
                    else
                    {
                        job_type='正常';
                    }
                    var jobcontent=msg_info[i]["jobcontent"];     //JOB描述
                    var jobtarget=msg_info[i]["jobtarget"];       //JOB目标

                    let str = `<tr id="jobtr${id}">
                                  <td>${jobid}</td>
                                  <td>${jobname}</td>
                                  <td>${day_of_week2}</td>
                                  <td>${runnertime}</td>
                                  <td style="display:none">${jobtype}</td>
                                  <td>${job_type}</td>
                                  <td>${mailaddress}</td>
                                  <td style="display:none">${caselist}</td>
                                  <td style="display:none">${day_of_week}</td>
                                  <td style="display:none">${jobcontent}</td>
                                  <td style="display:none">${jobtarget}</td>
                                  <td>
                                        <a style="cursor:pointer" onclick="updatejob(${id})" data-toggle="modal" data-target="#upmyModal">编辑</a>
                                   </td>
                                   <td>
                                        <a style="cursor:pointer" name="deljob" id="${id}">删除</a>
                                   </td>
                            </tr>`;

                    jobinfo.append(str);
            }

        },
        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
            if (textStatus == 'error')
                alert("Ajax返回出错了");
        }
    })
}


//删除定时任务
$("#jobinfo").on('click',"[name='deljob']",function(){
    var id=$(this).attr("id");

    if(confirm("确定删除吗")){
        $.ajax({
        type: "POST",
        url: "/job/job/",
        data: {btype:6,id:id},
        dataType: "json",

        success: function (data) {
            msginfo=data.msg;
            getjobinfo();
            alert("删除成功");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown, data) {
            if (textStatus == 'error')
                alert("Ajax返回出错了");
        }
    });
        return true;
    }
    return false;

});

});


