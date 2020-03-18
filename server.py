from flask import Flask,request,redirect,url_for

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
	return  default_sort(app.data) + upload_form()

@app.route("/new_csv", methods=['POST'])
def new_csv():
	file = request.files.get('filename')
	if file:
		raw = file.read();
		lines = raw.decode('utf-8')
		lines = lines.split('\n');
		app.data = parse_csv(lines)
		return redirect(url_for('home'))
	else:
		#TODO show error message to user 
		return redirect(url_for('home'))

def parse_csv(file):
	print("file")
	print(file)
	print(len(file))
	# split file into lines
	lines = [str(line).split(",") for line in file if line]
	for line in lines:
		print(line)
		line[3] = line[3].rstrip() #str.rstrip() remove trailing whitepsace
	return lines[1:] # do not include header row



def table(data):
	entry_template = "<tr> <th>{a}</th> <th>{b}</th> <th>{c}</th> <th>{d}</th> </tr>"
	res = "<table style='width:100%'>"
	for entry in data:
		res += entry_template.format(a=entry[0],b=entry[1],c=entry[2],d=entry[3])
	res += "</table>"
	return res

def upload_form():
	#enctype attribute is necessary for flask to see filename in request.files
	res =  "<form method='post' action='/new_csv' enctype=multipart/form-data>" 
	res += "<input type='file' id='csv' name='filename'/>"
	res += "<button type='submit'>Upload!</button>"
	res += "</form>"
	return res

#todo: potentially use sorted() rather than .sort() to not mutate global data	
def default_sort(data):
	data.sort(key=lambda line: line[2])
	return table(data)

if __name__=="__main__":
	with open("trains.csv") as file:
		data = parse_csv(file.readlines())	
		app.data = data
		app.run()	

