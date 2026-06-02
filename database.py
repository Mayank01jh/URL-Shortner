

#doc = {
#
#collection.count_documents()
#print(collection.find_one({"special_key": "abc123"}))

class urls():
    def __init__(self,mongo_db_collectiono_object) -> None:
        self.collection = mongo_db_collectiono_object

    def insert_url(self,url,special_key):
        if self.collection.count_documents({"special_key": special_key}) > 0:
            return False
        doc = {
            "special_key": special_key,
            "url": url,
            "clicks": 0 #http://127.0.0.1:8000/mp
        }
        self.collection.insert_one(doc)
        return True
    
    def fetch_url(self,special_key):
        try:
            data = self.collection.find_one({"special_key": special_key})
            self.collection.update_one({"special_key": special_key}, {"$inc": {"clicks": 1}})
            return data["url"]
        except:
            return "http://9ai.in"
    def count(self,special_key):
        try:
            data = self.collection.find_one({"special_key": special_key})
            return data["clicks"]
        except:
            return 0
        #data = self.collection.find_one({"special_key": special_key})
        #return data["url"]
    
#obj = urls(collection)
#print(obj.insert_url("9ai.in","abc123"))

#print(obj.fetch_url("abc123"))
