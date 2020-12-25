from flask import Flask,render_template,flash, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
import os
import random
import string
from utils import *
from Shape import *
from SVGElements.SVGCircle import *
from SVGElements.SVGPath import *
from SVGElements.SVGPolygon import *
from SVGElements.SVGRect import *
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

UPLOAD_FOLDER = './static/input'
ALLOWED_EXTENSIONS = {'svg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)

@app.route('/', methods=['GET'])
def home():
    return render_template('upload.html')

@app.route('/upload-svg',methods=['POST'])
def upload_svg():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_id=get_random_string(100)
        upload_dir=os.path.join(app.config['UPLOAD_FOLDER'],upload_id)
        os.mkdir(upload_dir)
        file.save(os.path.join(upload_dir, filename))
        return redirect(url_for('uploaded_file',
                                    upload_id=upload_id))
    else :
        return redirect(url_for('home'))


@app.route('/<upload_id>',methods=['GET'])
def uploaded_file(upload_id):
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],upload_id)):
        file=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],upload_id))
        # read the SVG file
        file_path="./static/input/"+upload_id+"/"+file[0]
        file_name=file[0]
        try :
            doc = minidom.parse(file_path)
        except :
            print("Error ! "+file_path+" does not exist ! ")
            exit()
        else :
            svg_shapes=parseSVGfile(file_path)

            shapesJS=[]
            for svg_shape in svg_shapes:
                shapesJS.append(svg_shape.toJSON())

            p=Parameters()

            #Extract the max and the Min for the view Box
            for shape in svg_shapes:
                __path=shape.renderStroke(p)

            dimension={}
            dimension["minX"]=p.minX
            dimension["minY"]=p.minY
            dimension["width"]=p.maxX-p.minX
            dimension["height"]=p.maxY-p.minY

            return render_template('uploaded.html',viewport=dimension,
            file_name=file_name,shapes=shapesJS)
    else :
        return render_template('upload.html')

@app.route('/generateGCode',methods=['POST'])
def generate_GCode():
    data=request.get_json();
    parametersJS=data["parameters"]
    SVGshapesJS=data["shapes"]
    upload_id=re.findall(r".*/([a-zA-Z]*)",data["url"])[0]

    print(upload_id)
    p=Parameters()
    state=State()

    p.offsetX=parametersJS["Xoffset"]
    p.offsetY=parametersJS["Yoffset"]
    p.bedXdim=parametersJS["bedXdim"]
    p.bedYdim=parametersJS["bedYdim"]
    p.sizeFactor=parametersJS["sizeFactor"]
    p.penUp=parametersJS["penUp"]
    p.penDown=parametersJS["penDown"]
    p.xFlip=parametersJS["xFlip"]
    p.yFlip=parametersJS["yFlip"]
    topMargin=parametersJS["topMargin"]
    botMargin=parametersJS["botMargin"]
    leftMargin=parametersJS["leftMargin"]
    rightMargin=parametersJS["rightMargin"]
    p.setMargins(top=topMargin,
                 bot=botMargin,
                 left=leftMargin,
                 right=rightMargin)
    p.closeTolerance=parametersJS["closeTolerance"]
    p.alwaysZhop=parametersJS["alwaysZhop"]

    for shapeJS in SVGshapesJS:
        __path=parseSingleJSShape(shapeJS,p)

    p.bedRatio=p.availableYdim/p.availableXdim
    p.svgRatio=(p.maxY-p.minY)/(p.maxX-p.minX)
    p.setReelInterspace(parametersJS["realInterspace"])
    p.zHopTolerance=parametersJS["zHopTolerance"]

    shapes=parseJSShapes(SVGshapesJS,p,state)

    colors=list(set([shape.wallColor for shape in shapes]))
    print(colors)
    finalGCode=""
    finalGCode+=getStartCode(p)
    for color in colors :
        finalGCode+=";COLOR:{}\n".format(color)
        finalGCode+=getPauseCode(p.offsetX+5,
                                 p.offsetY+5,
                                 p.penDown,
                                 p,
                                 state)
        for shape in shapes :
            if shape.wallColor==color :
                if shape.wall!=None:
                    finalGCode+=shape.codeWall(p,state)
                if shape.skin!=None:
                    finalGCode+=shape.codeSkin(p,state)

    finalGCode+=getEndCode(p)

    with open("output.gcode","w") as file :
        file.write(finalGCode)
    plt.clf()
    plt.axis([0, 230, 0, 230])
    plt.vlines(230-p.offsetX,ymin=0,ymax=230,linestyles='dashed')
    plt.vlines(230-p.offsetX-p.rightMargin,ymin=0,ymax=230,linestyles='dashed',color='red')
    plt.vlines(p.leftMargin,ymin=0,ymax=230,linestyles='dashed',color='red')
    plt.hlines(230-p.offsetY,xmin=0,xmax=230,linestyles='dashed')
    plt.hlines(230-p.offsetY-p.topMargin,xmin=0,xmax=230,linestyles='dashed',color='red')
    plt.hlines(p.bottomMargin,xmin=0,xmax=230,linestyles='dashed',color='red')
    for index in range(0,len(state.PltX)):
        plt.plot(state.PltX[index],state.PltY[index],'b',linewidth="0.5")

    plt.axes().set_aspect('equal')
    now=datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
    plt.savefig(os.path.join("./static/input",upload_id,date_time+"-preview.png"))

    data={}
    data["datetime"]=date_time
    data["upload_id"]=upload_id
    data["preview"]=True
    return jsonify(data),200
