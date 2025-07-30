import os
import sys
import copy
import re
import json
import argparse
from natsort import natsorted

__version__ = 'v1.0.2'

class JsonToC():
    def __init__(self, args):
        self.args = args
        self.js_file = args.file
        self.output_file = args.output
        self.file_name = os.path.basename(self.js_file)[:-5]
        self.group_map = {}
        self.path_addr_dict = {}

    def read_js_file(self, js_file):
        with open(js_file) as jf:
            js_dict = json.load(jf)
            return js_dict

    def get_fields_msg(self, reg):
        fields_msg = {'set_value':False}
        for field in reg['Fields']:
            fields_msg['b_' + field['name']] = {
                    'set_bit': False,
                    'range': field['range'],
                    'access': field['access'],
                    }
        return fields_msg

    def get_reg_msg(self, reg_list):
        reg_msg = {}
        for reg in reg_list:
            if "Attribute" not in reg or reg["Attribute"] != "GROUP":
                reg_msg['r' + reg['RegName']] = self.get_fields_msg(reg)
                #print(reg['RegName'])
            elif "Attribute" in reg or reg["Attribute"] == "GROUP":
                #print('GROUP', reg['RegName'])
                group_reg_list = reg['group_reg']
                reg_msg.update(self.get_reg_msg(group_reg_list))
        return reg_msg

    def get_group_map(self, in_dict, pre_path = ''):
        path_list = []
        for k in in_dict:
            l1_path = os.path.join(pre_path, k)
            if isinstance(in_dict[k], list):
                for n,v in enumerate(in_dict[k]):
                    l2_path = os.path.join(l1_path, str(n))
                    if k == "registers":
                        if "Attribute" not in v or v["Attribute"] != "GROUP":
                            path_list.append(l2_path.strip("/"))
                    if k == "group_reg":
                        #if "group_reg" not in v:
                        if l1_path not in path_list:
                            path_list.append(l1_path)
                            self.group_map[l1_path] = []
                        self.group_map[l1_path].append(l2_path.strip("/"))
                        #path_list.append(l2_path.strip("/"))
                    path_list.extend(self.get_group_map(v, l2_path))
        return path_list

    def get_dpath(self, in_dict, pre_path = ''):
        path_list = []
        for k in in_dict:
            l1_path = os.path.join(pre_path, k)
            if isinstance(in_dict[k], list):
                for n,v in enumerate(in_dict[k]):
                    l2_path = os.path.join(l1_path, str(n))
                    if k == "registers":
                        if "Attribute" not in v or v["Attribute"] != "GROUP":
                            path_list.append(l2_path.strip("/"))
                    if k == "group_reg":
                        if "group_reg" not in v:
                            if l1_path not in path_list:
                                path_list.append(l1_path)
                        else:
                            pass
                            #path_list.append(l1_path)
                        continue
                    path_list.extend(self.get_dpath(v, l2_path))
        return path_list

    def get_delem(self, in_dict, dpath, key = ''):
        path = dpath.strip('/').split('/')
        msg = ''
        for i in path:
            if i.isdigit():
                msg += "["  + i + "]"
            else:
                msg += "[\'"  + i + "\']"
        if key != '':
            msg += "[\'"  + key + "\']"
        return eval("in_dict" + msg)

    def get_addr(self, dpath):
        return self.tmp_path_dict[dpath]

    def parse_dict(self, in_dict, tpath = ''):
        if 'RegName' in in_dict and 'group_reg' not in in_dict:
            self.parse_reg(in_dict, tpath)
            return 0
        if 'RegName' in in_dict and  'group_reg' in in_dict:
            self.parse_group(in_dict, [], tpath)
            return 0
        if "base_addr" in in_dict:
            self.base_addr = int(in_dict['base_addr'], 16)
            self.history_addr = int(in_dict['base_addr'], 16)
            self.bit_num = int(in_dict['d_width'])
        for k, v in in_dict.items():
            if isinstance(v, (str,int)):
                pass
                #print(k,v)
            else:
                pass
                #print(k,type(v))
            if isinstance(v, list):
                if not tpath:
                    tpath = k
                else:
                    tpath += '/' +k
                for j in range(len(v)):
                    tmp = copy.deepcopy(tpath)
                    t = v[j]
                    if isinstance(t, dict):
                        self.parse_dict(t, tmp+'/'+str(j))

    def parse_reg(self, in_dict, tpath = ''):
        # name 
        name = in_dict['RegName']
        name = name.upper()

        # des
        des = ''
        if 'Description' in in_dict:
            des = in_dict['Description']

        # addr
        if 'Offset' in in_dict:
            offset = int(in_dict['Offset'], 16)
            st_addr =  hex(self.base_addr + offset)
            self.history_addr = self.base_addr + offset
        elif 'Step' in in_dict:
            step = int(in_dict['Step'], 16)
            st_addr =  hex(self.history_addr + step)
            self.history_addr = self.history_addr + step

        self.all_reg_msg[tpath + '##' + name] = {
            'name':name,
            'addr':st_addr,
                }
        #for field in in_dict['Fields']:
        #    self.all_reg_msg[name]['b_' + field['name']] = {
        #            'set_bit': False,
        #            'range': field['range'],
        #            'access': field['access'],
        #            }
        if tpath not in self.tmp_path_dict:
            self.tmp_path_dict[tpath] = st_addr


    def parse_group_reg(self, in_dict, index = [], tpath = ''):
        # 组后缀
        if index != []:
            d = "||".join(index)

        # name 
        name = in_dict['RegName'] + "||" + str(d)
        name = name.upper()

        # des
        des = ''
        if 'Description' in in_dict:
            des = in_dict['Description']

        # addr
        if 'Offset' in in_dict:
            offset = int(in_dict['Offset'], 16)
            st_addr =  hex(self.group_offset + offset)
            self.history_addr = self.group_offset + offset
        elif 'Step' in in_dict:
            step = int(in_dict['Step'], 16)
            st_addr =  hex(self.history_addr + step)
            self.history_addr = self.history_addr + step

        self.all_reg_msg[tpath + '##' + name] = {
            'name':name,
            'addr':st_addr,
                }
        #print(in_dict)

        #for field in in_dict['Fields']:
        #    self.all_reg_msg[name]['b_' + field['name']] = {
        #            'set_bit': False,
        #            'range': field['range'],
        #            'access': field['access'],
        #            }

        #print(tpath, name, st_addr)
        if tpath not in self.group_reg_dict:
            self.group_reg_dict[tpath] = []
        self.group_reg_dict[tpath].append({
            "name":name,
            "addr":st_addr,
            })
        if tpath not in self.tmp_path_dict:
            self.tmp_path_dict[tpath] = st_addr

    def parse_group_group(self, in_dict, index = [], tpath = ''):
        depth = in_dict['depth']
        if "Offset" in in_dict:
            offset = int(in_dict['Offset'], 16)
            self.group_offset =  self.group_offset + offset
        elif "Step" in in_dict:
            step = int(in_dict['Step'], 16)
            self.group_offset =  self.history_addr + step
        for d in range(depth):
            if d >= 1:
                if 'Offset' in in_dict['group_reg'][0] and \
                        int(in_dict['group_reg'][0]['Offset'], 16) == 0:
                    self.group_offset =  self.history_addr + int(self.bit_num/8)
            for j in range(len(in_dict['group_reg'])):
                #print(g['RegName'])
                g = in_dict['group_reg'][j]
                tmp = copy.deepcopy(index)
                tmp.append(str(d))
                tmp_path = copy.deepcopy(tpath)
                if 'RegName' in g and 'group_reg' not in g:
                    self.parse_group_reg(g, tmp, tmp_path + '/group_reg/' + str(j))
                if 'RegName' in g and  'group_reg' in g:
                    self.parse_group_group(g, tmp, tmp_path + '/group_reg/' + str(j))

    def parse_group(self, in_dict, index = [], tpath = ''):
        depth = in_dict['depth']
        if "Offset" in in_dict:
            offset = int(in_dict['Offset'], 16)
            self.group_offset =  self.base_addr + offset
        elif "Step" in in_dict:
            step = int(in_dict['Step'], 16)
            self.group_offset =  self.history_addr + step
        for d in range(depth):
            if d >= 1:
                if 'Offset' in in_dict['group_reg'][0]:
                    if int(in_dict['group_reg'][0]['Offset'], 16) == 0:
                        self.group_offset =  self.history_addr + int(self.bit_num/8)
                    else:
                        self.group_offset =  self.history_addr + int(in_dict['group_reg'][0]['Offset'], 16)
            for j in range(len(in_dict['group_reg'])):
                g = in_dict['group_reg'][j]
                #print(g['RegName'])
                tmp = copy.deepcopy(index)
                tmp.append(str(d))
                tmp_path = copy.deepcopy(tpath)
                if 'RegName' in g and 'group_reg' not in g:
                    self.parse_group_reg(g, tmp, tmp_path + '/group_reg/' + str(j))
                if 'RegName' in g and  'group_reg' in g:
                    self.parse_group_group(g, tmp, tmp_path + '/group_reg/' + str(j))

    def relist(self, in_list):
        new_list = []
        list_len = len(in_list)
        for i in range(list_len):
            for j in range(i, list_len):
                if int(in_list[i]['addr'], 16) >= int(in_list[j]['addr'], 16):
                    in_list[i], in_list[j] = in_list[j], in_list[i]

    def parse_js_file(self, js_file):
        ###################
        self.js_file = js_file
        self.all_reg_msg = {}
        self.base_addr = ''
        self.group_addr = ''
        self.bit_num = 32
        self.group_reg_dict = {}
        self.tmp_path_dict = {}
        ###################

        self.js_dict = self.read_js_file(js_file)
        self.parse_dict(self.js_dict)

        #return self.all_reg_msg
        #self.all_reg_msg = sorted(self.all_reg_msg.items(), key=lambda x:x[0])

    def create_group_struct(self, i, group_struct_name):
        c_data = 'struct ' + group_struct_name + ' {\n'
        reserved_count = 0
        for j in self.group_map[i]:
            #print(j)
            name = self.get_delem(self.js_dict, j, key = 'RegName' )
            elem = self.get_delem(self.js_dict, j)
            if name.upper() == 'RESERVED':
                addr = self.get_addr(j)
                self.path_addr_dict[j] = addr
                c_data += '    unsigned r' + name.upper() + str(reserved_count) + \
                        '; //' + addr + '\n'
                reserved_count += 1
                continue
            if 'group_reg' in elem:
                group_name = elem['RegName']
                group_depth = elem['depth']
                #print(">>>>>>>>", group_name, group_depth)
                sub_group_struct_name = 'g' + group_name.upper()
                c_data = self.create_group_struct(os.path.join(j, 'group_reg'), \
                        sub_group_struct_name)  + c_data
                c_data += '    struct g' + group_name.upper() + ' ' + group_name.lower() + \
                        '[' + str(group_depth) + '];\n'
            else:
                addr = self.get_addr(j)
                self.path_addr_dict[j] = addr
                c_data += '    unsigned r' + name.upper() + '; //' + addr + '\n'
        c_data +=  '};\n\n'
        return c_data
 
    def get_path_start_addr(self, dpath):
        start_addr = ''
        for path in natsorted(self.all_reg_msg.keys()):
            msg = self.all_reg_msg[path]
            addr = msg['addr']
            if path.startswith(dpath):
                start_addr = addr
                break
        return start_addr

    def get_path_end_addr(self, dpath):
        end_addr = ''
        start = 0
        for path in natsorted(self.all_reg_msg.keys()):
            msg = self.all_reg_msg[path]
            addr = msg['addr']
            if path.startswith(dpath):
                end_addr = addr
                start = 1
            if start and not path.startswith(dpath):
                break
        return end_addr

    def create_main_struct(self):
        #print(self.file_name)
        c_data_list = []
        c_data = 'struct ' + self.file_name + ' {\n'
        pre_dpath = ''
        reseve_count = 0
        for i in self.js_dpath:
            if i.endswith('group_reg'):

                group_path = '/'.join(i.split('/')[:-1])
                group_name = self.get_delem(self.js_dict, group_path, key = 'RegName' )
                group_depth = self.get_delem(self.js_dict, group_path, key = 'depth' )
                #print(">>>>>>>>", group_name, group_depth)
                group_struct_name = 'g' + group_name.upper()
                if pre_dpath != '':
                    pre_end_addr = self.get_path_end_addr(pre_dpath)
                    now_start_addr = self.get_path_start_addr(i)
                    #print(i)
                    #print(group_name)
                    #print(pre_end_addr)
                    #print(now_start_addr)
                    addr_diff = int(now_start_addr, 16) - int(pre_end_addr, 16)  -4
                    if addr_diff > 0:
                        bytes_count = int(addr_diff/4)
                        #print(addr_diff)
                        #print(bytes_count)
                        c_data += '    unsigned rRESV' + str(reseve_count) + '[ ' + \
                                str(bytes_count) + ' ];\n'
                        reseve_count += 1
                c_data += '    struct g' + group_name.upper() + ' ' + group_name.lower() + \
                        '[' + str(group_depth) + '];\n'
                c_data_list.append(self.create_group_struct(i, group_struct_name))
                #sys.exit()
            else:
                addr = self.get_addr(i)
                self.path_addr_dict[i] = addr
                name = self.get_delem(self.js_dict, i, key = 'RegName' )
                #print(name, "(" + addr + ")")
                if pre_dpath != '':
                    pre_end_addr = self.get_path_end_addr(pre_dpath)
                    now_start_addr = self.get_path_start_addr(i)
                    #print(pre_end_addr)
                    #print(now_start_addr)
                    addr_diff = int(now_start_addr, 16) - int(pre_end_addr, 16)  -4
                    if addr_diff > 0:
                        bytes_count = int(addr_diff/4)
                        #print(addr_diff)
                        #print(bytes_count)
                        c_data += '    unsigned rRESV' + str(reseve_count) + '[ ' + \
                                str(bytes_count) + ' ];\n'
                        reseve_count += 1
                c_data += '    unsigned r' + name.upper() + '; //' + addr + '\n'
            pre_dpath = i
        c_data +=  '};\n\n'
        c_data_list.append(c_data)
        return c_data_list

    def range_to_hex(self, start, end):
        '''
        [8:0] 应该输出0x1ff  (二进制9个1)
        [13:0] 应该输出0x3fff (二进制14个1)
        '''
        #print(start, end)
        width = abs(start - end) + 1
        all_ones_binary = (1 << width) - 1
        hex_str = hex(all_ones_binary)
        return hex_str

    def create_field_data(self, field):
        fname = field['name']
        frange = field['range']
        faccess = field['access']
        fdesc = field['description']
        fdesc = fdesc.replace('；', ';').replace('。', ';')\
                .replace(';', ';\n             ')
        freset = field['reset_value']

        scope = frange.strip("[]").split(":")
        end = int(scope[0])
        start = int(scope[-1])

        c_data = '    /* name: f_' + fname.upper() + ' */\n'
        c_data += '    /* desc: ' + fdesc + ' */\n'
        c_data += '    /* range: ' + frange + ' */\n'
        c_data += '    /* access: ' + faccess + ' */\n'
        c_data += '    /* reset_value: ' + freset + ' */\n'
        c_data += '    #define b_' + fname.upper() + '    ( ' + str(start) +' ) \n'
        c_data += '    #define m_' + fname.upper() + '    ( ' +\
                self.range_to_hex(start, end) + ' << b_' + fname.upper() + ' )\n\n'
        return c_data

    def create_fields(self):
        c_data_list = []
        for i in self.js_dpath:
            #print(i)
            if i.endswith('group_reg'):

                group_path = '/'.join(i.split('/')[:-1])
                group_name = self.get_delem(self.js_dict, group_path, key = 'RegName' )
                group_depth = self.get_delem(self.js_dict, group_path, key = 'depth' )
                for j in self.group_map[i]:
                    name = self.get_delem(self.js_dict, j, key = 'RegName' )
                    elem = self.get_delem(self.js_dict, j)
                    if 'group_reg' in elem:
                        continue
                    #print(j)
                    if name.upper() == 'RESERVED':
                        continue
                    addr = self.get_addr(j)
                    fields = self.get_delem(self.js_dict, j, key = 'Fields' )
                    #c_data_list.append('/* r' + name + ' START */\n')
                    c_data_list.append('/* r' + name + ' */\n')
                    for field in fields:
                        c_data_list.append(self.create_field_data(field))
            else:
                addr = self.get_addr(i)
                name = self.get_delem(self.js_dict, i, key = 'RegName' )
                #print(name, "(" + addr + ")")
                if name.upper() == 'RESERVED':
                    continue
                fields = self.get_delem(self.js_dict, i, key = 'Fields' )
                #print(fields)
                #c_data_list.append('/* r' + name + ' START */\n')
                c_data_list.append('/* r' + name + ' */\n')
                for field in fields:
                    c_data_list.append(self.create_field_data(field))
                #c_data_list[-1] = c_data_list[-1][:-1]
                #c_data_list.append('/* r' + name + ' END */\n\n')

        return c_data_list

    def main(self):
        file_msg = os.path.basename(self.js_file).split(".json")[0]
        self.js_dict = self.read_js_file(self.js_file)
        self.parse_js_file(self.js_file)

        self.get_group_map(self.js_dict)
        self.js_dpath = self.get_dpath(self.js_dict)
        c_data_list = []
        c_data_list.append("#ifndef __" + self.file_name.upper() + "_H__\n" + \
                "#define __" + self.file_name.upper() + "_H__\n\n")

        c_data_list.extend(self.create_main_struct())

        c_data_list.extend(self.create_fields())

        c_data_list.append("#endif\n")
        if self.output_file:
            output_dir = os.path.dirname(self.output_file)
            if not os.path.exists(output_dir):
                os.system('mkdir -p ' + output_dir)
            with open(self.output_file , 'w') as fd:
                for data_block in c_data_list:
                    fd.write(data_block)
            print("\n\tCreate " + self.output_file + " success")
        else:
            with open(self.file_name + '.h' , 'w') as fd:
                for data_block in c_data_list:
                    fd.write(data_block)
            print("\n\tCreate " + self.file_name + '.h' + " success")

def main():
    parser = argparse.ArgumentParser(description = "json转头文件")
    parser.add_argument('-f', '--file', dest='file', metavar='file',
            help='指定json文件')
    parser.add_argument('-o', '--output', dest='output', metavar='output',
            help='指定输出文件, 默认为当前目录下的同名.h')
    parser.add_argument('-v', dest='version', action='version', version=__version__,
            help='显示版本信息')

    args = parser.parse_args()

    #print(args)

    jt = JsonToC(args)
    jt.main()

if __name__ == "__main__":
    main()
