import pandas as pd

def gen_node():

    sell = []
    buy = []    

    df = pd.read_csv('Iron_dealers_data.csv')

    sellers = df["Seller ID"].unique()
    for ss in sellers:
        sell.append(ss)
    buyers = df["Buyer ID"].unique()
    for bb in buyers:
        buy.append(bb)
    #sell.sort()
    #print(sorted(sell))
    #print(sorted(buy))
    #print("Union")
    union_list = sorted(set(list(set(sell))+list(set(buy))))
    union_list_str = []
    for u in union_list:
        union_list_str.append("\n"+str(u))
    f = open("nodes_unique.txt", "w")
    f.writelines(union_list_str)
    f.close()
def gen_bad_node():
    df = pd.read_csv("bad.csv")
    bad_entity = df["Bad Id"]
    bad = []
    for b in bad_entity:
        bad.append("\n"+str(b))
    bad.sort()
    f = open("nodes_unique_bad.txt", "w")
    f.writelines(bad)
    f.close()
def gen_edge():
    df = pd.read_csv('Iron_dealers_data.csv')
    df = df.groupby(['Seller ID','Buyer ID']).size().reset_index().rename(columns={0:'count'})
    buyer = df["Buyer ID"]
    seller = df["Seller ID"]
    write_list = []
    for i in range(len(buyer)):
        write_list.append(str(seller[i])+","+str(buyer[i])+"\n")
    f = open("edge_unique.txt", "w")
    f.writelines(write_list)
    f.close()
gen_edge()