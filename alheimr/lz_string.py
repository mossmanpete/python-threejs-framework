
# Copyright 2014 Jens Páll Hafsteinsson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import re

class lz_string:

    def __init__(self):
        self.key_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    def compress(self, uncompressed):
        if uncompressed is None:
            return ''

        value = 0
        context_dictionary = {}
        context_dictionary_to_create = {}
        context_c = ''
        context_wc = ''
        context_w = ''
        context_enlarge_in = 2

        context_dict_size = 3
        context_num_bits = 2
        context_data_string = ''
        context_data_val = 0
        context_data_position = 0

        uncompressed = uncompressed

        for ii in range(len(uncompressed)):
            context_c = uncompressed[ii]

            if not context_c in context_dictionary:
                context_dictionary[context_c] = context_dict_size
                context_dict_size += 1
                context_dictionary_to_create[context_c] = True

            context_wc = context_w + context_c

            if context_wc in context_dictionary:
                context_w = context_wc
            else:
                if context_w in context_dictionary_to_create:
                    if ord(context_w[0]) < 256:
                        for i in range(context_num_bits):
                            context_data_val = (context_data_val << 1)

                            if context_data_position == 15:
                                context_data_position = 0
                                context_data_string += chr(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                        value = ord(context_w[0])

                        for i in range(8):
                            context_data_val = (context_data_val << 1) | (value & 1)

                            if context_data_position == 15:
                                context_data_position = 0
                                context_data_string += chr(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                            value = value >> 1
                    else:
                        value = 1
                   
                        for i in range(context_num_bits):
                            context_data_val = (context_data_val << 1) | value

                            if context_data_position == 15:
                                context_data_position = 0
                                context_data_string += chr(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                            value = 0

                        value = ord(context_w[0])

                        for i in range(16):
                            context_data_val = (context_data_val << 1) | (value & 1)

                            if context_data_position == 15:
                                context_data_position = 0
                                context_data_string += chr(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                            value = value >> 1

                    context_enlarge_in -= 1

                    if context_enlarge_in == 0:
                        context_enlarge_in = pow(2, context_num_bits)
                        context_num_bits += 1

                    context_dictionary_to_create.pop(context_w, None)
                    #del context_dictionary_to_create[context_w]
                else:
                    value = context_dictionary[context_w]

                    for i in range(context_num_bits):
                        context_data_val = (context_data_val << 1) | (value & 1)

                        if context_data_position == 15:
                            context_data_position = 0
                            context_data_string += chr(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = value >> 1

                context_enlarge_in -= 1

                if context_enlarge_in == 0:
                    context_enlarge_in = pow(2, context_num_bits)
                    context_num_bits += 1

                context_dictionary[context_wc] = context_dict_size
                context_dict_size += 1
                context_w = context_c
        if context_w != '':
            if context_w in context_dictionary_to_create:
                if ord(context_w[0]) < 256:
                    for i in range(context_num_bits):
                        context_data_val = (context_data_val << 1)

                        if context_data_position == 15:
                            context_data_position = 0
                            context_data_string += chr(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                    value = ord(context_w[0])

                    for i in range(8):
                        context_data_val = (context_data_val << 1) | (value & 1)

                        if context_data_position == 15:
                            context_data_position = 0
                            context_data_string += chr(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = value >> 1
                else:
                    value = 1

                    for i in range(context_num_bits):
                        context_data_val = (context_data_val << 1) | value

                        if context_data_position == 15:
                            context_data_position = 0
                            context_data_string += chr(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = 0

                    value = ord(context_w[0])

                    for i in range(16):
                        context_data_val = (context_data_val << 1) | (value & 1)

                        if context_data_position == 15:
                            context_data_position = 0
                            context_data_string += chr(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = value >> 1

                context_enlarge_in -= 1

                if context_enlarge_in == 0:
                    context_enlarge_in = pow(2, context_num_bits)
                    context_num_bits += 1

                context_dictionary_to_create.pop(context_w, None)
                #del context_dictionary_to_create[context_w]
            else:
                value = context_dictionary[context_w]

                for i in range(context_num_bits):
                    context_data_val = (context_data_val << 1) | (value & 1)

                    if context_data_position == 15:
                        context_data_position = 0
                        context_data_string += chr(context_data_val)
                        context_data_val = 0
                    else:
                        context_data_position += 1

                    value = value >> 1

            context_enlarge_in -= 1

            if context_enlarge_in == 0:
                context_enlarge_in = pow(2, context_num_bits)
                context_num_bits += 1

        value = 2

        for i in range(context_num_bits):
            context_data_val = (context_data_val << 1) | (value & 1)

            if context_data_position == 15:
                context_data_position = 0
                context_data_string += chr(context_data_val)
                context_data_val = 0
            else:
                context_data_position += 1

            value = value >> 1

        while True:
            context_data_val = (context_data_val << 1)

            if context_data_position == 15:
                context_data_string += chr(context_data_val)
                break
            else:
                context_data_position += 1

        return context_data_string

    
    def compress_to_base64(self, string):
        if string is None:
            return ''

        output = ''

        chr1 = float('NaN')
        chr2 = float('NaN')
        chr3 = float('NaN')
        enc1 = 0
        enc2 = 0
        enc3 = 0
        enc4 = 0

        i = 0

        string = self.compress(string)
        strlen = len(string)

        while i < (strlen * 2):
            if (i % 2) == 0:
                chr1 = ord(string[int(i / 2)]) >> 8
                chr2 = ord(string[int(i / 2)]) & 255

                if (i / 2) + 1 < strlen:
                    chr3 = ord(string[int((i / 2) + 1)]) >> 8
                else:
                    chr3 = float('NaN')
            else:
                chr1 = ord(string[int((i - 1) / 2)]) & 255
                if (i + 1) / 2 < strlen:
                    chr2 = ord(string[int((i + 1) / 2)]) >> 8
                    chr3 = ord(string[int((i + 1) / 2)]) & 255
                else:
                    chr2 = float('NaN')
                    chr3 = float('NaN')

            i += 3

            # python dont support bit operation with NaN like javascript
            enc1 = chr1 >> 2
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4 if not math.isnan(chr2) else 0)
            enc3 = ((chr2 & 15 if not math.isnan(chr2) else 0) << 2) | (chr3 >> 6 if not math.isnan(chr3) else 0)
            enc4 = (chr3 if not math.isnan(chr3) else 0) & 63

            if math.isnan(chr2):
                enc3 = 64
                enc4 = 64
            elif math.isnan(chr3):
                enc4 = 64

            output += self.key_str[enc1] + self.key_str[enc2] + self.key_str[enc3] + self.key_str[enc4]

        return output

    
    def compressToUTF16(self, string):

        if string is None:
            return ''

        output = ''
        c = 0
        current = 0
        status = 0

        string = self.compress(string)

        for i in range(len(string)):
            c = ord(string[i])

            if status == 0:
                status += 1
                output += chr(((c >> 1) + 32))
                current = (c & 1) << 14
            elif status == 1:
                status += 1
                output = chr(((current + (c >> 2)) + 32))
                current = (c & 3) << 13
            elif status == 2:
                status += 1
                output += chr(((current + (c >> 3)) + 32))
                current = (c & 7) << 12
            elif status == 3:
                status += 1
                output += chr(((current + (c >> 4)) + 32))
                current = (c & 15) << 11
            elif status == 4:
                status += 1
                output += chr(((current + (c >> 5)) + 32))
                current = (c & 31) << 10
            elif status == 5:
                status += 1
                output += chr(((current + (c >> 6)) + 32))
                current = (c & 63) << 9
            elif status == 6:
                status += 1
                output += chr(((current + (c >> 7)) + 32))
                current = (c & 127) << 8
            elif status == 7:
                status += 1
                output += chr(((current + (c >> 8)) + 32))
                current = (c & 255) << 7
            elif status == 8:
                status += 1
                output += chr(((current + (c >> 9)) + 32))
                current = (c & 511) << 6
            elif status == 9:
                status += 1
                output += chr(((current + (c >> 10)) + 32))
                current = (c & 1023) << 5
            elif status == 10:
                status += 1
                output += chr(((current + (c >> 11)) + 32))
                current = (c & 2047) << 4
            elif status == 11:
                status += 1
                output += chr(((current + (c >> 12)) + 32))
                current = (c & 4095) << 3
            elif status == 12:
                status += 1
                output += chr(((current + (c >> 13)) + 32))
                current = (c & 8191) << 2
            elif status == 13:
                status += 1
                output += chr(((current + (c >> 14)) + 32))
                current = (c & 16383) << 1
            elif status == 14:
                status += 1
                output += chr(((current + (c >> 15)) + 32))
                output += chr((c & 32767) + 32)

                status = 0

        output += chr(current + 32)

        return output

    
    def decompress(self, compressed):

        if (compressed is None) or (compressed == ''):
            return ''

        dictionary = {}
        enlarge_in = 4
        dict_size = 4
        num_bits = 3
        (entry, result, w, c) = ('', '', '', '')
        (i, nnext, bits, resb, maxpower, power) = (0, 0, 0, 0, 0, 0)

        data_string = compressed
        data_val = ord(compressed[0])
        data_position = 32768
        data_index = 1

        for i in range(3):
            #dictionary[i] = i
            dictionary[i] = ''

        bits = 0
        maxpower = pow(2, 2)
        power = 1

        while power != maxpower:
            resb = data_val & data_position
            data_position >>= 1

            if data_position == 0:
                data_position = 32768
                data_val = ord(data_string[data_index])
                data_index += 1

            bits |= (1 if resb > 0 else 0) * power
            power <<= 1

        nnext = bits
        if nnext == 0:
            bits = 0
            maxpower = pow(2, 8)
            power = 1

            while power != maxpower:
                resb = data_val & data_position
                data_position >>= 1

                if data_position == 0:
                    data_position = 32768
                    data_val = ord(data_string[data_index])
                    data_index += 1

                bits |= (1 if resb > 0 else 0) * power
                power <<= 1

            c = chr(bits)
        elif nnext == 1:
            bits = 0
            maxpower = pow(2, 16)
            power = 1

            while power != maxpower:
                resb = data_val & data_position
                data_position >>= 1

                if data_position == 0:
                    data_position = 32768
                    data_val = ord(data_string[data_index])
                    data_index += 1

                bits |= (1 if resb > 0 else 0) * power
                power <<= 1

            c = chr(bits)
        elif nnext == 2:
            return ''

        dictionary[3] = c
        result = c
        w = result

        while True:
            if data_index > len(data_string):
                return ''

            bits = 0
            maxpower = pow(2, num_bits)
            power = 1

            while power != maxpower:
                resb = data_val & data_position
                data_position >>= 1

                if data_position == 0:
                    data_position = 32768
                    data_val = ord(data_string[data_index])
                    data_index += 1

                bits |= (1 if resb > 0 else 0) * power
                power <<= 1

            c = bits

            if c == 0:
                bits = 0
                maxpower = pow(2, 8)
                power = 1

                while power != maxpower:
                    resb = data_val & data_position
                    data_position >>= 1

                    if data_position == 0:
                        data_position = 32768
                        data_val = ord(data_string[data_index])
                        data_index += 1

                    bits |= (1 if resb > 0 else 0) * power
                    power <<= 1

                dictionary[dict_size] = chr(bits)
                dict_size += 1
                c = dict_size - 1
                enlarge_in -= 1
            elif c == 1:
                bits = 0
                maxpower = pow(2, 16)
                power = 1

                while power != maxpower:
                    resb = data_val & data_position
                    data_position >>= 1

                    if data_position == 0:
                        data_position = 32768
                        data_val = ord(data_string[data_index])
                        data_index += 1

                    bits |= (1 if resb > 0 else 0) * power
                    power <<= 1

                dictionary[dict_size] = chr(bits)
                dict_size += 1
                c = dict_size - 1
                enlarge_in -= 1
            elif c == 2:
                return result

            if enlarge_in == 0:
                enlarge_in = pow(2, num_bits)
                num_bits += 1

            if c in dictionary:
                entry = dictionary[c]
            else:
                if c == dict_size:
                    entry = w + w[0]
                else:
                    return None

            result += entry

            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            enlarge_in -= 1

            w = entry

            if enlarge_in == 0:
                enlarge_in = pow(2, num_bits)
                num_bits += 1

                
    def decompres_from_base64(self, iinput):
        if iinput is None:
            return ''

        output = ""
        ol = 0
        output_ = ''

        i = 0

        iinput = re.sub(r'[^A-Za-z0-9\+\/\=]', '', iinput)

        while i < len(iinput):
            enc1 = self.key_str.index(iinput[i])
            i += 1
            enc2 = self.key_str.index(iinput[i])
            i += 1
            enc3 = self.key_str.index(iinput[i])
            i += 1
            enc4 = self.key_str.index(iinput[i])
            i += 1

            chr1 = (enc1 << 2) | (enc2 >> 4)
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2)
            chr3 = ((enc3 & 3) << 6) | enc4

            if (ol % 2) == 0:
                output_ = chr1 << 8

                if enc3 != 64:
                    output += chr(output_ | chr2)

                if enc4 != 64:
                    output_ = chr3 << 8
            else:
                output = output + chr(output_ | chr1)

                if enc3 != 64:
                    output_ = chr2 << 8

                if enc4 != 64:
                    output += chr(output_ | chr3)

            ol += 3

        return self.decompress(output)
