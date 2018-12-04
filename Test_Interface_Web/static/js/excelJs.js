/**
 * Created by Administrator on 2018/8/3.
 */

function upload_excel(){
    var formData = new FormData()
    formData.append("file",$("#file_ex")[0].files[0]);
    var excel = $('#file_ex').val()
    var opint_leg =excel.lastIndexOf(".")
    var last_name = excel.substring(opint_leg,excel.length)
    if(last_name==".xlsx"){
        $.ajax({
            url : '/interface/upload/',
            type : 'POST',
            async : false,
            data : formData,
            // 告诉jQuery不要去处理发送的数据
            processData : false,
            // 告诉jQuery不要去设置Content-Type请求头
            contentType : false,
            // beforeSend:function(){
            //     console.log("正在进行，请稍候");
            // },
            success : function(data) {
                res = JSON.parse(data)
                if(res.code == 200 ){
                    $("#myModal_addin").modal('hide')
                    alert(res.msg);
                }else{
                    alert(res.msg)
                }

                alert(ress.msg)
            }
        });

    }else {
        alert("选择.xlsx的文件");

    }

}


function upload_case(){
    var formData = new FormData()
    formData.append("file",$("#file_case")[0].files[0]);

    var excel = $('#file_case').val()
    var opint_leg =excel.lastIndexOf(".")
    var last_name = excel.substring(opint_leg,excel.length)
    if(last_name ==".xlsx"){
        $.ajax({
        url : '/interface/upload_case/',
        type : 'POST',
        async : false,
        data : formData,
        // 告诉jQuery不要去处理发送的数据
        processData : false,
        // 告诉jQuery不要去设置Content-Type请求头
        contentType : false,
        beforeSend:function(){
            console.log("正在进行，请稍候");
        },
        success : function(data) {
            var res = JSON.parse(data)
            if(res.code == 200){
                $("#myModal_case_addin").modal('hide')
                alert(res.msg);
            }else{
                alert(res.msg);
            }
        }
    });
    }else{
        alert("选择.xlsx的文件");
    }

}

function ex_usercase() {

    var pro_name = $("#project_id").find("option:selected").text()
    var pro_mo_name = $("#templatelist").find("option:selected").text()
    var pro_mo_id = $("#templatelist").find("option:selected").val()
    var case_name = $("#query_case_name").val()
    var interface_name = $("#query_interface_name").val()


    window.location.href="/interface/export_case?pro_name="+pro_name+
        "&pro_mo_name="+pro_mo_name+"&pro_mo_id="+pro_mo_id+"&case_name="+case_name+"&interface_name="+interface_name
}
