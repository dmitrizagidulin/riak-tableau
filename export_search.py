import dataextract as tde
import os
import riak
import tweetpony as tw

client = riak.RiakClient(host="127.0.0.1", http_port=10018)

# Create the Extract File
try:
    tdefile = tde.Extract('RiakExport-WebOnly.tde')
except:
    os.remove('RiakExport-WebOnly.tde')
    tdefile = tde.Extract('RiakExport-WebOnly.tde')

# Create the Tableau table definition
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

# Step 3: Create the table in the image of tableDef
table = tdefile.addTable('Extract', tableDef)

count = 0
# Iterate through all of the keys in the 'twitter_sample' bucket
results = client.fulltext_search(index='twitter_sample', query='source:web', rows=1000)
for result in results['docs']:
    # Create the Export row, as usual
    tweet = tw.Status.from_json(result)
    
    newrow = tde.Row(tableDef)
    newrow.setCharString(0, tweet.id_str)
    newrow.setCharString(1, tweet.text)
    newrow.setCharString(2, tweet.source)
    retweeted = tweet.retweeted == 'true'
    newrow.setBoolean(3, retweeted)
    newrow.setInteger(4, int(tweet.retweet_count))
    newrow.setInteger(5, int(tweet.user_friends_count))
    newrow.setCharString(6, tweet.user_lang)
    geo_enabled = tweet.user_geo_enabled == 'true'
    newrow.setBoolean(7, geo_enabled)
    try:
        # Most of the web-sourced Tweets don't have coordinates
        newrow.setDouble(8, tweet.coordinates.coordinates[1])
        newrow.setDouble(9, tweet.coordinates.coordinates[0])
    except:
        newrow.setNull(8)
        newrow.setNull(9)
    created = tweet.created_at
    newrow.setDateTime(10, created.year, created.month, created.day, created.hour, created.minute, created.second, 0)

    table.insert(newrow)
    count += 1

print "Exported %d objects" % count
tdefile.close()
