#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 11:23:50 2019

@author: nmp
"""

from antidotedb import *
import sys

def test_counter( server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_counter", "COUNTER")
    key2 = Key( "some_bucket", "some_other_key_counter", "COUNTER")
    
    clt = AntidoteClient(server,port)
    tx = clt.start_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    val = res[0].value()
    res = tx.read_objects( [key,key2])
    assert( len(res) == 2)
    assert( type(res[0]) == Counter)
    assert( type(res[1]) == Counter)
    res = tx.update_objects( Counter.IncOp(key, 2))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    assert( res[0].value() == val + 2)
    res = tx.commit()
    assert( res)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    assert( res[0].value() == val + 2)
    res = tx.update_objects( Counter.IncOp(key, 1))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    assert( res[0].value() == val + 3)
    return res

def test_fatcounter(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_counter", "FATCOUNTER")
    key2 = Key( "some_bucket", "some_other_key_counter", "FATCOUNTER")
    
    clt = AntidoteClient(server,port)
    tx = clt.start_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    val = res[0].value()
    res = tx.read_objects( [key,key2])
    assert( len(res) == 2)
    assert( type(res[0]) == Counter)
    assert( type(res[1]) == Counter)
    res = tx.update_objects( Counter.IncOp(key, 2))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    assert( res[0].value() == val + 2)
    res = tx.commit()
    assert( res)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    assert( res[0].value() == val + 2)
    res = tx.update_objects( Counter.IncOp(key, 1))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Counter)
    assert( res[0].value() == val + 3)
    return res

def test_lwwreg(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_lwwreg1", "LWWREG")
    val = bytes("lightkone",'utf-8')
    clt = AntidoteClient(server,port)
    tx = clt.start_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Register)
    res = tx.update_objects( Register.AssignOp( key, val))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Register)
    assert( res[0].value() == val)
    res = tx.commit()
    assert( res)
    return res


def test_mvreg(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_mvreg", "MVREG")
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')

    clt1 = AntidoteClient(server,port)
    tx1 = clt1.start_transaction()
    res = tx1.read_objects( key)
    assert( type(res[0]) == MVRegister)
    res = tx1.update_objects( MVRegister.AssignOp(key, val2))
    assert( res)
    res = tx1.read_objects( key)
    assert( type(res[0]) == MVRegister)
    assert( val2 in res[0].values())
    res = tx1.commit()
    assert( res)
    tx = clt1.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == MVRegister)
    assert( val2 in res[0].values())
    res = tx.update_objects( MVRegister.ResetOp(key))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == MVRegister)
    assert( len(res[0].values()) == 0)
    return res

def test_orset(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_orset", "ORSET")
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient(server,port)
    tx = clt.start_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    res = tx.update_objects( Set.AddOp( key, [val1,val2]))
    assert( res)
    res = tx.update_objects( Set.AddOp( key, val3))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    assert( val1 in res[0].values())
    assert( val2 in res[0].values())
    assert( val3 in res[0].values())
    res = tx.commit()
    assert( res)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    assert( val1 in res[0].values())
    assert( val2 in res[0].values())
    assert( val3 in res[0].values())
    res = tx.update_objects( Set.RemoveOp(key, val2))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    assert( val1 in res[0].values())
    assert( val2 not in res[0].values())
    assert( val3 in res[0].values())
    return res

def test_rwset(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_rwset", "RWSET")
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient(server,port)
    tx = clt.start_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    res = tx.update_objects( Set.addKeyOp( [val1,val2], key))
    assert( res)
    res = tx.update_objects( Set.addKeyOp( val3, key))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    assert( val1 in res[0].values())
    assert( val2 in res[0].values())
    assert( val3 in res[0].values())
    res = tx.commit()
    assert( res)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    assert( val1 in res[0].values())
    assert( val2 in res[0].values())
    assert( val3 in res[0].values())
    res = tx.update_objects( Set.removeKeyOp( val2, key))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Set)
    assert( val1 in res[0].values())
    assert( val2 not in res[0].values())
    assert( val3 in res[0].values())
    return res

def test_flagew(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_flagew", "FLAG_EW")
    
    clt = AntidoteClient(server,port)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    res = tx.update_objects( Flag.UpdateOp( key, True))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( res[0].value())
    res = tx.update_objects( Flag.UpdateOp( key, False))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( not res[0].value())
    res = tx.update_objects( Flag.ResetOp( key))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( not res[0].value())
    return res

def test_flagdw(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_flagdw", "FLAG_DW")
    
    clt = AntidoteClient(server,port)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    res = tx.update_objects( Flag.UpdateOp( key, True))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( res[0].value())
    res = tx.update_objects( Flag.UpdateOp( key, False))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( not res[0].value())
    res = tx.update_objects( Flag.ResetOp( key))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( not res[0].value())
    return res

def test_gmap(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_gmap", "GMAP")
    k1 = bytes("k1",'utf-8')
    k2 = bytes("k2",'utf-8')
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient(server,port)
    tx = clt.start_transaction()
    res = tx.read_objects( key)
    assert( res)
    res = tx.update_objects( Map.UpdateOp( key, [Counter.IncOp( k1, 1, "COUNTER"), Register.AssignOp( k2, val1, "LWWREG")]))
    assert(res)
    res = tx.read_objects( key)
    assert( k1 in res[0].values())
    assert( k2 in res[0].values())
    res = tx.commit()
    assert( res)
    
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( k1 in res[0].values())
    assert( k2 in res[0].values())

    res = tx.update_objects( Map.RemoveOp( key, [Key( "", k1, "COUNTER")]))
    assert( res == False)

    return res

def test_rrmap(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_rrmap", "RRMAP")
    k1 = bytes("k1",'utf-8')
    k2 = bytes("k2",'utf-8')
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient(server,port)
    tx = clt.start_transaction()
    res = tx.read_objects( key)
    assert( res)
    res = tx.update_objects( Map.UpdateOp( key, [Counter.IncOp( k1, 1, "COUNTER"), Register.AssignOp( k2, val1, "LWWREG")]))
    assert(res)
    res = tx.read_objects( key)
    assert( k1 in res[0].values())
    assert( k2 in res[0].values())
    res = tx.commit()
    assert( res)
    
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( k1 in res[0].values())
    assert( k2 in res[0].values())

    res = tx.update_objects( Map.RemoveOp( key, [Key( "", k1, "COUNTER")]))
    assert( res)

    res = tx.read_objects( key)
    return res

def test_committime(server = "localhost", port = 8087) :
    key = Key( "some_bucket", "some_key_committime", "MVREG")
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')

    client = AntidoteClient(server,port)
    tx = client.start_static_transaction()
    res = tx.update_objects(MVRegister.AssignOp(key, val1))
    assert(res)
    tx = client.start_static_transaction(min_snapshot=client.last_commit)
    res = tx.read_objects(key)
    assert(res[0].values() == [val1])
    res = tx.update_objects(MVRegister.AssignOp(key, val2))
    assert(res)
    tx = client.start_static_transaction(min_snapshot=client.last_commit)
    res = tx.read_objects(key)
    assert(res[0].values() == [val2])


def test_all(server = "localhost", port = 8087):
    test_committime(server, port)
    res = test_counter(server,port)
    res = test_fatcounter(server,port)
    res = test_lwwreg(server,port)
    res = test_mvreg(server,port)
    res = test_orset(server,port)
    res = test_rwset(server,port)
    res = test_flagew(server,port)
    res = test_flagdw(server,port)
    res = test_gmap(server,port)
    res = test_rrmap(server,port)
    return res


if len(sys.argv) == 2:
    test_all(str(sys.argv[1]),8087)
elif len(sys.argv) == 3:
    test_all(str(sys.argv[1]),int(sys.argv[2]))
else:
    test_all()
