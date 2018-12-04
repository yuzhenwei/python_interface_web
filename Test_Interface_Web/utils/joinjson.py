"""
读取接口返回指定参数
"""

class JoinPar():

    def __init__(self):
        self.key_info={}

    #递归查找value值
    def print_json_key(self,input_json,key):
        key_value=''
        if isinstance(input_json,dict):
            for json_result in input_json.values():
                if key in input_json.keys():
                    key_value = input_json.get(key)
                else:
                    self.print_json_key(json_result,key)
        elif isinstance(input_json,list):
            for json_array in input_json:
                self.print_json_key(json_array,key)
        if key_value!='':
            self.key_info[key]=key_value

    def key_replace_value(self,input_json,key,key_value):
        if isinstance(input_json, dict):
            for json_result in input_json.values():
                if key in input_json.keys():
                    input_json[key]= key_value
                    #return {key:input_json[key]}
                else:
                    self.key_replace_value(json_result, key,key_value)
        elif isinstance(input_json, list):
            for json_array in input_json:
                self.key_replace_value(json_array,key,key_value)

        return input_json;


    def str_replace(self,case_paraminfo,keys,values):
        #拼接要替换的值key:values
        #key_val和key_val2 是两种情况一种，key_val在外层的，key_val2是内层加反斜杠的
        key_val = '"{keys}":"{values}"'.format(keys=keys, values=values)
        key_val2 = '\\"{keys}\\":\\"{values}\\"'.format(keys=keys, values=values)
        sear_key = '"%s":"$$"' % keys
        sear_key2 = '\\"%s\\":\\"$$\\"' % keys
        #print("---",sear_key, key_val)
        if(sear_key in case_paraminfo):

            case_paraminfo = case_paraminfo.replace(sear_key, key_val)
        elif(sear_key2 in case_paraminfo):
            case_paraminfo = case_paraminfo.replace(sear_key2, key_val2)
        #case_paraminfo.replace('\"',"'")
        #print("---被替换后的值",case_paraminfo)
        return case_paraminfo;

# if __name__=="__main__":
#     str={'code': 200, 'message': 'OK', 'result': {'pageSize': 20, 'index': 1, 'totalItem': 1, 'totalPage': 1, 'startRow': 0, 'endRow': 1, 'rows': [{'companyCode': '7LK_GZ', 'goodsName': '云植 感冒止咳颗粒 云南植物 10g*6袋', 'skuCode': '402010050', 'partnerCode': '561', 'partnerName': '广东恒大医药有限公司', 'taxPrice': 6.5, 'inTax': 17.0, 'isMainPartner': 1, 'busiCategory': '中成药', 'otherBusiCategory': '123', 'companyType': '经营类', 'productionArea': '中药材,中药饮片,中成药,化学药制剂,抗生素制剂,生物制品（除疫苗）,生化药品', 'productionAreaOther': '', 'goodsBaseClass': 1}]}}
#     jp=JoinPar()
#     aa = jp.key_replace_value(str,"inTax",3)
#     print(aa)
