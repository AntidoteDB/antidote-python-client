#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 11:23:50 2019

@author: nmp
"""

from antidotedb import *

def test_counter() :
    key = Key( "some_bucket", "some_key_fatcounter", "COUNTER")
    key2 = Key( "some_bucket", "some_other_key_fatcounter", "COUNTER")
    
    clt = AntidoteClient( 'localhost', 8087)
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

def test_fatcounter() :
    key = Key( "some_bucket", "some_key_counter", "FATCOUNTER")
    key2 = Key( "some_bucket", "some_other_key_counter", "FATCOUNTER")
    
    clt = AntidoteClient( 'localhost', 8087)
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

def test_lwwreg() :
    key = Key( "some_bucket", "some_key_lwwreg1", "LWWREG")
    val = bytes("lightkone",'utf-8')
    clt = AntidoteClient( 'localhost', 8087)
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


def test_mvreg() :
    key = Key( "some_bucket", "some_key_mvreg", "MVREG")
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')

    clt1 = AntidoteClient( 'localhost', 8087)
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

def test_orset() :
    key = Key( "some_bucket", "some_key_orset", "ORSET")
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient( 'localhost', 8087)
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

def test_rwset() :
    key = Key( "some_bucket", "some_key_rwset", "RWSET")
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient( 'localhost', 8087)
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

def test_flagew() :
    key = Key( "some_bucket", "some_key_flagew", "FLAG_EW")
    
    clt = AntidoteClient( 'localhost', 8087)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    res = tx.update_objects( Flag.enableKeyOp( key))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( res[0].value())
    res = tx.update_objects( Flag.disableKeyOp( key))
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

def test_flagdw() :
    key = Key( "some_bucket", "some_key_flagdw", "FLAG_DW")
    
    clt = AntidoteClient( 'localhost', 8087)
    tx = clt.start_static_transaction()
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    res = tx.update_objects( Flag.enableKeyOp( key))
    assert( res)
    res = tx.read_objects( key)
    assert( type(res[0]) == Flag)
    assert( res[0].value())
    res = tx.update_objects( Flag.disableKeyOp( key))
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

def test_gmap() :
    key = Key( "some_bucket", "some_key_gmap", "GMAP")
    k1 = bytes("k1",'utf-8')
    k2 = bytes("k2",'utf-8')
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient( 'localhost', 8087)
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

def test_rrmap() :
    key = Key( "some_bucket", "some_key_rrmap", "RRMAP")
    k1 = bytes("k1",'utf-8')
    k2 = bytes("k2",'utf-8')
    val1 = bytes("lightkone",'utf-8')
    val2 = bytes("syncfree",'utf-8')
    val3 = bytes("concordant",'utf-8')
    
    clt = AntidoteClient( 'localhost', 8087)
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


def test_all():
    res = test_counter()
    res = test_fatcounter()
    res = test_lwwreg()
    res = test_mvreg()
    res = test_orset()
    res = test_rwset()
    res = test_flagew()
    res = test_flagdw()
    res = test_gmap()
    res = test_rrmap()
    return res


test_all()


