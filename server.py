from flask import Flask,request,redirect,url_for

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
	if not app.data: 
		return options()
	sort_by = request.args.get("sort_by")
	if sort_by:
		return options() + custom_sort(std_table, sort_by)
	return  options() + default_sort(std_table) 

@app.route("/edit", methods=['GET', 'POST'])
def edit():
	if not app.data: 
		return redirect(url_for('home'))
	if request.method=='GET':
		try:
			row,col = int(request.args['row']), int(request.args['col'])
			return options() + edit_item_table(app.data,row,col)

		except:
			return options() + edit_link_table(app.data)
	else:
		new_entry = request.form.get('new_entry')
		row,col = int(request.args['row']), int(request.args['col'])
		app.data[row][col] = new_entry
		return redirect(url_for('home'))

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
	repeats = set()
	lines = []
	for raw_line in file:
		if not raw_line: 
			continue
		line = str(raw_line).split(",")	
		line = [item.strip() for item in line] 
		tup = tuple(line)
		if tup not in repeats:
			repeats.add(tup)
			lines.append(line)
	return lines # do not include header row


#python string template, handles text and edit links
entry_template = "<tr> <th>{}</th> <th>{}</th> <th>{}</th> <th>{}</th> </tr>"

def headers(names):
	link_template =  "<strong><a href='/?sort_by={n}'>{n}</a></strong>"
	links = [link_template.format(n=name) for name in names]
	return entry_template.format(*links)

def std_table(data):
	res = "<table style='width:100%'>"
	res += headers(data[0])
	for entry in data[1:]:
		res += entry_template.format(*entry)
	res += "</table>"
	return res


def edit_link_table(data):
	res = "<table style='width:100%'>"
	for (i,entry) in enumerate(data):
		#header row is a special case with no links - cannot edit category names
		if i==0:
			res += entry_template.format(*entry)
		else:
			entry_with_links = [edit_link(i,j,text) for (j,text) in enumerate(entry)]
			res += entry_template.format(*entry_with_links)
	res += "</table>"
	return res

def edit_item_table(data,row,col):
	res = "<table style='width:100%'>"
	for (i,entry) in enumerate(data):
		if i==row:
			e = entry.copy()
			e[col] = edit_item(row,col)
			res += entry_template.format(*e)
		else:
			res += entry_template.format(*entry)
	res += "</table>"
	return res

def edit_link(row,col,text):
	return text + "<a href='/edit?row={}&col={}'>(edit)</a>".format(row,col)

def edit_item(row,col):
	res =  "<form method='post' action='/edit?row={}&col={}'>".format(row,col)
	res += "<input type='text' name='new_entry'/>"
	res += "<button type='submit'>Submit!</button>"
	res += "</form>"
	return res

def options():
	#enctype attribute is necessary for flask to see filename in request.files
	res =  "<form method='post' action='/new_csv' enctype=multipart/form-data>" 
	res += "<input type='file' id='csv' name='filename'/>"
	res += "<button type='submit'>Upload!</button>"
	res += "<p><a href='/edit'>Edit</a>  <a href='/'>Home</a></p>"
	res += "</form>"
	return res

def default_sort(table):
	data = [app.data[0]] + sorted(app.data[1:], key=lambda line: line[2])
	app.data = data
	return table(data)

def custom_sort(table, sort_by):
	category_index = None  
	for (i,header_name) in enumerate(app.data[0]):
		if header_name == sort_by:
			category_index = i	

	if category_index==None:
		category_index = 0

	data = [app.data[0]] + sorted(app.data[1:], key=lambda line: line[category_index])
	app.data = data
	return table(data)

if __name__=="__main__":
	try: 
		with open("trains.csv") as file:
			data = parse_csv(file.readlines())	
			app.data = data
			app.run()	
	except:
		app.data = []
		app.run()