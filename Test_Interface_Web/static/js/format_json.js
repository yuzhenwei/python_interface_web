/**
 * JSON格式化
 */
    var APP=function(){

        var format=function(json){

            var reg=null,

                result='';

                pad=0,

                PADDING='    ';

            //if (typeof json !== 'string') {
            //
            //    json = JSON.stringify(json);
            //
            //} else {
            //
            //    json = JSON.parse(json);
            //
            //    json = JSON.stringify(json);
            //
            //}

            if (typeof json == 'string') {

                json = JSON.stringify(json);
                json = JSON.parse(json);

            } else {
                json = JSON.stringify(json);
            }
            // 在大括号前后添加换行

            reg = /([\{\}])/g;

            json = json.replace(reg, '\r\n$1\r\n');

            // 中括号前后添加换行

            reg = /([\[\]])/g;

            json = json.replace(reg, '\r\n$1\r\n');

            // 逗号后面添加换行

            reg = /(\,)/g;

            json = json.replace(reg, '$1\r\n');

            // 去除多余的换行

            reg = /(\r\n\r\n)/g;

            json = json.replace(reg, '\r\n');

            // 逗号前面的换行去掉

            reg = /\r\n\,/g;

            json = json.replace(reg, ',');

            //冒号前面缩进

            reg = /\:/g;

            json = json.replace(reg, ': ');

            //对json按照换行进行切分然后处理每一个小块

            $.each(json.split('\r\n'), function(index, node) {

                var i = 0,

                    indent = 0,

                    padding = '';

                //这里遇到{、[时缩进等级加1，遇到}、]时缩进等级减1，没遇到时缩进等级不变

                if (node.match(/\{$/) || node.match(/\[$/)) {

                    indent = 1;

                } else if (node.match(/\}/) || node.match(/\]/)) {

                    if (pad !== 0) {

                        pad -= 1;

                    }

                } else {

                    indent = 0;

                }

                   //padding保存实际的缩进

                for (i = 0; i < pad; i++) {

                    padding += PADDING;

                }

                //添加代码高亮

                node = node.replace(/([\{\}])/g,"<span class='ObjectBrace'>$1</span>");

                node = node.replace(/([\[\]])/g,"<span class='ArrayBrace'>$1</span>");

                node = node.replace(/(\".*\")(\:)(.*)(\,)?/g,"<span class='PropertyName'>$1</span>$2$3$4");

                node = node.replace(/\"([^"]*)\"(\,)?$/g,"<span class='String'>\"$1\"</span><span class='Comma'>$2</span>");

                node = node.replace(/(-?\d+)(\,)?$/g,"<span class='Number'>$1</span><span class='Comma'>$2</span>");

                result += padding + node + '<br>';

                pad += indent;

            });

            return result;

        };

        return {

            "format":format,

        };

    }();
