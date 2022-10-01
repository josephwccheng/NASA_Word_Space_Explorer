#tutorial https://www.youtube.com/watch?v=GMppyAPbLYk&ab_channel=TechWithTim
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from os.path import exists
import pandas as pd
from search_engine_v1 import SearchEngineV1

app = Flask(__name__)
api = Api(app) # Side Note: Wrapping flask into Restful API

# Web Server Gateway Interface
glove_embedder_file_path = '../model/glove.6B.100d.txt'
document_embedder_file_path ='../data/ntrs_word_embedder_with_glove.txt'
ntrs_cdms_results_file_path ='../data/ntrs_cdms_results.csv'
# Check for all essential files
for file in [glove_embedder_file_path, document_embedder_file_path, ntrs_cdms_results_file_path]:
    if not exists(file):
        print(f'{file} not found. it is required for the app')
ntrs_cdms_results_df = pd.read_csv(ntrs_cdms_results_file_path)
search_engine = SearchEngineV1(glove_embedder_file_path=glove_embedder_file_path, document_embedder_file_path=document_embedder_file_path)


class Home(Resource): # Side Note: creating a class and inherit from Resource - different methods we can overwrite on
    #TODO
    def get(self):
        return jsonify("Welcome to the NASA 2022 Hackathon - Word Space Explorer")

class SearchEngine(Resource): # Side Note: creating a class and inherit from Resource - different methods we can overwrite on
    def post(self):
        json_data = request.get_json()
        recommended_document_list = search_engine.recommend_top_documents_from_query(json_data['query'])
        result = {"documentList": recommended_document_list}
        return jsonify(result)

class DocumentMetadata(Resource): # Side Note: creating a class and inherit from Resource - different methods we can overwrite on
    def get(self, document_id):
        result_df = ntrs_cdms_results_df[ntrs_cdms_results_df.document_id == document_id]
        if len(result_df) > 0:
            result = result_df.to_dict('records')
            return jsonify(result)
        return jsonify({"searchResult": f'Document ID Not Found'})

# Register this class as a resource
api.add_resource(DocumentMetadata, "/documentMetadata/<int:document_id>")
api.add_resource(SearchEngine, "/searchEngine")
api.add_resource(Home, "/")

if __name__ == '__main__':
    app.run(debug=True)