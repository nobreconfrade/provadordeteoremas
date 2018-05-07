"""
    OPAT
"""
import Formula


count = 0
cardinality = 0
formList = []

with open('test/test1.seq') as f:
    for l in f:
        if count == 0:
            cardinality = l
        else:
            raw = l.split(" ")
            raw[len(raw)-1] = raw[len(raw)-1].rstrip()
            raw.insert(0,'1')
            formList.append(raw)
        count += 1
    formList[len(formList)-1][0] = '1'
    print(formList)
