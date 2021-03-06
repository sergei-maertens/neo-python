# -*- coding:utf-8 -*-

from .StateBase import StateBase
from neo.IO.BinaryReader import BinaryReader
from neo.IO.MemoryStream import MemoryStream,StreamManager
import binascii
from autologging import logged

@logged
class SpentCoinState(StateBase):
    Output = None
    StartHeight = None
    EndHeight = None


    TransactionHash = None
    TransactionHeight = None
    Items = {}

    def __init__(self, hash=None, height = None, items = {}):
        self.TransactionHash = hash
        self.TransactionHeight = height
        self.Items = items

    @staticmethod
    def DeserializeFromDB(buffer):
        m = StreamManager.GetStream(buffer)
        reader = BinaryReader(m)
        spentcoin = SpentCoinState()
        spentcoin.Deserialize(reader)

        StreamManager.ReleaseStream(m)

        return spentcoin

    def Deserialize(self, reader):
        self.TransactionHash = reader.ReadUInt256()
        self.TransactionHeight = reader.ReadUInt32()

        count = reader.ReadVarInt()
#        self.__log.debug("num items %s " % count)
#        print("tx %s " % self.TransactionHash.decode('utf-8'))
#        txhash = binascii.hexlify(self.TransactionHash).decode('utf-8')

        items = {}
        for i in range(0, count):
            try:
                key = reader.ReadUInt16()
                val = reader.ReadUInt32()
                items[key] = val
            except Exception as e:
#                self.__log.debug("no could not read spent coin state items with length %s " % count)
#                self.__log.debug("DID Get items %s " % items)
                pass

        self.Items = items


    def Serialize(self, writer):

        super(SpentCoinState, self).Serialize(writer)

        writer.WriteUInt256(self.TransactionHash)
        writer.WriteUInt32(self.TransactionHeight)

        writer.WriteVarInt( len( self.Items))

        for key,val in self.Items.items():
            writer.WriteUInt16(key)
            writer.WriteUInt32(val)

