#-*- coding:utf-8 -*-
#######################################################################
#
#######################################################################
class command_t:
    __cmd = 0;
    __len = 0;
    __data = [0 for i in range(256)]

    def __init__(self, match_data):
      cmd = match_data[0]
      len = match_data[1]
      data = match_data[2:]

    def clikeBuffer(self):
        b = list()
        b.append(self.cmd)
        b.append(self.len)
        b = b+ self.data
        return b
