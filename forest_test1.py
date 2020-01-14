from __future__ import division
import pandas as pd
import getopt,sys
from random import randrange
from pandas import ExcelFile

class Motif:
    name = "blank"
    PHI = 0.0
    TP = 0.0
    TN = 0.0
    FP = 0.0
    FN = 0.0
    Accuracy = 0.0
    seqzero = []  # a list to hold all row indexes of sequences not present in a motif
    seqone = []   # a list to hold all row indexes of sequences present in a motif
    totalpos = 0
    totalneg = 0
    colindex = 0

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def run_tree(excel,motif_names,motif_indexes,row_indexes):
    x = len(motif_indexes)  
    total_rows = len(row_indexes)
    obj = Motif()
    obj.PHI = 0

    for i in range (x):
        name = motif_names[motif_indexes[i]]
        y = 0
        z = 0
        left = []
        right = []
        zero = []
        one = []
        negt = 0
        post = 0
        for j in range(total_rows):
            if(excel[row_indexes[j],motif_indexes[i]] == 1.0):
                y = y + 1
                x1 = excel[row_indexes[j],len(df.columns) - 1]
                if x1 == 1.0:
                    post = post + 1
                else:
                    negt = negt + 1
                right.append(x1)
                one.append(j)
            else:
                z = z + 1
                y1 = excel[row_indexes[j],len(df.columns) - 1]
                if y1 == -1.0:
                    negt = negt + 1
                if y1 == 1.0:
                    post = post + 1
                left.append(y1)
                zero.append(j)
        
        left_pos =0
        left_neg = 0
        right_pos = 0
        right_neg = 0

        TruePos = 0
        TrueNeg = 0
        FalsePos = 0
        FalseNeg = 0

        for item in left:
            if item == 1.0:
                left_pos = left_pos + 1
                FalseNeg = FalseNeg + 1
            else:
                left_neg = left_neg + 1
                TrueNeg = TrueNeg + 1

        for item in right:
            if item == 1.0:
                right_pos = right_pos + 1
                TruePos = TruePos + 1
            else:
                right_neg = right_neg + 1
                FalsePos = FalsePos + 1

        jneg = 0
        jpos = 0

        if z == 0 and y == 0:
            jneg = abs((left_neg) - (right_neg))
            jpos = abs((left_pos)-(right_pos))

        elif z == 0 or y == 0:
            if z == 0:
                jneg = abs((left_neg) - (right_neg/y))
                jpos = abs((left_pos)-(right_pos/y))
            else:
                jneg = abs((left_neg/z) - (right_neg))
                jpos = abs((left_pos/z)-(right_pos))
        else:
            jneg = abs((left_neg/z) - (right_neg/y))
            jpos = abs((left_pos/z)-(right_pos/y))

        jsum = jneg + jpos
        PLC= z / total_rows
        PLR = y / total_rows 
        PHI = 2*PLC*PLR*jsum

        if PHI > obj.PHI:
            obj.name = name
            obj.PHI = PHI
            obj.TP = TruePos
            obj.TN = TrueNeg
            obj.FP = FalsePos
            obj.FN = FalseNeg
            obj.Accuracy = ((TruePos + TrueNeg)/total_rows)
            obj.seqone = one 
            obj.seqzero = zero 
            obj.colindex = i
            obj.totalpos = post 
            obj.totalneg = negt 
    return obj 

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def run_tree_children(dataframe,motif_names,motif_indexes,row_indexes,prev_motif_col):
    x = len(motif_indexes)  
    total_rows = len(row_indexes)
    obj = Motif()
    obj.PHI = 0
    for i in range (x):
        name = motif_names[motif_indexes[i]]
        y = 0
        z = 0
        left = []
        right = []
        zero = []
        one = []
        negt = 0
        post = 0
        for j in range(total_rows):
            if i != prev_motif_col:
                if(df.iat[row_indexes[j],motif_indexes[i]] == 1.0):
                    y = y + 1
                    x1 = df.iat[row_indexes[j],len(df.columns) - 1]
                    if x1 == 1.0:
                        post = post + 1
                    else:
                        negt = negt + 1
                    right.append(x1)
                    one.append(j)
                else:
                    z = z + 1
                    y1 = df.iat[row_indexes[j],len(df.columns) - 1]
                    if y1 == -1.0:
                        negt = negt + 1
                    if y1 == 1.0:
                        post = post + 1
                    left.append(y1)
                    zero.append(j)
        
        left_pos =0
        left_neg = 0
        right_pos = 0
        right_neg = 0

        TruePos = 0
        TrueNeg = 0
        FalsePos = 0
        FalseNeg = 0

        for item in left:
            if item == 1.0:
                left_pos = left_pos + 1
                FalseNeg = FalseNeg + 1
            else:
                left_neg = left_neg + 1
                TrueNeg = TrueNeg + 1

        for item in right:
            if item == 1.0:
                right_pos = right_pos + 1
                TruePos = TruePos + 1
            else:
                right_neg = right_neg + 1
                FalsePos = FalsePos + 1

        jneg = 0
        jpos = 0

        if z == 0 and y == 0:
            jneg = abs((left_neg) - (right_neg))
            jpos = abs((left_pos)-(right_pos))

        elif z == 0 or y == 0:
            if z == 0:
                jneg = abs((left_neg) - (right_neg/y))
                jpos = abs((left_pos)-(right_pos/y))
            else:
                jneg = abs((left_neg/z) - (right_neg))
                jpos = abs((left_pos/z)-(right_pos))
        else:
            jneg = abs((left_neg/z) - (right_neg/y))
            jpos = abs((left_pos/z)-(right_pos/y))

        jsum = jneg + jpos
        PLC= z / total_rows
        PLR = y / total_rows 
        PHI = 2*PLC*PLR*jsum

        if PHI > obj.PHI:
            obj.name = name
            obj.PHI = PHI
            obj.TP = TruePos
            obj.TN = TrueNeg
            obj.FP = FalsePos
            obj.FN = FalseNeg
            obj.Accuracy = ((TruePos + TrueNeg)/total_rows)
            obj.seqone = one 
            obj.seqzero = zero 
            obj.colindex = i
            obj.totalpos = post 
            obj.totalneg = negt 
    return obj 


def pick_rows(df):
    size_rows = len(df.index) - 1
    is_in = [0] * size_rows
    rows_picked = []
    count = 0
    for x in range(size_rows):
        y = randrange(size_rows)
        rows_picked.append(y)
        is_in[y] = 1
    for x in range(size_rows):
        if is_in[x] == 1:
            count = count + 1
    return rows_picked,(size_rows - count)



if __name__ =='__main__':
    opts, args = getopt.getopt(sys.argv[1:],'hd:n:',['help','numtrees'])
    numtrees = 10
    for opt,value in opts:
        if opt == '-n':
            numtrees = int(value)
    ### Read our starting excel file
    df = pd.read_csv('C:\Users\Jesse\Desktop\ETS.training.csv', index_col = 0)
    df = df.iloc[:df.shape[0],:df.shape[1]]
    excel = df.values




    ### This list holds the names of all motifs. This way we can reference the correct Motif name later if 
    ### we know our column index
    motif_names = []
    motif_names = list(df.columns.values) 
    out_of_bag = 0
    oobsum = 0
    for total_trees in range(numtrees):
        motif_indexes = []
        row_indexes = []
        for x in range(10):
            motif_indexes.append(randrange(107))
        row_indexes,out_of_bag = pick_rows(df)
        root = run_tree(excel,motif_names,motif_indexes,row_indexes)
        print("*****************")
        print("Tree"),
        print(total_trees)
        print("Name:"),
        print(root.name)
        print("PHI:"),
        print(root.PHI)
        print("Out of bag for this tree:"),
        print(out_of_bag)

        oobsum = oobsum + out_of_bag
        leftlength = len(root.seqzero)
        rightlength = len(root.seqone)

        ### now we are going to create new dataframes for the left and right children

        list_of_rows_left = []
        list_of_rows_right = []



        ### Creates the left child of the root and the right child of the root
        leftChild = run_tree_children(excel,motif_names,motif_indexes,root.seqzero,root.colindex)
        rightChild = run_tree_children(excel,motif_names,motif_indexes,root.seqone,root.colindex)
        
        ### Now we determine our pure leaf sequences
        colindex1 = rightChild.colindex 
        colindex2 = leftChild.colindex 

        rightleafneg = 0
        rightleafpos = 0
        leftleafneg = 0
        leftleafpos = 0

        rightleafneg1 = 0
        rightleafpos1 = 0
        leftleafneg1 = 0
        leftleafpos1 = 0

        leftchildlefttree = len(leftChild.seqzero)
        leftchildrighttree = len(leftChild.seqone)
        rightchildlefttree = len(rightChild.seqzero)
        rightchildrighttree = len(rightChild.seqone)
   
        for i in range(0,leftchildlefttree):
            if excel[(leftChild.seqzero[i],(len(df.columns) - 1))] == -1.0:
                leftleafneg = leftleafneg + 1
            else:
                leftleafpos = leftleafpos + 1

        for i in range(0,leftchildrighttree):
            if excel[(leftChild.seqone[i],len(df.columns) - 1)] == -1.0:
                leftleafneg1 = leftleafneg1 + 1
            else:
                leftleafpos1 = leftleafpos1 + 1

        for i in range(0,rightchildlefttree):
            if excel[(rightChild.seqzero[i],len(df.columns) - 1)] == -1.0:
                rightleafneg = rightleafneg + 1
            else:
                rightleafpos = rightleafpos + 1

        for i in range(0,rightchildrighttree):
            if excel[(rightChild.seqone[i],len(df.columns) - 1)] == -1.0:
                rightleafneg1 = rightleafneg1 + 1
            else:
                rightleafpos1 = rightleafpos1 + 1
        print("Total left leaf neg:"),
        print(leftleafneg)
        print("Total left leaf pos:"),
        print(leftleafpos)
        print("Tota left leaf right child leaf neg:"),
        print(leftleafneg1)
        print("Total left leaf right child leaf pos:"),
        print(leftleafpos1)
        print("______")
        print("Total left leaf neg:"),
        print(rightleafneg)
        print("Total left leaf pos:"),
        print(rightleafpos)
        print("Tota left leaf right child leaf neg:"),
        print(rightleafneg1)
        print("Total left leaf right child leaf pos:"),
        print(rightleafpos1)

    print("The average out of bag sample size was:"),
    print(oobsum / numtrees)
    
    ## Now we begin the classifier 

    poscount = 0
    negcount = 0
    for i in range(0,50):
        randomrow = randrange(0,14000)
        length = len(leftChild.seqzero)
        for y in range(0, length):
            if randomrow == leftChild.seqzero[y]:
                x = 1
                nodeindex = y
        length1 = len(leftChild.seqone)
        for y in range(0, length1):
            if randomrow == leftChild.seqone[y]:
                x = 2
                nodeindex = y
        length2 = len(rightChild.seqzero)
        for y in range(0, length2):
            if randomrow == rightChild.seqzero[y]:
                x = 3
                nodeindex = y
        length3 = len(rightChild.seqone)
        for y in range(0, length3):
            if randomrow == rightChild.seqone[y]:
                x = 4        
                nodeindex = y     
        if x == 1:
            if leftleafneg > leftleafpos:
                negcount = negcount + 1
            else:
                poscount = poscount + 1
        if x == 2:
            if leftleafneg1 > leftleafpos1:
                negcount = negcount + 1
            else:
                poscount = poscount + 1
        if x == 3:
            if rightleafneg > rightleafpos:
                negcount = negcount + 1
            else:
                poscount = poscount + 1
        if x == 4:
            if rightleafneg1 > rightleafpos1:
                negcount = negcount + 1
            else:
                poscount = poscount + 1
    print("Negatives: "),
    print(negcount)
    print("Positives:"),
    print(poscount)








    





