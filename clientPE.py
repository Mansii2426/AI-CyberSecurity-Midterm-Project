#!/usr/bin/env python

import boto3
import numpy as np
import argparse
import ast
from sklearn.preprocessing import RobustScaler

### Change the following to the correct endpoint name ###
myEndpointName = 'sagemaker-tensorflow-serving-2021-10-15-01-19-22-610'
def main():
 
    import json
    import ember
    
    from sklearn.preprocessing import RobustScaler
    rs = RobustScaler()
       
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--featureversion", type=int, default=2, help="EMBER feature version")
    parser.add_argument("binaries", metavar="BINARIES", type=str, nargs="+", help="PE files to classify")
    args = parser.parse_args()
    #opening the downloaded PE file
    testpe = open(args.binaries[0],'rb').read()
    #Feature extractor class of the ember project 
    extract = ember.PEFeatureExtractor() 
    data = extract.feature_vector(testpe) #vectorizing the extracted features
    scaled_data = rs.fit_transform([data])
    Xdata = np.reshape(scaled_data,(1, 2381))
    Xdata= Xdata.tolist()

    client = boto3.client('runtime.sagemaker',
				region_name='us-east-1',
                              	#### Change the following to your AWS credentials ####
				aws_access_key_id='ASIAUD2RCO2HH2ICE3GK', 
				aws_secret_access_key='eNrctJemQp21GPxKpp1zbL65N8xOS43CpsheZ+8L',
				aws_session_token='FwoGZXIvYXdzEPX//////////wEaDEAJdKcR6HYwEfLp0iK3AUvzJ9UoAgKt6cBM0XsoH7RKxUGE8s43zXA8sln/0rzqF8ZYa85kbQexoO5JBh4psK7ABnAUzG+i17pqN5VV6B2PldC3jj1EuAu32FZxziqZ/kwREsZSQmdNWZEI3LNK54BlZQBXKbLiY9MVCAPPRTCaqVrZgahGn1rep+cxm5T+2ybq1sRAPXJbAxeaoXuVyk0GZKRNeJTvAxQJX2ntQFMN6ygWnLAOXu6Sp0CuIsEoZJ9q+mTrbCjnnKmLBjItXftzlbEYpkLTYUfkvsIZkDC+UvbBcYqRBZGx3f1kxg3DD/gURkzQTieGnbl6')
    
    response = client.invoke_endpoint(EndpointName=myEndpointName, Body=json.dumps(Xdata),ContentType ='application/json')
    response_body = response['Body']
    out = response_body.read()
    astr = out.decode("UTF-8")
    out = ast.literal_eval(astr)
    print(out)

    #if out[0] >0.5:
    #    print("Malicious")
    #else:
    #    print("Benign")
		
if __name__ == "__main__":
	main()
