import json
import riak

client = riak.RiakClient(host="127.0.0.1", http_port=10018)
bucket = client.bucket('twitter_sample')
count = 0

# Open the 
for line in open('C:\data\sf_tweets.json'):
    try:
        tweet = json.loads(line)        
        # Store the object via POST (no key specified)
        # (alternatively, you can use the status id string as a key)
        riak_object = bucket.new(key=None, data=tweet)
        riak_object.store()
        count += 1
    except:
        pass

print "Loaded into Riak: %d" % count
