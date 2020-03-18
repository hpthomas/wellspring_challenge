from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
	return default_sort(app.data)

def parse_csv(file):
	# split file into lines
	lines = [line.split(",") for line in file]
	for line in lines:
		line[3] = line[3].strip("\r\n")
	return lines[1:] # do not include headeer row


table_entry = """<tr>
    <th>{a}</th>
    <th>{b}</th>
    <th>{c}</th>
    <th>{d}</th>
 </tr>"""
def default_sort(data):
	data.sort(key=lambda line: line[2])
	res = "<table style='width:100%'>"
	res += table_entry.format(a="Train Line",b="Route",c="Run Number",d="Operator")
	for entry in data:
		res += table_entry.format(a=entry[0],b=entry[1],c=entry[2],d=entry[3])
	res+="</table>"
	return res

if __name__=="__main__":
	with open("trains.csv") as file:
		data = parse_csv(file)	
		app.data = data
		app.run()	

