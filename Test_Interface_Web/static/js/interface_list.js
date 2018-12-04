/**
 * Created by Administrator on 2018/5/23.
 * 接口列表页面js
 */

/**
 * 修改页面的JS效果 编辑接口列表后保存接口
 * @param item-接口全部内容
 */
function interface_update(item) {
    // console.log(item)
    $("#pname").val(item.pnumber_id)
    //获取数据列表数据
    $("#interfacename").val(item.interfacename)
    $("#url_id").val(item.url)
    $("#defaultpar").val(item.defaultpar)
    $("#type").val(item.type)
    $("#remark").val(item.remark)
    $("#interface_id").val(item.id)
    var h = "<option selected=selected value='" + item.mnumber + "' >" + item.mname + "</option>";
    $("#mname").append(h)
    $("#title_id").html("修改接口")
    $('#update_Modle').modal({
        keyboard: false,
        backdrop: false
    },"show")

    //动态获取模块的值
    $("#pname").change(function() {

        var pname = $("#pname option:selected").text()
        //判断如果pname为“--请选择--”时，不请求接口
        if(pname == "---请选择---"){
            var options = "<option >---请选择---</option>";
            $("#mname").html(options)

        }else {
            $("#mname").children().remove()
            var pnumber = $("#pname").find("option:selected").val() //获取项目选中的值
            //请求模块接口
            $.getJSON(
                "/interface/search/?pnumber="+pnumber,
                function(data){
                    var msg = data.msg
                    console.log(msg)
                    var options = '';
                    for(var i in msg){
                        options += "<option  value='" + msg[i].mnumber + "' > "+msg[i].modelname+"</option>";
                        console.log(msg[i].modelname);
                    }
                    $("#mname").html(options)
                });

        }

    })
    //提交按钮功能
    $("#oks_id").unbind('click').bind('click',function () {
        //通过item不为null是修改功能否则时添加功能
        submit_page();//调取提交按钮
        interfaceSearchList();//查询接口刷新页面
    })


}

/**
 * 删除页面的JS效果
 * @param req
 */
function interface_del(req) {

    $('#myModal').modal({
        keyboard: false,
        backdrop: false
    },"show")

    $("#sure_del").one('click',function () {
        $.getJSON(
            "/interface/del/?id="+req,
            function (data){
                if(data.code ==200 ){
                    alert("删除成功")
                }else {

                    alert("删除失败")
                }

            }
        )
        $('#myModal').modal('hide')
        search_pro_mo();//查询接口刷新页面
    })

}

/**
 * 关闭按钮刷新页面
 */
function close_id() {
    $('#update_Modle').modal('hide');
}

/**
 * /interface/upadte/提交按钮调用的ajax请求
 */
function submit_page() {
    var ids = $("#interface_id").val()
    var interfacename = $.trim($("#interfacename").val())
    var url_adress = $.trim($("#url_id").val())
    var defaultpar = $.trim($("#defaultpar").val())
    var remark =  $.trim($("#remark").val())
    var type =  $("#type").val()
    var mnumber =  $("#mname").val()
    var pnumber = $("#pname").val()
    var pname = $("#pname option:selected").text()
    var mname = $("#mname option:selected").text()
    if(interfacename ==""){
        alert("接口名称不能为空")
    }else if (url_adress ==""){
        alert("接口地址不能为空")
    }else if(mname =="" || mname =="---请选择---"){
        alert("模块名称不能为空")
    }else if(type ==""){
        alert("请求方式不能为空")
    }else{
        $.ajax({
            type: "POST",//方法类型
            dataType: "json",//预期服务器返回的数据类型
            url: "/interface/upadte/" ,//url
            data:  {"id":ids,"interfacename":interfacename,"url_adress":url_adress,"defaultpar":defaultpar,"remark":remark,
                "type":type,"mnumber":mnumber,"pnumber":pnumber,"pname":pname,"mname":mname},
            success: function (result) {
                // console.log(result);
                if (result.resultCode == 200) {
                    alert("保存成功！");
                }
            },
            error : function() {
                alert("异常！");
            }
        });
        $('#update_Modle').modal('hide');
    }

}

/**
 * 根据项目查询接口列表
 */
function search_pro_mo(params) {
    var params={
        pageNumber: 1,
        limit: 10,   //页面大小params.limit
        // offset: params.offset,  //页码
        pnumber: $("#pro_name").find("option:selected").val(),
        mnumber: $("#pro_mo_name").find("option:selected").val(),
        query_name: $('#query_name').val()
    }
    $('#testtable').bootstrapTable('destroy');
    //初始化Table
    var oTable = new TableInit();
    oTable.Set(params);


}

/**
 * 查询按钮调用
 * @params get请求后的参数字典；主要是分页及查询用
 * @author zijing 2018-08-06
 */
function interfaceSearchList() {
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
        // offset: params.offset,  //页码
        pnumber: $("#pro_name").find("option:selected").val(),
        mnumber: $("#pro_mo_name").find("option:selected").val(),
        query_name: $('#query_name').val()
    }
    $('#testtable').bootstrapTable('destroy');
    var oTable = new TableInit();
    oTable.Set(params);
    $("#right_result2").empty();
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
            url: '/interface/page_sel/',     //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            // dataType:'json',
            // contentType: "application/x-www-form-urlencoded",
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
            // height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showToggle: false,                  //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                  //是否显示父子表
            columns: [{
                checkbox: true,
                width: '5%'
            }, {
                field: 'id',
                title: '接口编号',
                align: 'center',
                width: '10%'
            }, {
                field: 'interfacename',
                title: '接口名称',
                align: 'left',
                width: '15%'
            }, {
                field: 'url',
                title: '接口URL',
                align: 'left',
                width: '5%'
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
            pnumber: $("#pro_name").find("option:selected").val(),
            mnumber: $("#pro_mo_name").find("option:selected").val(),
            query_name: $('#query_name').val()
        };
        return temp;
    };
    return oTableInit;
};

/**
 * 新增接口--“添加接口”按钮调用js方法
 */
function interface_insert() {

    $("#title_id").html("新增接口")
    $('#update_Modle').modal({
        keyboard: false,
        backdrop: false
    },"show")
    //动态获取模块的值
    $("#pname").change(function() {

        var pname = $("#pname option:selected").text()
        //判断如果pname为“--请选择--”时，不请求接口
        if(pname == "---请选择---"){
            var options = "<option >---请选择---</option>";
            $("#mname").html(options)

        }else {
            $("#mname").children().remove()
            var pnumber = $("#pname").find("option:selected").val() //获取项目选中的值
            //请求模块接口
            $.getJSON(
                "/interface/search/?pnumber="+pnumber,
                function(data){
                    var msg = data.msg
                    // console.log(msg)
                    var options = '';
                    for(var i in msg){
                        options += "<option  value='" + msg[i].mnumber + "' > "+msg[i].modelname+"</option>";
                        // console.log(msg[i].modelname);
                    }
                    $("#mname").html(options)
                });

        }

    })
    //提交按钮功能
    $("#oks_id").unbind('click').bind('click',function () {
        var id = $("#interface_id").val()
        //通过item不为null是修改功能否则时添加功能
        submit_page();//调取提交按钮
        var pnumber = $("#pro_name").find("option:selected").val(); //获取项目选中的值
        var mnumber = $("#pro_mo_name").find("option:selected").val();//获取项目选中的值
        if(pnumber !="" & mnumber !="" ){
            search_pro_mo();//查询接口刷新页面
        }

    })
}

/**
 * 批量导出接口数据
 */
function pull_all_interface() {

    var pro_name = $("#pro_name").find("option:selected").text()
    var pro_mo_name = $("#pro_mo_name").find("option:selected").text()
    window.location.href="/interface/export_interface?pro_name="+pro_name+"&pro_mo_name="+pro_mo_name

}

/**
 * 初始化方法
 */
window.onload=function(){
    $("#pro_name").change(function() {
        var pname = $("#pro_name option:selected").text()
        if(pname == "---请选择---"){
            var options = "<option >---请选择---</option>";
            $("#pro_mo_name").html(options)
        }else {
            $("#pro_mo_name").children().remove()
            var pnumber = $("#pro_name").find("option:selected").val() //获取项目选中的值
            //请求模块接口
            $.getJSON(
                "/interface/search/?pnumber="+pnumber,
                function(data){
                    var msg = data.msg
                    // console.log(msg)
                    var options = '';
                    for(var i in msg){
                        options += "<option  value='" + msg[i].mnumber + "' > "+msg[i].modelname+"</option>";
                        // console.log(msg[i].modelname);
                    }
                    $("#pro_mo_name").html(options)
                });
        }

    })
    interfaceSearchList()
    $('#update_Modle').on('hidden.bs.modal', function () {
        // $("#pro_name").val("--请选择--")
        // $("#pro_mo_name").val("--请选择--")
        $('#templateName').val("")
        $("#interfacename").val("")
        $("#url_id").val("")
        $("#defaultpar").val("")
        $("#type").val("")
        $("#remark").val("")
        $("#interface_id").val("")
    });
}
/**
 * 获取接口详情
 */
$(document).on('click',"#testtable tr",function() {
    var interfaceId = $(this).find("td").eq(1).text();
    $.ajax({
        type:'POST',
        url:'/interface/detail/',
        dataType:'json',
        data:{
            id:interfaceId
        },
        success:function(data){
            var tableStr = " ";
            var tableEdit="";
            var item = JSON.stringify(data.msg[0]);//转换为json对象传递给前端
            detail = data.msg;
            var interface_type="";   //请求方式
            switch(detail[0].type )
            {
                case 0:
                    interface_type="GET";
                    break;
                case 1:
                    interface_type="POST";
                    break;
            }
            tableStr = tableStr + "<tr><th>接口编号：</th></tr>"
                + "<td>" + detail[0].id + "</td>"
                + "<tr><th>接口描述：</th></tr>"
                + "<tr><td >" + detail[0].remark  + "</td></tr>"
                + "<tr><th>请求方式：</th></tr>"
                + "<tr><td >" + interface_type + "</td></tr>"
                + "<tr><th>参数：</th></tr>"
                + "<tr><td class='right_result'>" + APP.format(detail[0].defaultpar) + "</td></tr>";
            tableEdit = tableEdit + "<button  class='btn editbutton' onclick='interface_update("+item+")'>编辑</button>"
            //将动态生成的table添加的事先隐藏的div中.
            $("#right_result2").html(tableStr);
            $("#EdidtButton").html(tableEdit);

        }

    })
});
$(function () {
    //查找后按项目刷新用例集列表
    $('#search').on('click', function () {
            interfaceSearchList()
            $("#TableDetail").empty();
            $("#EdidtButton").empty();
        }
    );
    $('#btn_delete').on('click', function () {
        var rows = $("#testtable").bootstrapTable("getSelections");
        var interface_ids=new Array();
        if (rows.length<1)
            alert("请选择要删除的行")
        else{
            for(i=0;i<rows.length;i++){
                interface_ids.push(rows[i].id)
            }
            console.log(interface_ids)
            $.ajax({
                type: "POST",
                url: "/interface/batch_del/",
                data: {
                    inter_ids:interface_ids
                },
                traditional: true,
                timeout: 15000,
                success: function (data) {
                    data=JSON.parse(data)
                    if(data.code==200){
                        alert(data.msg)
                        interfaceSearchList()
                    }
                    else
                        alert(data.msg+"接口编号："+data.data)
                }
            })

        }

    })
})