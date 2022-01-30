#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 11:23:50 2019

@author: nmp
"""

import socket
import struct
from antidotedb.proto import *

class AntidoteException(Exception):
    pass


#---------------------------------------------------------------------------------
# Classes that represent data objects stores in Antidote
#---------------------------------------------------------------------------------
class Counter :
    """ Represents a counter object
    """
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def value( self) :
        return self.val

    def incOp( self, val) :
        return Counter.IncOp( self.key, val)

    def incKeyOp( val, key) :
        return Counter.IncOp( key, val)

    def __repr__( self):
        return self.key.data_type_name + ' { val : ' + str(self.val) + '}'

    class IncOp:
        def __init__(self, key, val, data_type = None):
            self.val = val
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.counterop.inc = self.val

    def resetOp( self) :
        return Counter.ResetOp( self.key)

    # def resetKeyOp(key) :
    #     return Counter.ResetOp( key)

    class ResetOp:
        def __init__(self, key, data_type = None):
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.resetop.SetInParent()


class Flag :
    """ Represents a register object
    """
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def value( self) :
        return self.val

    def enableOp( self) :
        return Flag.UpdateOp( self.key, True)

    # def enableKeyOp( key) :
    #     return Flag.UpdateOp( key, True)

    def disableOp( self) :
        return Flag.UpdateOp( self.key, False)

    # def disableKeyOp( key) :
    #     return Flag.UpdateOp( key, False)

    # def updateKeyOp( val, key) :
    #     return Flag.UpdateOp( key, val)

    class UpdateOp:
        def __init__(self, key, val, data_type = None):
            self.val = val
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.flagop.value = self.val

    def resetOp( self) :
        return Flag.ResetOp( self.key)

    # def resetKeyOp(key) :
    #     return Flag.ResetOp( key)

    class ResetOp:
        def __init__(self, key, data_type = None):
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.resetop.SetInParent()


    def __repr__( self):
        return self.key.data_type_name + ' { val : ' + str(self.val) + '}'


class Register :
    """ Represents a register object
    """
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def value( self) :
        return self.val

    def assignOp( self, val) :
        return Register.AssignOp( self.key, val)

    # def assignKeyOp( val, key) :
    #     return Register.AssignOp( key, val)

    class AssignOp:
        def __init__(self, key, val, data_type = None):
            self.val = val
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.regop.value = self.val

    def resetOp( self) :
        return Register.ResetOp( self.key)

    # def resetKeyOp(key) :
    #     return Register.ResetOp( key)

    class ResetOp:
        def __init__(self, key, data_type = None):
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.resetop.SetInParent()

    def __repr__( self):
        return self.key.data_type_name + ' { val : ' + str(self.val) + '}'


class MVRegister :
    """ Represents a MV register object
    """
    def __init__(self, key, vals):
        self.key = key
        self.vals = vals

    def values( self) :
        return self.vals

    def assignOp( self, val) :
        return MVRegister.AssignOp( self.key, val)

    def assignKeyOp( val, key) :
        return MVRegister.AssignOp( key, val)

    class AssignOp:
        def __init__(self, key, val, data_type = None):
            self.val = val
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.regop.value = self.val

    def resetOp( self) :
        return MVRegister.ResetOp( self.key)

    # def resetKeyOp(key) :
    #     return MVRegister.ResetOp( key)

    class ResetOp:
        def __init__(self, key, data_type = None):
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.resetop.SetInParent()

    def __repr__( self):
        return self.key.data_type_name + ' { val : ' + str(self.vals) + '}'

class Set :
    """ Represents a Set
    """
    def __init__(self, key, vals):
        self.key = key
        self.vals = vals

    def values( self) :
        return self.vals

    def addOp( self, val) :
        return Set.AddOp( self.key, val)

    # def addKeyOp( val, key) :
    #     return Set.AddOp( key, val)

    class AddOp:
        def __init__(self, key, val, data_type = None):
            self.val = val
            self.key = key
            if type( self.val) != list:
                self.val = [self.val]
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.setop.optype = ApbSetUpdate.SetOpType.Value('ADD')
            op.setop.adds.extend( self.val)

    def removeOp( self, val) :
        return Set.RemoveOp( self.key, val)

    # def removeKeyOp( val, key) :
    #     return Set.RemoveOp( key, val)

    class RemoveOp:
        def __init__(self, key, val, data_type = None):
            self.val = val
            self.key = key
            if type( self.val) != list:
                self.val = [self.val]
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.setop.optype = ApbSetUpdate.SetOpType.Value('REMOVE')
            op.setop.rems.extend( self.val)

    def resetOp( self) :
        return Set.ResetOp( self.key)

    # def resetKeyOp(key) :
    #     return Set.ResetOp( key)

    class ResetOp:
        def __init__(self, key, data_type = None):
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.resetop.SetInParent()

    def __repr__( self):
        return self.key.data_type_name + ' { val : ' + str(self.vals) + '}'

class Map :
    """ Represents a Set
    """
    def __init__(self, key, vals):
        self.key = key
        self.vals = vals

    def values( self) :
        return self.vals

    def updateOp( self, upds) :
        return Map.UpdateOp( self.key, upds)

    # def updateKeyOp( upds, key) :
    #     return Map.UpdateOp( key, upds)

    class UpdateOp:
        def __init__(self, key, upds, data_type = None):
            self.upds = upds
            self.key = key
            if type( self.upds) != list:
                self.upds = [self.upds]
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, opbase) :
            for upd in self.upds :
                op = opbase.mapop.updates.add()
                op.key.key = upd.getKey()
                op.key.type = upd.getType()
                upd.recordOp( op.update)

    def removeOp( self, keys) :
        return Map.RemoveOp( self.key, keys)

    # def removeKeyOp( upds, keys) :
    #     return Map.RemoveOp( key, keys)

    class RemoveOp:
        def __init__(self, key, keys, data_type = None):
            self.keys = keys
            self.key = key
            if type( self.keys) != list:
                self.keys = [self.keys]
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, opbase) :
            for opkey in self.keys :
                op = opbase.mapop.removedKeys.add()
                op.key = opkey.key
                op.type = opkey.data_type

    def resetOp( self) :
        return Map.ResetOp( self.key)

    # def resetKeyOp(key) :
    #     return Map.ResetOp( key)

    class ResetOp:
        def __init__(self, key, data_type = None):
            self.key = key
            if data_type == None :
                self.data_type = key.data_type
            else:
                self.data_type = CRDT_type.Value(data_type)

        def getType( self) :
            return self.data_type

        def getKey( self) :
            return self.key

        def recordOp( self, op) :
            op.resetop.SetInParent()

    def __repr__( self):
        return self.key.data_type_name + str(self.vals)


#---------------------------------------------------------------------------------
# Utilitiles
#---------------------------------------------------------------------------------
class ServerAddress:
    """ Records the information about a server endpoint, consisting of
    IP address and port"""
    def __init__(self, address, port):
        """ Address should be a string and port an integer """
        self.address = address
        self.port = port

    def getAddress( self) :
        """ Returns the address as a tuple """
        return (self.address, self.port)

#---------------------------------------------------------------------------------
# Antidote client main classes
#---------------------------------------------------------------------------------
class Key :
    """" Class for an interative transaction """
    def __init__(self, bucket, key, data_type):
        if type(bucket) == bytes :
            self.bucket = bucket
        else:
            self.bucket = bytes(bucket, 'utf-8')
        if type(key) == bytes :
            self.key = key
        else:
            self.key = bytes(key, 'utf-8')
        if type(data_type) == int :
            self.data_type = data_type
            self.data_type_name = CRDT_type.Name(data_type)
        else :
            self.data_type = CRDT_type.Value(data_type)
            self.data_type_name = data_type

class StaticTransaction :
    """" Class for an interative transaction """
    def __init__(self, clt, red_blue, min_snapshot):
        self.antidoteClient = clt
        self.red_blue = red_blue
        self.min_snapshot = min_snapshot


    def read_objects_raw( self, keys) :
        """ Execute one or more read object operations
        """
        op = ApbStaticReadObjects()
        op.transaction.properties.read_write = 1
        op.transaction.properties.red_blue = self.red_blue
        if self.min_snapshot is not None:
            op.transaction.timestamp = self.min_snapshot
        if type( keys) != list :
            keys= [keys]
        for key in keys :
            obj = op.objects.add()
            obj.key = key.key
            obj.bucket = key.bucket
            obj.type = key.data_type
        self.antidoteClient.sendMessageStaticReadObjects( op)
        res = self.antidoteClient.recvMessageStaticReadObjectsResp()
        return res

    def read_objects( self, keys) :
        """ Execute one or more read object operations
        """
        op = ApbStaticReadObjects()
        op.transaction.properties.read_write = 1
        op.transaction.properties.red_blue = self.red_blue
        if self.min_snapshot is not None:
            op.transaction.timestamp = self.min_snapshot
        if type( keys) != list :
            keys= [keys]
        for key in keys :
            obj = op.objects.add()
            obj.key = key.key
            obj.bucket = key.bucket
            obj.type = key.data_type
        self.antidoteClient.sendMessageStaticReadObjects( op)
        res = self.antidoteClient.recvMessageStaticReadObjectsResp()
        if res.objects.success == True:
            reply = []
            for i in range(len(keys)):
                key = keys[i]
                val = res.objects.objects[i]
                reply.append( AntidoteClient.decodeObjectReply( key, val))
            return reply
        else:
            return None

    def update_objects( self, updates) :
        """ Execute one or more read object operations
        """
        op = ApbStaticUpdateObjects()
        op.transaction.properties.read_write = 2
        op.transaction.properties.red_blue = self.red_blue
        if self.min_snapshot is not None:
            op.transaction.timestamp = self.min_snapshot
        if type( updates) != list :
            updates = [updates]
        for upd in updates :
            opupd = op.updates.add()
            key = upd.getKey()
            opupd.boundobject.key = key.key
            opupd.boundobject.bucket = key.bucket
            opupd.boundobject.type = key.data_type
            upd.recordOp( opupd.operation)
        #print(op)
        self.antidoteClient.sendMessageStaticUpdateObjects( op)
        res = self.antidoteClient.recvMessageCommitResp()
        if res.success == True:
            self.antidoteClient.last_commit = res.commit_time
        return res.success == True




class InteractiveTransaction :
    """" Class for an interative transaction """
    def __init__(self, clt, txDescriptor):
        self.antidoteClient = clt
        self.txDescriptor = txDescriptor


    def read_objects_raw( self, keys) :
        """ Execute one or more read object operations
        """
        op = ApbReadObjects()
        op.transaction_descriptor = self.txDescriptor
        if type( keys) != list :
            keys= [keys]
        for key in keys :
            obj = op.boundobjects.add()
            obj.key = key.key
            obj.bucket = key.bucket
            obj.type = key.data_type
        self.antidoteClient.sendMessageReadObjects( op)
        res = self.antidoteClient.recvMessageReadObjectsResp()
        return res

    def read_objects( self, keys) :
        """ Execute one or more read object operations
        """
        op = ApbReadObjects()
        op.transaction_descriptor = self.txDescriptor
        if type( keys) != list :
            keys= [keys]
        for key in keys :
            obj = op.boundobjects.add()
            obj.key = key.key
            obj.bucket = key.bucket
            obj.type = key.data_type
        self.antidoteClient.sendMessageReadObjects( op)
        res = self.antidoteClient.recvMessageReadObjectsResp()
        if res.success == True:
            reply = []
            for i in range(len(keys)):
                key = keys[i]
                val = res.objects[i]
                reply.append( AntidoteClient.decodeObjectReply( key, val))
            return reply
        else:
            return None

    def update_objects( self, updates) :
        """ Execute one or more read object operations
        """
        op = ApbUpdateObjects()
        op.transaction_descriptor = self.txDescriptor
        if type( updates) != list :
            updates = [updates]
        for upd in updates :
            opupd = op.updates.add()
            key = upd.getKey()
            opupd.boundobject.key = key.key
            opupd.boundobject.bucket = key.bucket
            opupd.boundobject.type = key.data_type
            upd.recordOp( opupd.operation)
        self.antidoteClient.sendMessageUpdateObjects( op)
        res = self.antidoteClient.recvMessageOperationResp()
        return res.success == True

    def commit( self) :
        """ Commit transaction. Commit time gets recoded in AntidoteClient as
        last_commit
        """
        op = ApbCommitTransaction()
        op.transaction_descriptor = self.txDescriptor
        self.antidoteClient.sendMessageCommitTransaction( op)
        res = self.antidoteClient.recvMessageCommitResp()
        if res.success == True:
            self.antidoteClient.last_commit = res.commit_time
        return res.success == True

    def abort( self) :
        """ Commit transaction. Commit time gets recoded in AntidoteClient as
        last_commit
        """
        op = ApbAbortTransaction()
        op.transaction_descriptor = self.txDescriptor
        self.antidoteClient.sendMessageCommitTransaction( op)
        res = self.antidoteClient.recvMessageCommitResp()
        return res





class AntidoteClient :
    """ AntidoteDB protobuf client
    """
    def __init__(self, address = None, port = None, serverAddress = None):
        """ Intiialize a client, connecting to an AntidoteDB server located
        at serverAddress (of type ServerAddress)
        """
        if serverAddress == None:
            self.connect( ServerAddress( address, port))
        else:
            self.connect( serverAddress)
        self.last_commit = None

    def connect( self, serverAddress):
        """ Connect this AntidoteClient to the AntidoteDB server located
        at serverAddress (of type ServerAddress)
        """
        self.serverAddress = serverAddress
        try :
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect( serverAddress.getAddress())
        except socket.error as e:
            self.server = None
            raise AntidoteException( e)

    def close( self) :
        """ Closes the underlying connection of this client
        """
        try :
            if self.server != None :
                self.server.close()
                self.server = None
        except socket.error as e:
            self.server = None
            raise AntidoteException( e)

    def start_transaction( self, read_write = 0, red_blue = 0, min_snapshot = None) :
        """ Starts an interactive transaction, returning an object of type
        InteractiveTransaction. Raises an exception if the operation fails.
        """
        apbtxn = ApbStartTransaction()
        apbtxn.properties.read_write = read_write
        apbtxn.properties.red_blue = red_blue
        if min_snapshot is not None:
            apbtxn.timestamp = min_snapshot
        self.sendMessageStartTransaction( apbtxn)
        apbtxnresp = self.recvMessageStartTransactionResp()
        if apbtxnresp.success :
            return InteractiveTransaction( self, apbtxnresp.transaction_descriptor)
        else :
            raise AntidoteException( "Start transaction failed")

    def start_static_transaction( self, red_blue = 0, min_snapshot = None) :
        """ Starts a static transaction, returning an object of type
        StaticTransaction. Raises an exception if the operation fails.
        """
        return StaticTransaction( self, red_blue, min_snapshot)


    #---------------------------------------------------------------------------------
    # Utilities
    #---------------------------------------------------------------------------------
    def decodeObjectReply( key, val) :
        """ Decodes the value of an object returned in a read, creating
        the appropriate data type
        """
        if key.data_type == CRDT_type.Value("COUNTER") or key.data_type == CRDT_type.Value("FATCOUNTER"):
            return Counter(key, val.counter.value)
        if key.data_type == CRDT_type.Value("LWWREG"):
            return Register(key, val.reg.value)
        if key.data_type == CRDT_type.Value("MVREG"):
            return MVRegister(key, val.mvreg.values)
        if key.data_type == CRDT_type.Value("ORSET") or key.data_type == CRDT_type.Value("RWSET"):
            return Set(key, val.set.value)
        if key.data_type == CRDT_type.Value("FLAG_EW") or key.data_type == CRDT_type.Value("FLAG_DW"):
            return Flag(key, val.flag.value)
        if key.data_type == CRDT_type.Value("GMAP") or key.data_type == CRDT_type.Value("RRMAP"):
            els = {}
            for el in val.map.entries:
                els[el.key.key] = AntidoteClient.decodeObjectReply( Key( "", el.key.key, el.key.type), el.value)
            return Map(key, els)
        raise AntidoteException( "Unknown type")

    #---------------------------------------------------------------------------------
    # Methods for reading messages from the server
    #---------------------------------------------------------------------------------
    def recvNBytes( self, nbytes) :
        if self.server == None:
            raise AntidoteException( "Not connected to server")
        try :
#            data = []
#            nRecv = 0;
#            while nRecv < nbytes:
#                d = self.server.recv( nbytes - nRecv)
#                nRecv = nRecv + len(d)
#                data.append( d)
#            return ''.join(data)
            return self.server.recv( nbytes)
        except socket.error as e:
            raise AntidoteException( e)

    def recvMessageRaw( self) :
        data = self.recvNBytes( 5)
        msgSize, msgCode = struct.unpack( ">IB", data)
        return msgCode, self.recvNBytes( msgSize - 1)

    def recvMessageCommitResp( self) :
        msgCode, data = self.recvMessageRaw()
        if msgCode == 127 :
            msg = ApbCommitResp()
            msg.ParseFromString(data)
            return msg
        raise AntidoteClient.invalidReply(msgCode, data)

    def recvMessageOperationResp( self) :
        msgCode, data = self.recvMessageRaw()
        if msgCode == 111 :
            msg = ApbOperationResp()
            msg.ParseFromString(data)
            return msg
        raise AntidoteClient.invalidReply(msgCode, data)

    def recvMessageReadObjectsResp( self) :
        msgCode, data = self.recvMessageRaw()
        if msgCode == 126 :
            msg = ApbReadObjectsResp()
            msg.ParseFromString(data)
            return msg
        raise AntidoteClient.invalidReply(msgCode, data)

    def recvMessageStaticReadObjectsResp( self) :
        msgCode, data = self.recvMessageRaw()
        if msgCode == 128 :
            msg = ApbStaticReadObjectsResp()
            msg.ParseFromString(data)
            return msg
        raise AntidoteClient.invalidReply(msgCode, data)

    def recvMessageStartTransactionResp( self) :
        msgCode, data = self.recvMessageRaw()
        if msgCode == 124 :
            msg = ApbStartTransactionResp()
            msg.ParseFromString(data)
            return msg
        raise AntidoteClient.invalidReply(msgCode, data)

    @staticmethod
    def invalidReply(msgCode, data):
        if msgCode == 0:
            msg = ApbErrorResp()
            msg.ParseFromString(data)
            return AntidoteException(f"Antidote error {msg.errcode}: {msg.errmsg.decode('utf-8')}")
        return AntidoteException(f"Invalid reply (code {msgCode})")

    #---------------------------------------------------------------------------------
    # Methods for sending messages to the server
    #---------------------------------------------------------------------------------
    def sendMessage( self, msg, msgCode) :
        if self.server == None:
            raise AntidoteException( "Not connected to server")
        try :
            msgB = msg.SerializeToString()
            buf = struct.pack( '>IB', len(msgB) + 1, msgCode)
            self.server.sendall( buf)
            self.server.sendall( msg.SerializeToString())
        except socket.error as e:
            raise AntidoteException( e)

    def sendMessageReadObjects( self, msg) :
        self.sendMessage( msg, 116)

    def sendMessageUpdateObjects( self, msg) :
        self.sendMessage( msg, 118)

    def sendMessageStartTransaction( self, msg) :
        self.sendMessage( msg, 119)

    def sendMessageAbortTransaction( self, msg) :
        self.sendMessage( msg, 120)

    def sendMessageCommitTransaction( self, msg) :
        self.sendMessage( msg, 121)

    def sendMessageStaticUpdateObjects( self, msg) :
        self.sendMessage( msg, 122)

    def sendMessageStaticReadObjects( self, msg) :
        self.sendMessage( msg, 123)

