/**
 * 分页查询调用函数
 * @params get请求后的参数字典；主要是分页及查询用
 * @author zijing 2018-08-06
 * */
function templateSearchList(params) {

    $('#table').bootstrapTable('destroy');
    //1.初始化Table
    var oTable = new TableInit();
    oTable.Set(params);

}
/**
 * 删除用例集函数
 * @params p是删除的超链接id
 * @author zijing 2018-08-06
 * */
function deleteTemplate(p) {

    $('#deleteModal').modal({
        keyboard: false,
        backdrop: false
    },"show")

    var temId = $(p).parent('td').siblings()[1].innerText;
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
    $("#sure_del").unbind('click').bind('click',function () {
        $.ajax({
            type: "POST",
            url: "/testcase/delete/",
            data: {'templateID': temId},
            success: function (data, status, xhr) {
                data=JSON.parse(data)
                alert(data.msg);
                templateSearchList(params)
                setTimeout(function(){
                    console.log($('.pagination li.page-item').eq(params.pageNumber).addClass('active'))
                },500)
            }
        })
        $('#deleteModal').modal('hide')
    })

}
/**
 * 编辑用例集函数
 * @params p是编辑的超链接id
 * @author zijing 2018-08-06
 * */
function editTemplate(p) {
    var temId = $(p).parent('td').siblings()[1].innerText;
    var proName = $(p).parent('td').siblings()[2].innerText
    var temName = $(p).parent('td').siblings()[3].innerText
    var type = 0

    $('#mymodal h6').text("编辑用例集")
    $('.projectName2').text(proName)
    $('#templateName').val(temName)

    $('#selectproject').click(function (event) {
        return false;
    });

    $('#mymodal').modal('show');
    //避免后台多次提交数据
    $("#save").unbind('click').bind('click', function () {
        temName = $("#templateName").val()

        if (temName == "" || temName == null)
            alert("用例集名称不能为空！");
        else {

            $('#mymodal').modal('hide')
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
            // console.log(params)
            $.ajax({
                type: "POST",
                url: "/testcase/add/",
                data: {'projectName': proName, 'templateName': temName, 'type': type, 'temId': temId},
                success: function (response, status, xhr) {
                    alert(response);
                }
            })
            templateSearchList(params)
            setTimeout(function(){
                console.log($('.pagination li.page-item').eq(params.pageNumber).addClass('active'))
            },500)
            //console.log($('.pagination li.page-item').eq(params.pageNumber))
            //console.log(params.pageNumber,'~~~~~~~~~')
        }
    })

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
        // console.log(params)
        $('#table').bootstrapTable({
            url: '/testcase/projectLists/',     //请求后台的URL（*）
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
                field: 'id',
                title: '项目编号',
                width: '15%'
            }, {
                field: 'pnumber__pname',
                title: '项目名称',
                align: 'center',
                width: '25%'
            }, {
                field: 'templatename',
                title: '用例集名称',
                align: 'center',
                width: '45%'
            }, {
                field: 'id',
                title: '操作',
                width: '10%',
                formatter:function(value, row, index) {
                    var id=value;
                    var result = "";
                    // result += "<a href='javascript:;' class='btn btn-xs green' onclick=\"\" title='查看'><span class='glyphicon glyphicon-search'></span></a>";
                    result += "<a href='javascript:;' id=\"edit"+id+"\" class='btn btn-xs blue' " +
                        "onclick='editTemplate(\"#edit"+id+"\")' title='编辑'>" +
                        "<span class='glyphicon glyphicon-edit' style='color: rgb(0, 0, 255);'>编辑</span></a>";
                    result += "<a href='javascript:;' id=\"delete"+id+"\" class='btn btn-xs red' " +
                        "onclick='deleteTemplate(\"#delete"+id+"\")' title='删除'>" +
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
            pname: $.trim($(".projectName1").text()),
            // statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
};
/**
 * 初始化相关操作及页面一开始加载后的操作
 * @author zijing 2018-08-06
 * */
$(function () {
//初始化刷新用例集列表
    $(document).ready(function () {
        var params={
            pageNumber: 1,
            limit: 10,
            pname: $.trim($(".projectName1").text()),
        }
        templateSearchList(params)
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
                pname: $.trim($(".projectName1").text()),
            }
            // console.log(params)
            templateSearchList(params)
        }
    );
//模态框隐藏
    $('.smodal').click(function () {
        $('#mymodal').modal('show');
        $('#mymodal h6').text("新增用例集")
    });
//新增用例集/testcase/add/
    $("#save").click(function () {
        var projectName = $.trim($(".projectName2").text());
        var templateName = $("#templateName").val();
        if (templateName == "" || templateName == null)
            alert("用例集名称不能为空！");
        else {
            $('#mymodal').modal('hide');
            if ($('.page-item.active a'))
                pageNumberSet=1;
            else
                pageNumberSet=$.trim($('.page-item.active a').text())
            var params={
                pageNumber: pageNumberSet,
                limit: $.trim($(".page-size").text()),
                pname: $.trim($(".projectName1").text()),
            }
            // console.log(params)

            $.ajax({
                type: "POST",
                url: "/testcase/add/",
                data: {'projectName': projectName, 'templateName': templateName, 'type': 1},
                success: function (response, status, xhr) {
                    alert(response);

                    templateSearchList(params)
                }
            })
        }
    });

//更新列表页的下拉菜单
    $("#projectBtn1 li").on('click', function () {
        $('.projectName1').text($(this).text());
    })
//更新模态框里的下拉菜单
    $("#projectBtn2 li").on('click', function () {
        $('.projectName2').text($(this).text());
    })
//模态框初始化
    $('#mymodal').on('hidden.bs.modal', function () {
        $('#mymodal h2').text("新增用例集")
        $('.projectName2').text("请选择");
        $('#templateName').val("")
        $('#selectproject').unbind('click')
    });

})