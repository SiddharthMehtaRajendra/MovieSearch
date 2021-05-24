import json
import requests
from elasticsearch import Elasticsearch


class SearchClient:

    def __init__(self):
        super().__init__()
        self.client = Elasticsearch([{'host': 'host.docker.internal', 'port': 9200}]) 

    def check_if_index_is_present(self, url):
        response = requests.request("GET", url, data="")
        json_data = json.loads(response.text)
        return json_data

    def index(self, id, index_name, doc_body):
        try:
            response = self.client.index(
                index = index_name,
                doc_type = '_doc',
                id = id,
                body = doc_body,
                request_timeout=45
            )
            print ("response:", response)
            if response["_shards"]["successful"] == 1:
                print ("INDEX CALL WAS SUCCESS:", response["_shards"]["successful"])
            else:
                print ("INDEX CALL FAILED")
        except Exception as err:
            print ("Elasticsearch index() ERROR:", err)

    def search(self, index, query):
        response = self.client.search(index=index, body=query)
        print(f"documents found: {response['hits']['total']['value']}")
        return response['hits']['hits']

    def test_es(self):
        data = [{"balance": "$2,410.62", "age": 40, "name": "Bettie Buckner", "gender": "female", "company": "RODEOMAD",
            "email": "bettiebuckner@rodeomad.com", "phone": "+1 (857) 491-2461"},
            {"balance": "$1,143.56", "age": 28, "name": "Hanson Gates", "gender": "male", "company": "PEARLESSA",
            "email": "hansongates@pearlessa.com", "phone": "+1 (825) 524-3896"},
            {"balance": "$2,542.95", "age": 20, "name": "Audra Marshall", "gender": "female", "company": "COMTRAIL",
            "email": "audramarshall@comtrail.com", "phone": "+1 (920) 569-2780"},
            {"balance": "$2,235.86", "age": 34, "name": "Milagros Conrad", "gender": "female", "company": "IDEGO",
            "email": "milagrosconrad@idego.com", "phone": "+1 (823) 451-2064"},
            {"balance": "$2,606.95", "age": 34, "name": "Maureen Lopez", "gender": "female", "company": "EVENTEX",
            "email": "maureenlopez@eventex.com", "phone": "+1 (913) 425-3716"}]
        for a_data in data:
            res = self.client.index(index='my-index', body=a_data)
        body = {'query': {'bool': {'must': [{'match': {'gender': 'male'}},{'range': {'age': {'gte': 25}}}]}}}
        return self.client.search(index='my-index', body=body)