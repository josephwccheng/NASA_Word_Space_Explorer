from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from os.path import exists
import pandas as pd
from search_engine_v1 import SearchEngineV1
from tag_recommender_v1 import TagRecommenderV1

app = Flask(__name__)
api = Api(app) # Side Note: Wrapping flask into Restful API

# Web Server Gateway Interface
glove_embedder_file_path = 'model/glove.6B/glove.6B.100d.txt'
document_embedder_file_path ='model/ntrs_document_embedder_with_glove.txt'
ntrs_cdms_results_file_path ='data/ntrs_cdms_results.csv'
ntrs_trained_glove_model_file_path = 'model/ntrs_trained_glove_model.txt'
# Check for all essential files
for file in [glove_embedder_file_path, document_embedder_file_path, ntrs_cdms_results_file_path, ntrs_cdms_results_file_path]:
    if not exists(file):
        print(f'{file} not found. it is required for the app')
ntrs_cdms_results_df = pd.read_csv(ntrs_cdms_results_file_path)

# Models Deploymnet
search_engine = SearchEngineV1(glove_embedder_file_path=ntrs_trained_glove_model_file_path, document_embedder_file_path=document_embedder_file_path)
tag_recommender = TagRecommenderV1(ntrs_trained_glove_model_path= ntrs_trained_glove_model_file_path)

class Home(Resource): # Side Note: creating a class and inherit from Resource - different methods we can overwrite on
    #TODO
    def get(self):
        return jsonify("Welcome to the NASA 2022 Hackathon - Word Space Explorer")

# Tier one model
class SearchEngine(Resource): # Side Note: creating a class and inherit from Resource - different methods we can overwrite on
    def post(self):
        json_data = request.get_json()
        recommended_document_list = search_engine.recommend_top_documents_from_query(json_data['query'])
        result = {"documentList": recommended_document_list}
        return jsonify(result)

# Tier two model
class TagRecommender(Resource): # Side Note: creating a class and inherit from Resource - different methods we can overwrite on
    def post(self):
        json_data = request.get_json()
        recommended_word_embed = tag_recommender.get_sum_array_embedding(json_data['query'])
        recommended_words = tag_recommender.find_similar_word_from_glove_vector(recommended_word_embed)
        result = {"tagsRecommended": recommended_words}
        return jsonify(result)

class DocumentMetadata(Resource): # Side Note: creating a class and inherit from Resource - different methods we can overwrite on
    def get(self, document_id):
        result_df = ntrs_cdms_results_df[ntrs_cdms_results_df.document_id == document_id]
        if len(result_df) > 0:
            result = result_df.to_dict('records')[0]
            return jsonify(result)
        return jsonify({"searchResult": f'Document ID Not Found'})

class MultipleDocumentMetadata(Resource):
    def post(self):
        multiple_doc_list = []
        json_data = request.get_json()
        document_id_list = json_data['documentList']
        if len(document_id_list) > 0:
            for document_id in document_id_list:
                result_df = ntrs_cdms_results_df[ntrs_cdms_results_df.document_id == int(document_id)]
                if len(result_df) > 0:
                    multiple_doc_list.append(result_df.to_dict('records')[0])
        return jsonify(multiple_doc_list)

# Register this class as a resource
api.add_resource(MultipleDocumentMetadata, "/documentMultipleMetadata")
api.add_resource(DocumentMetadata, "/documentMetadata/<int:document_id>")
api.add_resource(SearchEngine, "/searchEngine")
api.add_resource(TagRecommender, "/tagRecommender")
api.add_resource(Home, "/")

if __name__ == '__main__':
    app.run(debug=True)