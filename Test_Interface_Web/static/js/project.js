/**
 * 查询按钮调用
 * @params get请求后的参数字典；主要是分页及查询用
 * @author zijing 2018-08-06
 */
function projectSearchList(params) {

    $('#table').bootstrapTable('destroy');
    //初始化Table
    var oTable = new TableInit();
    oTable.Set(params);

}
/**
 * 分页主要调用函数
 * @params get请求后的参数字典；主要是分页及查询用
 * @author zijing 2018-08-06
 */
var TableInit = function (params) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Set = function (params) {
        console.log(params)
        $('#table').bootstrapTable({
            url: '/project/projectLists/',     //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
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
                field: 'mnumber',
                title: '模块编号',
                width: '10%'
            }, {
                field: 'pnumber__pname',
                title: '项目名称',
                align: 'center',
                width: '20%'
            }, {
                field: 'modelname',
                title: '模块名称',
                align: 'center',
                width: '20%'
            }, {
                field: 'description',
                title: '模块描述',
                align: 'center',
                width: '26%'
            },{
                field: 'pnumber',
                title: '项目编号',
                visible: false
            },{
                field: 'mnumber',
                title: '操作',
                width: '24%',
                formatter:function(value, row, index) {
                    var id=value;
                    var result = "";
                    // result += "<a href='javascript:;' class='btn btn-xs green' onclick=\"\" title='查看'><span class='glyphicon glyphicon-search'></span></a>";
                    result += "<a href='javascript:;' id=\"edit"+id+"\" class='btn btn-xs blue' " +
                        "onclick='editProject(\"#edit"+id+"\")' title='编辑'>" +
                        "<span class='glyphicon glyphicon-edit' style='color: rgb(0, 0, 255);'>编辑</span></a>";
                    result += "<a href='javascript:;' id=\"delete"+id+"\" class='btn btn-xs red' " +
                        "onclick='deleteProject(\"#delete"+id+"\")' title='删除'>" +
                        "<span class='glyphicon glyphicon-remove' style='color: rgb(255, 0, 0);cursor:pointer;'>删除</span></a>";

                    return result;
                }
            }],
            responseHandler:function (res) {
                if(res==0||res['retcode']!=0){
                    alert("查询出问题！")
                }else{
                    return res
                }
            },
            onLoadError:function (status) {
                $('#table').bootstrapTable('removeAll');
            }
        });
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一致
            limit: $.trim($(".page-size").text()),   //页面大小params.limit
            offset: params.offset,  //页码
            // page: $('.pagination .active').text(),//页码
            pname: $.trim($("#projectNum").val()),
            // statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
};


/**
 * 新增项目
 */
function submit_page() {
    var pnumber = $("#Pn").val();
    var modelname = $("#mname").val();
    var description = $("#desc").val();
    if(pnumber=='') {
        alert('项目名不能为空！');
        return false;
    }
    if(modelname=='') {
        alert('模块名不能为空！');
        return false;
    }
    if(description=='') {
        alert('模块描述不能为空！');
        return false;
    }
    else{
        // if ($('.page-item.active a')){
        //     pageNumberSet=$.trim($('.page-item.active a').text())
        //     // console.log(pageNumberSet)
        // }
        // else{
        //     pageNumberSet=1;
        // }
        // var params={
        //     pageNumber: pageNumberSet,
        //     limit: $.trim($(".page-size").text()),
        //     pname: $.trim($(".projectName1").text()),
        // }
        $.ajax({
            type:'POST',
            url:'/project/add_project/',
            data:{
                Pn:pnumber,
                modelname:modelname,
                description:description
            },
            success:function(data){
                alert(data);
                location.reload()
            }
        })
        // projectSearchList(params)
        // setTimeout(function(){
        //         console.log($('.pagination li.page-item').eq(params.pageNumber).addClass('active'))
        //     },500)
    }

}
/**
 * 删除按钮获取页面数据
 */
function deleteProject(project){
    var mnumber = $(project).parent('td').siblings()[1].innerText;
    $('#myModaledel').modal({
        keyboard: false,
        backdrop: false
    },"show")
    if ($('.page-item.active a')){
        pageNumberSet=$.trim($('.page-item.active a').text())
        // console.log(pageNumberSet)
    }
    else{
        pageNumberSet=1;
    }
    var params={
        pageNumber: pageNumberSet,
        limit: $.trim($(".page-size").text()),
        pname: $.trim($(".projectName1").text()),
    }
    $("#delete_sure").unbind('click').bind('click',function () {
        $.ajax({
            type: "POST",
            url: "/project/delete_project/",
            data: {mnu:mnumber},
            success: function (data, status, xhr) {
                alert(data);
                projectSearchList(params)
                setTimeout(function(){
                    console.log($('.pagination li.page-item').eq(params.pageNumber).addClass('active'))
                },500)
            }
        })
        $('#myModaledel').modal('hide')
    })
}


/**
 * 编辑项目页确认按钮调用ajax请求
 */
function editProject(project) {

    var mnumber = $(project).parent('td').siblings()[1].innerText;

    $('#myModaledit').modal('show');
    $('#editPn').find("option:contains("+$(project).parent('td').siblings()[2].innerText+")").attr("selected",true);
    $('#modelname_edit').val($(project).parent('td').siblings()[3].innerText)
    $('#description').val($(project).parent('td').siblings()[4].innerText)


    $("#edit_save").unbind('click').bind('click', function () {
        var description = $.trim($('#description').val());
        var pnumber = $.trim($('#editPn').find("option:selected").val());
        var modelname = $.trim($('#modelname_edit').val());
        // console.log(editPn,modelname,mnumber,description)
        if(pnumber=='') {
            alert('项目名不能为空！');
            return false;
        }
        if(modelname=='') {
            alert('模块名不能为空！');
            return false;
        }
        if(description=='') {
            alert('模块描述不能为空！');
            return false;
        }
        else{
            $('#myModaledit').modal('hide')
            if ($('.page-item.active a')){
                pageNumberSet=$.trim($('.page-item.active a').text())
                // console.log(pageNumberSet)
            }
            else{
                pageNumberSet=1;
            }
            var params={
                pageNumber: pageNumberSet,
                limit: $.trim($(".page-size").text()),
                pname: $.trim($(".projectName1").text()),
            }
            $.ajax({
                type:'POST',
                url:'/project/edit_project/',
                data:{
                    editPn:pnumber,
                    modelnames:modelname,
                    mnumbers:mnumber,
                    descriptions:description
                },
                success:function(data){
                    alert(data);
                }
            })
            projectSearchList(params)
            setTimeout(function(){
                console.log($('.pagination li.page-item').eq(params.pageNumber).addClass('active'))
            },500)
        }

    })
}
/**
 * 初始化相关操作及页面一开始加载后的操作
 * @author zijing 2018-08-06
 * */
$(function () {
    $(document).ready(function () {
        var params={
            pageNumber: 1,
            limit: 10,
            pname: $.trim($("#projectNum").val()),
        }
        projectSearchList(params)
    })
    //查找后按项目刷新用例集列表
    $('#search').on('click', function () {
            if ($('.page-item.active a'))
                pageNumberSet=1;
            else
                pageNumberSet=$.trim($('.page-item.active a').text())
            var params={
                pageNumber: pageNumberSet,
                limit: $.trim($(".page-size").text()),
                pname: $.trim($("#projectNum").val()),
            }
            projectSearchList(params)
        }
    );
})