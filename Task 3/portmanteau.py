#!/user/bin/python
import numpy as np
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cross_decomposition import PLSCanonical,PLSRegression

vec_dict = {}
dataset, l_c, l_p, l_c_t, l_p_t = [], [], [], [], []

with open('data.txt', 'r') as data:
    data_l = data.readlines()

with open('vector.txt', 'r') as vec:
    vectors = vec.readlines()

for l in data_l:
    tokens_list = []
    tokens = l.strip().split(',')
    for t in tokens:
        tokens_list.append(t)
    dataset.append(tokens_list)

for line in vectors:
    temp = []
    tokens = line.strip().split(' ')
    for i in range(1,len(tokens)):
        if tokens[i]:
            num = float(tokens[i].strip())
            temp.append(num)
    vec_dict[tokens[0]] = temp

len_train = 0.8 * len(dataset)
j = 0

for t_list in dataset:
    p_word = t_list[0]
    vec_p = vec_dict[p_word]
    word1 = t_list[1]
    vec1 = vec_dict[word1]
    word2 = t_list[2]
    vec2 = vec_dict[word2]    
    vec_c = []

    for i in vec1:
        vec_c.append(i)
    for i in vec2:
        vec_c.append(i)

    if j < len_train:          
        l_p.append(vec_p)
        l_c.append(vec_c)  
    else:
        l_p_t.append(vec_p)
        l_c_t.append(vec_c) 
    j += 1

sorted_p = np.asarray(l_p) 
sorted_c = np.asarray(l_c)     #Convert the input to an array

plc = PLSCanonical()
plc.fit_transform(sorted_c, sorted_p)
sorted_c,sorted_p = plc.transform(sorted_c, sorted_p)

sorted_c_test = np.asarray(l_c_t)
sorted_p_test = np.asarray(l_p_t)
sorted_c_test,sorted_p_test = plc.transform(sorted_c_test,sorted_p_test)

plr = PLSRegression()
plr.fit(sorted_c, sorted_p)
params = plr.get_params()
plr.set_params(**params)
y_score = plr.predict(sorted_c_test)
sim_count = 0

print ("Test Similarity: ");
for i in range(len(y_score)):
    result_sim = 1 - spatial.distance.cosine(y_score[i], sorted_p_test[i])
    if result_sim >= 0.85:
        sim_count += 1
    print ("Data "+str(i+1)+" : "+str(result_sim))
accuracy = float(sim_count)/float(len(y_score))
print ("Accuracy: " + str(accuracy))
