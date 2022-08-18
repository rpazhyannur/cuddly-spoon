#!/usr/bin/env python
# coding: utf-8

# In[420]:


# code to create YAML file


# In[421]:


import yaml


# In[422]:


def getSubnet(ipaddr, subnetMask):
    # ipaddr and subnetMask are in a.b.c.d format
    ipList = ipaddr.split('.')
    if len(ipList) != 4:
        raise Exception ('Incorrect IP address format')
    maskList = subnetMask.split('.')
    if len(maskList) != 4:
        raise Exception ('Incorrect Subnet mask format')
    return('.'.join([str(int(ipList[i])&int(maskList[i])) for i in range(4)])) #not checking whether value between 0 and 255


# In[423]:


def getOnes (number):
    # gets the number of ones when number is expressed in binary
    count = 0
    for i in range(8):
        if (number % 2) == 1:
            count = count + 1
        number = number >> 1
    return(count)


# In[424]:


def getSlashNumber(ipaddr):
    ipList = ipaddr.split('.')
    if len(ipList) != 4:
        raise Exception ('Incorrect IP address format')
    return sum([getOnes(int(ipList[i])) for i in range(4)])


# In[425]:


def getRoute(ipaddr, subnetMask):
    try:
        subnet = getSubnet(ipaddr,subnetMask)
        slashNumber = getSlashNumber(subnetMask)
        return subnet + '/' + str(slashNumber)
    except Exception as e:
        print(e)
        return (None)


# In[426]:


def createNetplanConfig(interfaceName,routes):
    netplanConfig = {'network':{'ethernets':{interfaceName:{'routes': routes}}}}
    return yaml.dump(netplanConfig)


# ## How to create Netplan YAML file from DNN Configuration

# In[427]:


dnn1 =  {'defGw': '192.168.1.1', 'subnetMask':'255.255.255.0'}
dnn2 =  {'defGw': '10.10.20.1', 'subnetMask':'255.255.0.0'}
dnnList = [dnn1, dnn2]


# ## Create routes 

# In[428]:


viaAddr = '10.1.1.2'
routes = [{ 'to': getRoute(dnn['defGw'],dnn['subnetMask']), 'via': viaAddr} for dnn in dnnList]
print(routes)


# ## Create YAML configuration

# In[429]:


config=createNetplanConfig('en01',routes)


# In[430]:


print(config)


# In[ ]:




