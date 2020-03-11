from ncclient import manager
import xml.dom.minidom
import socket

node = "127.0.0.1"
#Connection Establishment
def connect(node):
    try:
        device_connection = manager.connect(host = node, port = '2222', username = 'admin', password = 'Cisco!123', hostkey_verify = False, device_params={'name':'nexus'})
        return device_connection
    except:
        print("Unable to connect " + node)

#Task 1 - NXOS version checker.
def getVersion(node):
    device_connection = connect(node)
    version = """
               <show xmlns="http://www.cisco.com/nxos:1.0">
                   <version>
                   </version>
               </show>
              """
    try:
        netconf_output = device_connection.get(('subtree', version))
        xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
        version = xml_doc.getElementsByTagName("mod:nxos_ver_str")
        return "Version "+str(version[0].firstChild.nodeValue)
    except:
        return "Unable to get this node version"

#Task 2 - Hostname Setter
def changeHostname(node, hostname):
    m = connect(node)
    HOSTNAME = '''
            <configure xmlns="http://www.cisco.com/nxos:1.0">
                <__XML__MODE__exec_configure>
                    <hostname>
                        <name>%s</name>
                    </hostname>
                </__XML__MODE__exec_configure>   
            </configure>  
'''
    configuration = ''
    configuration += '<config>'
    configuration += HOSTNAME %hostname
    configuration += '</config>'
    try:
         m.edit_config(target='running', config= configuration)
         return "Hostname changed to "+hostname
    except:
         return "Unable to change this node hostname"  

def Main():
    host = "127.0.0.1"
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(5)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        message = conn.recv(1024).decode()
        if message == "show version":
                message = getVersion(node)
        elif message.split()[0] == "hostname":
                hostname = message.split()[1]
                message = changeHostname(node,hostname)               
        else:
                message = "I do not understand"
        conn.send(message.encode())
    conn.close()

if __name__ == '__main__':
        Main()
