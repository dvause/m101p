__author__ = 'davev'

import pymongo
import sys

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

# get a handle to the school database
db=connection.school
students = db.students

def find():
    try:
        cursor = students.find()

    except:
        print "Unexpected error:", sys.exc_info()[0]

    return cursor



for doc in find():
    print str(doc['_id'])
    homework_score_holder = []
    score_holder = []
    iter = 0
    for score in doc['scores']:
        if score['type'] == 'homework':
            homework_score_holder.append(score)
        else:
            score_holder.append(score)
    print homework_score_holder
    #kinda lame but my python is weak.
    # I know there are only 2 homework scores so I'll hardcode comparing the 2 scores and only keep the highest
    if homework_score_holder[0]['score'] > homework_score_holder[1]['score']:
        score_holder.append(homework_score_holder[0])
    else:
        score_holder.append(homework_score_holder[1])
    print score_holder
    print "Updating scores for " + str(doc['_id'])
    students.update({'_id':doc['_id']}, {'$set':{'scores':score_holder}})