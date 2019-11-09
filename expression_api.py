# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:41:19 2019

@author: Malinda
"""

import label_image as li
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask import jsonify
import shutil
import os
from werkzeug import secure_filename
import numpy as np
from PIL import Image
import cv2
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

#def verify_summarization_data(receivedData):
#    if ('' not in receivedData):
#        return 300
#    else:
#        return 200


class summarize_api(Resource):
    @app.route('/',methods=['POST'])
    def post(self):
        receivedData = request.get_json() # Receieve data]
        #file = request.files['file'].read()
        text = receivedData['text']
        print()
        byte_check = text[0:2]
        if byte_check == "b'":            
            text = text[2:len(text)-1]
            img = base64.b64decode(text)
        else:
            img = base64.b64decode(text)
        

        with open("test2.jpg",'wb') as f:
            f.write(img)
        
        file_name = 'test2.jpg'
        try:            
            res = li.main(file_name)
        	
            returnJson = {
            	'result': res,
            	'status': 200 
	        }
            return jsonify(returnJson) 
        except Exception as e:
        	returnJson = {
            	'msg': e,
            	'status': 500
        	}
        	return jsonify(returnJson)
       

api.add_resource(summarize_api,'/expression/')

if __name__ == '__main__':
    app.run()
    
# Home route
@app.route('/api')
def welcome():
    return 'Text Summarization & Grammar Checking API'