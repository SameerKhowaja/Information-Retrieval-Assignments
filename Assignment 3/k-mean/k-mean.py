import math
import json
import numpy as np
import pandas as pd

with open('tf_idf_vectors_list.txt') as f:
    tf_idf_vectors_list = json.load(f)

with open('idf_list.txt') as f:
    idf_list = json.load(f)

idf_list = np.array(idf_list)
unit_vectors_document = np.array(tf_idf_vectors_list['vectors'])
vector_classes_list = tf_idf_vectors_list['class']


def euclidean_distance(var1, var2):
    ans_temp = (var1 - var2) * (var1 - var2)
    ans_temp = math.sqrt(ans_temp.sum())
    return ans_temp


def cosine_similarity(var1, var2):
    ans_temp = var1 * var2
    return ans_temp.sum()


def RSS(var1, var2):
    ans_temp = (var1 - var2) * (var1 - var2)
    ans_temp = ans_temp.sum()
    return ans_temp


def random_centroid(k):
    index = np.random.randint(low=0, high=len(unit_vectors_document), size=k)
    centroid = unit_vectors_document[index]
    return centroid


def kmean(k):
    centroid = random_centroid(k)
    clusters_dict = {}
    clusterClasses_dict = {}
    iterates = 0
    centroids_check = 1
    rss_old = 999999
    rss_sum = 99999
    rss_k = None
    while centroids_check == 1:
        centroids_check = 0

        for i in range(0, k):
            clusters_dict['cluster' + str(i)] = []
            clusterClasses_dict['cluster' + str(i)] = []

        for i in range(0, len(unit_vectors_document)):
            temp = list(unit_vectors_document[i])
            temp = [temp] * k
            temp = np.array(temp)
            simalarity = list(map(cosine_similarity, temp, centroid))

            max_similarity = max(simalarity)
            max_index = simalarity.index(max_similarity)
            clusters_dict['cluster' + str(max_index)].append(unit_vectors_document[i])
            clusterClasses_dict['cluster' + str(max_index)].append(vector_classes_list[i])

        for i in range(0, k):
            cluster_k = np.array(clusters_dict['cluster' + str(i)])

            if len(clusters_dict['cluster' + str(i)]) != 0:
                centroid_new = (cluster_k.sum(axis=0)) / len(cluster_k)

                mag = np.array(centroid_new)
                mag = mag * mag
                mag = math.sqrt(mag.sum())

                centroid_new = centroid_new / mag

                if not np.array_equal(centroid[i], centroid_new):
                    centroids_check = 1

                centroid[i] = centroid_new

        rss_old = rss_sum
        rss_sum = 0
        cluster_rss = pd.DataFrame(index=['cluster0', 'cluster1', 'cluster2', 'cluster3', 'cluster4'],
                                   columns=['RSS_k'])

        for i in range(0, k):
            cluster_k = np.array(clusters_dict['cluster' + str(i)])
            centroidk = [centroid[i]] * len(clusters_dict['cluster' + str(i)])
            centroidk = np.array(centroidk)

            rss_k = list(map(RSS, cluster_k, centroidk))

            rss_k = np.array(rss_k)

            rss_sum += rss_k.sum()
            cluster_rss['RSS_k']['cluster' + str(i)] = rss_k.sum()

        iterates += 1
    print(cluster_rss, '\n')
    # print('Total RSS :: ', rss_sum)

    return centroid, clusters_dict, clusterClasses_dict


classes = ['athletics', 'cricket', 'football', 'rugby', 'tennis']
centroid, clusters_dict, clusterClasses_dict = kmean(5)

for key, lst in clusters_dict.items():
    max_limit = -1
    clusterClass = ''

    for j in classes:
        if clusterClasses_dict[key].count(j) > max_limit:
            max_limit = clusterClasses_dict[key].count(j)
            clusterClass = j

    clusterClasses_dict[key] = (clusterClass, max_limit)
    print(key, '--', len(lst))

total_purity = 0

for key, lst in clusterClasses_dict.items():
    total_purity += clusterClasses_dict[key][1]

total_purity = total_purity / len(unit_vectors_document)
print('Purity(%) of Dataset :: ', total_purity * 100)
