import requests
import cv2
import imutils
import numpy as np
import webbrowser


img = cv2.imread('tester.jpg')


w_width = 500
w_height = 300
cv2.resizeWindow('blokshot', w_width, w_height)

def drawFrame():

    cv2.line(img, (30,20), (40,20), (255, 0, 0), 3)
    cv2.line(img, (30,20), (30,280), (255, 0, 0), 3)
    cv2.line(img, (30,280), (40,280), (255, 0, 0), 3)

    cv2.line(img, (480,20), (490,20), (255, 0, 0), 3)
    cv2.line(img, (490,20), (490,280), (255, 0, 0), 3)
    cv2.line(img, (480,280), (490,280), (255, 0, 0), 3)


    cv2.line(img, (260,140), (260,160), (0, 255, 255), 3)
    cv2.line(img, (250,150), (270,150), (0, 255, 255), 3)

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def getColorMask(hsv, color):
    color = color.upper()
    if(color == "RED" or color == "R"):
        lower_red = np.array([0,50,50])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170,50,50])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        mask = mask0 + mask1

    elif(color == "GREEN" or color == "G"):

        sensitivity = 15
        lower_green = np.array([60 - sensitivity, 100, 50])
        upper_green = np.array([60 + sensitivity, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

    elif(color == "BLACK" or color == "B"):
        lower_blk = np.array([0,0,0])
        upper_blk = np.array([255, 255, 30])
        mask = cv2.inRange(hsv, lower_blk, upper_blk)

    else:
        print("You did not input a valid color")
        mask = 0;

    return mask

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
blackmask = getColorMask(hsv,"b")
cv2.imshow('blk', blackmask)
redmask = getColorMask(hsv, "r")
rowList = []


while True:

# Finds image divider components (black)

    img2, bcntrs, hierarchy = cv2.findContours(blackmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Adds divider components to array

    bList = []
    if bcntrs is not None:
        for i in bcntrs:
            x,y,w,h = cv2.boundingRect(i)
            if (w > 60):
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

            line = [y, 0]
            bList.append(line)

    cv2.imshow('blk', blackmask)

    bList = bList[::-1]

# Finds image section components (red)

    img3, rcntrs, hierarchy = cv2.findContours(redmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Adds section components to array

    if rcntrs is not None:
        for i in rcntrs:
            x,y,w,h = cv2.boundingRect(i)
            if (w > 40 and h > 40):
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            num = 0
            rCt = 1

            for b in range(len(bList)-1):
                    if (y > bList[num][0] and y < bList[rCt][0]):
                        bList[num][1] = bList[num][1] + 1
                    num = num + 1
                    rCt = rCt + 1


    cv2.imshow('CamShot', img)
    cv2.imshow('red', redmask)


    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break

# Creates file, uses array data

f = open('blokshot.html','w')

message = """
<html>
<head>
    <title>blokshot</title>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="description" content="graphic to web app">
    <meta name="keywords" content="developer, opencv, hackru" />
    <meta name="author" content="Janice Konadu">
    <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
    <style type="text/css">
        body{
            font-family: 'Montserrat', sans-serif;
            background-color: #ffef62;
            color: #222;
        }

        section{
            width: 80%;
            margin: 0 auto;
            font-size: 12pt;
            text-align: center;
            height: 100vh;
        }

        .logo{
            margin: 0 auto;
        }

        .logo, .cont{
            margin-top: 250px;
        }

        p, h1{
            padding-right: 40px;
            padding-left: 40px;
        }

        h1{
            text-transform: uppercase;
            margin-bottom: 2px;
            font-weight: '700';
        }

        hr{
            width: 50px;
            border: 3px solid #222;
            margin-top: 10px;
            margin-bottom: 10px;

        }
    </style>
</head>
<body>
    <section>
        <img class="logo" src="bk.jpg" />
    </section>
"""

div = """
<div class="cont">
    <h1>This is a header</h1>
    <h3></h3>
    <hr>
    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ullamcorper tempus dignissim. Aenean ut semper risus. Aliquam erat volutpat. Aenean sit amet ultricies nunc, tincidunt rutrum nisl. Maecenas eget egestas odio. Suspendisse id bibendum neque, ac volutpat neque. Vestibulum tristique lorem sodales semper feugiat. Pellentesque tellus enim, euismod ultricies efficitur ut, varius vitae dolor. Sed sed mi quis mauris placerat bibendum. Phasellus porta orci vel orci sagittis, vitae
        tristique justo feugiat. Praesent quis accumsan orci, vel mattis leo. Aenean magna leo, commodo et faucibus vel, porta ac massa. Maecenas vitae lorem ornare, ornare urna ut, auctor nunc. Fusce rhoncus rutrum consequat.
    </p>
</div>
"""

for i in bList:
    bDiv = i[:-1]
    if (bDiv == 0):
        nu = 0
        col = "100%"
    else:
        nu = 100 / bDiv
        col = (str(nu) + "% ") * (bDiv)

    message = message + " <section style=\"" + "display: grid; grid-template-columns: " + col + ";\">" + div*bDiv + "</section>\n"

message = message + """

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script>

        $(function() {
        $('body').hide().fadeIn(350);

        });

    </script>


    </body></html>"""
print (message)

f.write(message)
f.close()

# Opens browser

filename = 'C:///Users/jkona/Desktop/blokshot/' + 'blokshot.html'

webbrowser.open_new_tab(filename)
