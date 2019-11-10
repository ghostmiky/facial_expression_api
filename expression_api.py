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
import logging as l

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
        #l.debug()
        #receivedData = request.get_json() # Receieve data]
        #file = request.files['file'].read()
        #text = receivedData['text']
        text = "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"
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