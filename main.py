import cv2
import PySimpleGUI as sg

def gs(imf, imgb, smin, smax):
  fhsv = cv2.cvtColor(imgf, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(fhsv, smin, smax)

  mskf = cv2.bitwise_and(imgf, imgf, mask=255-mask)
  mskb = cv2.bitwise_and(imgb, imgb, mask=mask)
  sum = mskb+mskf
  return cv2.imencode('.png', sum)[1].tobytes()

sg.theme('DarkAmber')

imgf = cv2.imread("green.jpg")
imgb = cv2.imread("background.jpg")
imgb = cv2.resize(imgb, (imgf.shape[1], imgf.shape[0]))

h_min = 50
h_max = 65
s_min = 0
s_max = 255
v_min = 35
v_max = 255

layout = [
  [sg.Frame('Hue',[[      
        sg.Slider(range=(0, 255), size=(15, 10), orientation='h', default_value=1, key="h_min")],           
        [sg.Slider(range=(0, 255), orientation='h', size=(15, 10), default_value=1, key="h_max")]]),
        sg.Frame('Saturation',[[     
        sg.Slider(range=(0, 255), size=(15, 10), orientation='h', default_value=1, key="s_min")],           
        [sg.Slider(range=(0, 255), orientation='h', size=(15, 10), default_value=1, key="s_max" 
        )]]),
        sg.Frame('Value',[[      
        sg.Slider(range=(0, 255), size=(15, 10), orientation='h', default_value=1, key="v_min")],           
        [sg.Slider(range=(0, 255), orientation='h', size=(15, 10), default_value=1, key="v_max")]]),
        ],
  
  [sg.Image(data=gs(imgf, imgb, (h_min, s_min, v_min), (h_max, s_max, v_max)))]
]

window = sg.Window('Green Screen', layout)

while True:
  event, values = window.read()
  if event == sg.WINDOW_CLOSED or event == 'Quit':
    break
  elif event in ('h_min', 'h_max', 's_min', 's_max', 'v_min', 'v_max'):
    h_min = int(values['h_min'])
    h_max = int(values['h_max'])
    s_min = int(values['s_min'])
    s_max = int(values['s_max'])
    v_min = int(values['v_min'])
    v_max = int(values['v_max'])
    window['image'].Update(data=gs(imgf, imgb, (h_min, s_min, v_min), (h_max, s_max, v_max)))
window.close()