import dataextract as tde
import os
import riak
import tweetpony as tw

# Set up a Riak connection
client = riak.RiakClient(host="127.0.0.1", http_port=10018)
bucket = client.bucket('twitter_sample')

# Create the Extract File
try:
    tdefile = tde.Extract('RiakExport.tde')
except:
    os.remove('RiakExport.tde')
    tdefile = tde.Extract('RiakExport.tde')

# Create the tableDef
tableDef = tde.TableDefinition()
tableDef.addColumn('id', tde.Type.CHAR_STRING)
tableDef.addColumn('text', tde.Type.CHAR_STRING)
tableDef.addColumn('source', tde.Type.CHAR_STRING)
tableDef.addColumn('retweeted', tde.Type.BOOLEAN)
tableDef.addColumn('retweet_count', tde.Type.INTEGER)
tableDef.addColumn('user_friends_count', tde.Type.INTEGER)
tableDef.addColumn('language', tde.Type.CHAR_STRING)
tableDef.addColumn('user_geo_enabled', tde.Type.BOOLEAN)
tableDef.addColumn('Latitude', tde.Type.DOUBLE)
tableDef.addColumn('Longitude', tde.Type.DOUBLE)
tableDef.addColumn('created_at', tde.Type.DATETIME)

#Step 3: Create the table in the image of tableDef
table = tdefile.addTable('Extract', tableDef)

count = 0
# Iterate through all of the keys in the 'twitter_sample' bucket
for keylist in bucket.stream_keys():
    for key in keylist:
        # Request the object from Riak
        riak_obj = bucket.get(key)
        
        # Instantiate a Twitter Status object from json
        tweet = tw.Status.from_json(riak_obj.data)
        
        # Create the Export row, as usual        
        newrow = tde.Row(tableDef)
        newrow.setCharString(0, tweet.id_str)
        newrow.setCharString(1, tweet.text)
        newrow.setCharString(2, tweet.source)
        newrow.setBoolean(3, tweet.retweeted)
        newrow.setInteger(4, tweet.retweet_count)
        newrow.setInteger(5, tweet.user.friends_count)
        newrow.setCharString(6, tweet.user.lang)
        newrow.setBoolean(7, tweet.user.geo_enabled)
        if tweet.coordinates:
            newrow.setDouble(8, tweet.coordinates.coordinates[1]) # Lat
            newrow.setDouble(9, tweet.coordinates.coordinates[0]) # Long
        else:
            newrow.setNull(8)
            newrow.setNull(9)
        
        created = tweet.created_at        
        newrow.setDateTime(10, created.year, created.month, created.day, created.hour, created.minute, created.second, 0)

        table.insert(newrow)
        count += 1

print "Exported %d objects" % count
tdefile.close()