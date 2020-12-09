from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def server_message_root():
	with open ("deployment_schedule.json", "r") as f:
		read_data = f.read()
#	print ("read_data: ", read_data)
	
#	return jsonify({"message": "{ \"environment\":\"acai\", \"release\":\"RELEASE_2020.11.23.22.01.22.00\", \"deploy_time\":\"2020-11-26:17:00\" }"})
#	return '{ "environment":"acai", "release":"RELEASE_2020.11.23.22.01.22.00", "deploy_time":"2020-11-26:17:00" }'
	return read_data

@app.route("/query")
def query():
	with open ("deployment_schedule.json", "r") as f:
		read_data = f.read()
	print ("read_data: ", read_data)

	read_data_json = json.loads(read_data)
	print ("-----")
	print (read_data_json)

	if request.args:
		# query string serialized as a Python dictionary
		args = request.args
		if "env" in args:
			requester_env = args["env"]
			print ("env: ", requester_env)

			env_not_found=0
			for keyval in read_data_json:
				#print (keyval['environment'])
				if requester_env.lower() == keyval['environment'].lower():
					print (keyval['release'])
					ret = keyval['release']
					env_not_found = 1

			if env_not_found ==	0:
				ret = "Please pass env as query string"

		return ret, 200
	else:
		return "No query string received", 200

@app.route("/ack")
def ack():
	if request.args:
		# query string serialized as a Python dictionary
		args = request.args
		if "env" in args:
			env_name = args["env"]
			print ("env: ", env_name)

		if "result" in args:
			result_val = args["result"]
			print ("result_val: ", result_val)

		if "release" in args:
			release_deployed = args["release"]
			print ("release_deployed: ", release_deployed)

		now = datetime.now()
		dt_str = now.strftime("%Y/%m/%d-%H:%M:%S")
		print (dt_str)

		log_str= env_name+","+result_val+","+release_deployed+","+dt_str
		log_json = json.dumps (log_str)
		with open ("deployment.log", "r+") as fw:
			fw.write(log_str)

		return log_json , 200
	else:
		return "No query string received", 200

if __name__ == '__main__':
 app.run()


