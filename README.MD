
# Antidote Python Client

The repository contains classes for using Antidote Database service in Python. It provides the 
client implementation to use Antidote Database.

You can learn more about Antidote Database [here](http://antidotedb.eu/)

## Installation

For installing the Python AntidoteDB client, just use pip installer.

    pip antidotedb
    

## Documentation

The classes for accessing AntidoteDB are in package **antidotedb**.

For accessing AntidoteDB, you should start by creating an **AntidoteClient** object, as in the following
example.

    from antidotedb import *
    
    server = 'localhost'
    port = 8087
    
    clt = AntidoteClient(server, port)

### Interactive transactions

_start_transaction_ starts an interactive transactions. On failure,
_start_transaction_ method raises an _AntidoteException_.

    tx = clt.start_transaction()

_commit_ method commits a sequence of operations executed in a transaction. On success, 
the _commit_ method returns _True_.

    ok = tx.commit()

_abort_ method rollbacks the transactions.
 
    tx.abort()

#### Session guarantees

By default, the client will not maintain a session across consecutive transactions, i.e., 
there will be no causal dependency established between two consecutive transaction.

To set these dependencies, star a transactionas follows:


    tx = clt.start_transaction(min_snapshot=clt.last_commit)

### Operations on objects

The **Key** class allows to specify the AntidoteDB key for an object.

    Key( bucket_name, key_name, type_name)

_read_objects_ method allows to read the contents of one (or more) objects. On success, _read_objects_
returns a list of typed objects (more information next). On failure, 
_read_objects_ returns _None_. 

    key = Key( "some_bucket", "some_key_counter", "COUNTER")
    res = tx.read_objects( key)
    print( res[0].value())

It is also possible to read more than one object.

    key1 = Key( "some_bucket", "some_key", "COUNTER")
    key2 = Key( "some_bucket", "some_other_key", "MVREG")
    res = tx.read_objects( [key1,key2])
    print( res[0].value())
    print( res[1].values())

_update_objects_ method allows to update one (or more) objects. On success/failure, _update_objects_ returns _True_/_False_.

    key1 = Key( "some_bucket", "some_key", "COUNTER")
    res = tx.update_objects( Counter.IncOp(key1, 2))

#### Counters

The data type name for the Counter data type is: **COUNTER**.

    key = Key( "some_bucket", "some_key", "COUNTER")

The following **read only** operations are available in a **Counter** object
returned by _read_objects_ method:

* **value()**, for accessing the value of an object.

      res = tx.read_objects( key)
      print( res[0].value())

The following **update** operations are available:

* **Counter.IncOp(key, value)**, for incrementing a counter.

      res = tx.update_objects( Counter.IncOp(key, 2))
 
The other counter data type supported by AntidoteDB, _FATCounter_ can be used
using **FATCOUNTER** data type name.

#### Last-writer-wins register

The data type name for the Last-write-wins Register data type is: **LWWREG**.

    key = Key( "some_bucket", "some_key", "LWWREG")

The following **read only** operations are available in a **Register** object
returned by _read_objects_ method:

* **value()**, for accessing the value of an object.

      res = tx.read_objects( key)
      print( res[0].value())

The following **update** operations are available:

* **Register.AssignOp( key, val)**, for assigning a new value to the register.

      val = bytes("lightkone",'utf-8')
      
      res = tx.update_objects( Register.AssignOp( key, val))
 
#### Multi-value register

The data type name for the multi-value Register data type is: **MVREG**.

    key = Key( "some_bucket", "some_key", "MVREG")

The following **read only** operations are available in a **MVRegister** object
returned by _read_objects_ method:

* **values()**, for accessing the values of an object. The multiple values are returned in a list.

      res = tx.read_objects( key)
      print( res[0].values())

The following **update** operations are available:

* **Register.AssignOp( key, val)**, for assigning a new value to the register.

      val = bytes("lightkone",'utf-8')
      
      res = tx.update_objects( Register.AssignOp( key, val))
 
#### Sets

The data type name for the **add-wins set** data type is: **ORSET**.

    key = Key( "some_bucket", "some_key", "ORSET")
    
The data type name for the **remove-wins set** data type is: **RWSET**.

    key = Key( "some_bucket", "some_key", "RWSET")
  
The following **read only** operations are available in a **Set** object
returned by _read_objects_ method:

* **values()**, for accessing the value of the set. The multiple values are returned in a list.

      res = tx.read_objects( key)
      print( res[0].values())

The following **update** operations are available:

* **Set.AddOp( key, val)**, for adding values to the set.

      val1 = bytes("lightkone",'utf-8')
      val2 = bytes("syncfree",'utf-8')
      
      res = tx.update_objects( Set.AddOp( key, [val1,val2]))
 
* **Set.RemoveOp( key, val)**, for removing values from the set.

      val1 = bytes("lightkone",'utf-8')
      val2 = bytes("syncfree",'utf-8')
      
      res = tx.update_objects( Set.RemoveOp( key, [val1,val2]))


#### Flags

The data type name for the **enable-wins flag** data type is: **FLAG_EW**.

    key = Key( "some_bucket", "some_key", "FLAG_EW")
    
The data type name for the **disable-wins flag** data type is: **FLAG_DW**.

    key = Key( "some_bucket", "some_key", "FLAG_DW")
  
The following **read only** operations are available in a **Flag** object
returned by _read_objects_ method:

* **value()**, for accessing the value of the flag.

      res = tx.read_objects( key)
      print( res[0].value())

The following **update** operations are available:

* **Flag.UpdateOp( key, val)**, for setting a value to the flag.

      res = tx.update_objects( Flag.UpdateOp( key, True))
 

#### Maps

The data type name for the **grow-only map** data type is: **GMAP**.

    key = Key( "some_bucket", "some_key", "GMAP")
    
The data type name for the **recursive-remove map** data type is: **RRMAP**.

    key = Key( "some_bucket", "some_key", "RRMAP")
  
The following **read only** operations are available in a **Map** object
returned by _read_objects_ method:

* **value()**, for accessing the contents of the map. The map is represented by a Python
dictionary that maps a key to the object.

      res = tx.read_objects( key)
      print( res[0].value())

The following **update** operations are available:

* **Map.UpdateOp(key,ops)**, for removing a key from the map.

      k1 = bytes("k1",'utf-8')
      k2 = bytes("k2",'utf-8')
      val = bytes("lightkone",'utf-8')

      res = tx.update_objects( Map.RemoveOp( key, [Key( "", k1, "COUNTER")]))

* **Map.RemoveOp(key,ops)**, for executing a set of operations in the objects stored in the map.

      k1 = bytes("k1",'utf-8')

      res = tx.update_objects( Map.RemoveOp( key, [Key( "", k1, "COUNTER")]))

### Generic operations

The following **update** operations are available in all data types (when they 
are available in the AntidoteDB data type -- check the AntidoteDB documentation):

* **Type.ResetOp(key)**, for resetting the value.

      res = tx.update_objects( Flag.ResetOp(key))

# Development / Contributing

Any help on developing this code is welcome. Feel free to open pull requests or open issues.

Testing the AntidoteDB client requires an Antidote instance running. 
You can use Docker to start an instance in your local machine:

    docker run -d -p "8087:8087" antidotedb/antidote
