/**
 * 报告列表页面js
 * @author shidi
 * zijing 20180807 edited 分页
 * */
$(document).ready(function (){
    reportLists()

/**
 * 动态加载两个selector下拉菜单
 * */
    $("#pro").change(function(e) {
        var id = $("#pro").find("option:selected").val();
        var mname = "#templatelist";
        if(id == "-1"){
            $(mname).children().remove();
            var option = $("<option>").val("-1").text("---请选择---");
            $(mname).append(option);
        }else{
             $.ajax({
              type:"POST",
              url:"/report/report/",
              data:{pro:id,btype:1},
              dataType:"json",
              success:function(data)
              {
                  var msg_info = data.msglist;
                  // $(mname).empty();
                  // $(mname).append($("<option>").val("-1").text("---请选择---"));
                  $(mname).children().remove();
                  for (var i = 0;i<msg_info.length;i++)
                  {
                      var option = $("<option>").val(msg_info[i]["id"]).text(msg_info[i]["templatename"]);
                      $(mname).append(option);
                  }
              },
              error:function(XMLHttpRequest,textStatus,errorThrown,data)
              {
                  if (textStatus =="error") {
                      //alert("页面跑神了！");
                      $(mname).empty();
                      $(mname).append($("<option>").val("-1").text("---请选择---"));
                  }

              }
          })
        }

        //请求用例集接口

    });
/**
 *查询按钮加载分页数据
 * */
$("#search").on('click',function () {
    reportLists()
})

});
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
            url: '/report/report/',     //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
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
            // height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showToggle: false,                  //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                  //是否显示父子表
            columns: [{
                field: 'id',
                title: '报告编号',
                width: '5%'
            }, {
                field: 'templateid__pnumber__pname',
                title: '项目名称',
                width: '10%'
            }, {
                field: 'templateid__templatename',
                title: '用例集名称',
                align: 'center',
                width: '15%'
            }, {
                field: 'totalcount',
                title: '用例总数',
                align: 'center',
                width: '5%'
            }, {
                field: 'okcount',
                title: '通过数',
                width: '5%'
            },{
                field: 'failcount',
                title: '失败数',
                width: '5%'
            },{
                field: 'errorcount',
                title: '错误数',
                width: '5%'
            },{
                field: 'runnertime',
                title: '执行时间',
                width: '20%'
            },{
                field: 'id',
                title: '操作',
                width: '20%',
                formatter:function(value, row, index) {
                    var id=value;
                    var result = "";
                    result += "<a href='/report/testreport?id="+id+"' target='_blank'>查看详情</a>"
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
            btype: 2,
            templateid: $("#templatelist").find("option:selected").val()
        };
        return temp;
    };
    return oTableInit;
};

function reportLists() {
    $('#table').bootstrapTable('destroy');
    // 分页初始化
    var params={
            pageNumber: 1,
            limit: 10,
            btype: 2,
            templateid: $("#templatelist").find("option:selected").val()
        }
    //初始化Table
    var oTable = new TableInit();
    oTable.Set(params);
}




