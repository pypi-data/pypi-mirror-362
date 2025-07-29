import json
import sys

def runTask(data):
    #write program in here
    
    return {
        "result" : [ 
            {
                "type" : "text", #text audio image video
                "content": [ 
                    "hello world"
                ]
            }
        ],
        "status" : 0,  #0 is success
        "message" : ""
    }
