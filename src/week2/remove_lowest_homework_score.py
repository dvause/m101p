
import pymongo
import sys

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

# get a handle to the school database
db=connection.students
grades = db.grades


def find():

    print "find, reporting for duty"

    query = {'type':'homework'}

    try:

        cursor = grades.find(query)

        cursor = cursor.sort([('student_id',pymongo.ASCENDING),('score',pymongo.DESCENDING)])

        cursor.limit(20)


    except:
        print "Unexpected error:", sys.exc_info()[0]


    pos = 0
    records_removed = 0
    while (pos < cursor.count()):
        print "current item: " + str(cursor[pos])
        current_student_id = cursor[pos]['student_id']
        print "current student_id is: " + str(current_student_id) + " score: " + str(cursor[pos]['score'])

        if pos > 0:
            last_student_id = cursor[pos-1]['student_id']
            print "last student_id is: " + str(last_student_id) + " score: " + str(cursor[pos]['score'])
            if last_student_id != current_student_id:
                print "student_id is different"
                try:
                    print "removing " + str(cursor[pos-1])
                    db.grades.remove(cursor[pos-1]["_id"])
                    records_removed += 1
                except:
                    print "Unexpected error:", sys.exc_info()[0]
        if pos == cursor.count()-1:
            print "last item!"
            try:
                db.grades.remove(cursor[pos]["_id"])
            except:
                print "Unexpected error:", sys.exc_info()[0]
            records_removed += 1
        pos += 1

    print "removed " + str(records_removed) + " records"

find()
