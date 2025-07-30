#-*- coding:utf-8 -*-
PS_STX = 0
PS_DATA = 1
PS_ESC = 2
MAX_PACKET_LEN = 1024
STX= 0x02
ETX = 0x03
ESC= 0x23
DLE=0x40
DEFAULT_CRC= 0xff

class packet_t(object):
    m_state = None
    m_pos = None
    m_crc = None
    m_completion_handler = None
    m_write_handler = None
    m_buffer = None

    def __init__(self, rx=None, tx=None):
        print('packet_t::__init__\n')
        self.m_buffer =bytearray(MAX_PACKET_LEN)
        self.m_completion_handler = rx
        self.m_write_handler = tx
        self.reset();

    def reset(self):
        self.m_pos   = 0
        self.m_state = PS_STX
        self.m_crc   = DEFAULT_CRC

    def write_bytes(self, ch):
        if ch <= ETX:
            self.m_write_handler(bytearray([ESC]))
            ch = ch^ DLE
            self.m_write_handler(bytearray([ch]))
        elif ch == ESC :
            self.m_write_handler(bytearray([ch]))
            self.m_write_handler(bytearray([ch]))
        else :
            self.m_write_handler(bytearray([ch]));

    def send_packet(self, buf,  len):
        if (self.m_write_handler == None):
            return;
        self.m_write_handler(bytearray([STX]));
        crc = DEFAULT_CRC
        i = 0;
        while len !=  0 :
            len -= 1
            # ch = struct.pack("B",buf[i])
            ch = buf[i]
            i += 1
            self.write_bytes(ch)
            crc ^= ch

        self.write_bytes(crc);
        self.m_write_handler(bytearray([ETX]))

    def add_data(self,  ch):
        if (self.m_pos >= MAX_PACKET_LEN):
            self.reset();
            return;

        self.m_crc ^= ch					# update crc
        self.m_buffer[self.m_pos] = ch;		#add ch to buffer
        self.m_pos+=1

    def add(self,  ch):
        if (ch == STX):
            self.reset();

        if self.m_state ==  PS_STX:
              self.m_state = PS_DATA
        elif self.m_state ==  PS_DATA:
                if (ch == ETX) :
                    self.m_state = PS_STX

                    if (self.m_pos >= 2 and self.m_crc == 0) :
                        self.m_pos-=1;
                        if (self.m_completion_handler) :
                            self.m_completion_handler(self.m_buffer, self.m_pos);
                        return;
                elif (ch == ESC):
                    self.m_state = PS_ESC;
                else:
                    if (ch < ETX):
                        self.reset();
                    else:
                        self.add_data(ch);
        elif self.m_state ==  PS_ESC:
                if (ch == ESC) :
                    self.m_state = PS_DATA;
                    self.add_data(ch);
                else:
                    self.m_state = PS_DATA;
                    self.add_data(ch ^ DLE);
        else :
            print ('')
