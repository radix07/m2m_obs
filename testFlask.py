# The following lines require manual changes 
username = "pgSatterlee" # enter your username
password = "Pgecs-2322" # enter your password 
# Nothing below this line should need to be changed
# -------------------------------------------------
import httplib
import base64 

# create HTTP basic authentication string, this consists of 
# "username:password" base64 encoded 
auth = base64.encodestring("%s:%s"%(username,password))[:-1]
webservice = httplib.HTTP("login.etherios.com",80)

message = """<sci_request version="1.0"> 
  <send_message cache="false"> 
    <targets> 
      <device id="00000000-00000000-00042dFF-FF0418fb"/>
    </targets> 
    <rci_request version="1.1"> 
      <query_setting/>
    </rci_request>
  </send_message>
</sci_request>
"""
webservice = httplib.HTTP("login.etherios.com",80)

# to what URL to send the request with a given HTTP method
webservice.putrequest("POST", "/ws/sci")

# add the authorization string into the HTTP header
webservice.putheader("Authorization", "Basic %s"%auth)
webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
webservice.putheader("Content-length", "%d" % len(message))
webservice.endheaders()
webservice.send(message)

# get the response
statuscode, statusmessage, header = webservice.getreply()
response_body = webservice.getfile().read()

# print the output to standard out
print (statuscode, statusmessage)
print response_body

'''
# to what URL to send the request with a given HTTP method
webservice.putrequest("GET", "/ws/DataPoint/0000000-00000000-00042dFF-FF0418fb/EngineSpeedFloat")
#0000000-00000000-00042dFF-FF0418fb/EngineSpeedFloat
# add the authorization string into the HTTP header
webservice.putheader("Authorization", "Basic %s"%auth)
webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
webservice.endheaders()

# get the response
statuscode, statusmessage, header = webservice.getreply()
response_body = webservice.getfile().read()

# print the output to standard out
print (statuscode, statusmessage)
print response_body

'''
