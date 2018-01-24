#how to run:
# in the command line, first "cd" to the folder where the iris.data and ,py is
# and next to it, write python yang_chun_clustering.py iris.data k
# the output txt would also be shown in the same folder

import sys
import heapq

#file="C:/Users/user/Desktop/Inf553/HW4/iris.data"
file=sys.argv[1]
lines=open(file).readlines()
datas=[line.strip().split(",") for line in lines if line.strip()]


cluster={}
data_lists=[]

id=0
for data in datas:
    # one point one cluster K=150  {id:{centroid:,points:}}
    cluster[str([id])] = {}
    cluster[str([id])]["centroid"] = data[0:4]
    cluster[str([id])]["points"] = [id]

    each={}
    each["point"] = data[0:4]
    data_lists.append(each)
    id = id + 1

#print data_lists
#print cluster

#print len(data_lists)  150 data
#print len(cluster)  K=150
#point1=data_lists[0]["point"]
#print point1

def euclidean(point1,point2):
    sum=0
    for i in range(len(point1)):
        sum=sum+(float(point1[i])-float(point2[i]))**2
    return sum**0.5

def pair_cluster(total):
    total_distance=[]
    for i in range(len(total)-1):
        for j in range(i+1,len(total)):
            dis=euclidean(total[i]["centroid"],total[j]["centroid"])
            if total[i]["points"]<total[j]["points"]:
                total_distance.append((dis,[total[i]["points"],total[j]["points"]]))
            else:
                total_distance.append((dis, [total[j]["points"], total[i]["points"]]))
    return total_distance

def centroid(data,lists):
    sum=[0,0,0,0]
    for i in lists:
        for j in range(len(data[i]["point"])):
            sum[j]=float(data[i]["point"][j])+sum[j]
    centroid=[k/len(lists) for k in sum]
    return centroid

#print centroid(data_lists,[1,2,0])

queue=pair_cluster(list(cluster.values()))
#print queue

#k_number=3
k_number=int(sys.argv[2])
while len(cluster) > k_number:
    heapq.heapify(queue)
    priority= heapq.heappop(queue)
    #print priority

# create the new merged cluster
    merged=priority[1]
    #print merged
    merged_list=sum(priority[1],[])
    #print merged_list
    new={}
    new["points"]=merged_list
    new["centroid"]=centroid(data_lists,merged_list)
    #print "new", new

# delete merged clusters
    for i in merged:
        del cluster[str(i)]
    #print len(cluster)
    #print cluster
    #print "c", cluster

    # add new cluster
    cluster[str(merged_list)] = new
    #print cluster

    x= list(cluster.values())
    queue=pair_cluster(x)

#print cluster

output={}
id=0
for data in datas:
    for i in range(len(data)-1):
        data[i] = float(data[i])
    output[id]=data
    id=id+1

#filename="output_cluster_3.txt"
filename="output_cluster_" + sys.argv[2]+".txt"
output_file = open(filename, "w")

# print output class is a string
wrong=0
for i in cluster.values():
    cluster_list=i["points"]
    count = {}
    for j in sorted(cluster_list):
        count[output[j][-1]] = count.get(output[j][-1], 0) + 1
        cluster_name=max(count, key=count.get)
        if output[j][-1]!=cluster_name:
            wrong=wrong+1
    output_file.write("cluster:"+ str(cluster_name)+"\n")
    for j in sorted(cluster_list):
        output_file.write(str(output[j])+"\n")
    output_file.write ("Number of points in this cluster:"+str(len(cluster_list))+"\n"+"\n")

output_file.write ("Number of points wrongly assigned:"+str(wrong))
