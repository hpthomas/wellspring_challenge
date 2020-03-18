from flask import Flask,request,redirect,url_for

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
	sort_by = request.args.get("sort_by")
	if sort_by:
		return custom_sort(sort_by) + upload_form()
	return  default_sort() + upload_form()

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
	# split file into lines
	lines = [str(line).split(",") for line in file if line]
	for line in lines:
		line[3] = line[3].rstrip() #str.rstrip() remove trailing whitepsace
	return lines # do not include header row



entry_template = "<tr> <th>{}</th> <th>{}</th> <th>{}</th> <th>{}</th> </tr>"

def headers(names):
	link_template =  "<strong><a href='/?sort_by={n}'>{n}</a></strong>"
	links = [link_template.format(n=name) for name in names]
	return entry_template.format(*links)

def table(data):
	res = "<table style='width:100%'>"
	res += headers(data[0])
	for entry in data[1:]:
		res += entry_template.format(entry[0],entry[1],entry[2],entry[3])
	res += "</table>"
	return res

def upload_form():
	#enctype attribute is necessary for flask to see filename in request.files
	res =  "<form method='post' action='/new_csv' enctype=multipart/form-data>" 
	res += "<input type='file' id='csv' name='filename'/>"
	res += "<button type='submit'>Upload!</button>"
	res += "</form>"
	return res

def default_sort():
	data = [app.data[0]] + sorted(app.data[1:], key=lambda line: line[2])
	return table(data)

def custom_sort(sort_by):
	category_index = None  
	for (i,header_name) in enumerate(app.data[0]):
		if header_name == sort_by:
			category_index = i	

	if category_index==None:
		print("ERROR ON SORT")
		cateegory_index = 0

	data = [app.data[0]] + sorted(app.data[1:], key=lambda line: line[category_index])
	return table(data)

if __name__=="__main__":
	with open("trains.csv") as file:
		data = parse_csv(file.readlines())	
		app.data = data
		app.run()	

