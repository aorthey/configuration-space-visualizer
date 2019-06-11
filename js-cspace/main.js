//*****************************************************************************
//Control Elements
//*****************************************************************************
function userEventSlider(event) {
  documentState.robot.l1 = lengthL1.value;
  documentState.robot.l2 = lengthL2.value;
  documentState.robot.update(qL1.value, qL2.value);
  documentState.valid = false;
}

function CreateSlider(name, min, max, step, value){
  var lines = '';
  lines += '<div class="slidecontainer">';
  lines += '<span>'+name+' </span>';
;
  lines += '<span style="font-weight:bold;color:black">'+min+' \<= </span>';
  lines += '<span id="'+name+'.value" style="font-weight:bold;color:black"></span>';
  lines += '<span style="font-weight:bold;color:black">\<= '+max+' </span>';
  lines += '<input type="range" ';
  lines += 'min="'+min+'" ' ;
  lines += 'max="'+max+'" ' ;
  lines += 'step="'+step+'" ' ;
  lines += 'value="'+value+'" ' ;
  lines += 'class="slider" id="'+name+'">';
  lines += '</div>';
  document.write(lines);

  var s = document.getElementById(name);
  var output = document.getElementById(name+".value");
  output.innerHTML = s.value;
  s.addEventListener("click", userEventSlider);

  s.oninput = function() {
    output.innerHTML = this.value;
  }
  return s;
}


//*****************************************************************************
//documentState
//*****************************************************************************
function DocumentState(canvas, cspaceCanvas, qspaceCanvas) {
  this.canvas = canvas;
  this.width = canvas.width;
  this.height = canvas.height;
  this.ctx = canvas.getContext('2d');
  this.ctx.imageSmoothingEnabled = true;

  this.canvas_cspace = new CanvasConfigurationSpace(cspaceCanvas);
  this.canvas_qspace = new CanvasConfigurationSpace(qspaceCanvas);
  this.canvas_qspace.qspace = true;

  var stylePaddingLeft, stylePaddingTop, styleBorderLeft, styleBorderTop;
  if (document.defaultView && document.defaultView.getComputedStyle) {
    this.stylePaddingLeft = parseInt(document.defaultView.getComputedStyle(canvas, null)['paddingLeft'], 10)      || 0;
    this.stylePaddingTop  = parseInt(document.defaultView.getComputedStyle(canvas, null)['paddingTop'], 10)       || 0;
    this.styleBorderLeft  = parseInt(document.defaultView.getComputedStyle(canvas, null)['borderLeftWidth'], 10)  || 0;
    this.styleBorderTop   = parseInt(document.defaultView.getComputedStyle(canvas, null)['borderTopWidth'], 10)   || 0;
  }
  // Some pages have fixed-position bars (like the stumbleupon bar) at the top or left of the page
  // They will mess up mouse coordinates and this fixes that
  var html = document.body.parentNode;
  this.htmlTop = html.offsetTop;
  this.htmlLeft = html.offsetLeft;

  this.valid = false; // when set to false, the canvas will redraw everything
  this.obstacles = [];

  this.robot = new Robot();
  this.canvas_cspace.robot = this.robot;
  this.canvas_qspace.robot = this.robot;

  this.dragging = false; // Keep track of when we are dragging
  this.selection = null;
  this.dragoffx = 0;
  this.dragoffy = 0;
  var myState = this;
  
  canvas.addEventListener('selectstart', function(e) { e.preventDefault(); return false; }, false);
  canvas.addEventListener('mousedown', function(e) {
    var mouse = myState.getMouse(e);
    var mx = mouse.x;
    var my = mouse.y;
    var obstacles = myState.obstacles;
    var l = obstacles.length;
    for (var i = l-1; i >= 0; i--) {
      if (obstacles[i].contains(mx, my)) {
        var mySel = obstacles[i];
        // Keep track of where in the object we clicked
        // so we can move it smoothly (see mousemove)
        myState.dragoffx = mx - mySel.x;
        myState.dragoffy = my - mySel.y;
        myState.dragging = true;
        myState.selection = mySel;
        myState.valid = false;
        return;
      }
    }
    // havent returned means we have failed to select anything.
    // If there was an object selected, we deselect it
    if (myState.selection) {
      myState.selection = null;
      myState.valid = false;
    }
  }, true);
  canvas.addEventListener('mousemove', function(e) {
    if (myState.dragging){
      var mouse = myState.getMouse(e);
      myState.selection.x = mouse.x - myState.dragoffx;
      myState.selection.y = mouse.y - myState.dragoffy;   
      myState.valid = false;
    }
  }, true);
  canvas.addEventListener('mouseup', function(e) {
    myState.dragging = false;
    if (myState.selection) {
      myState.selection = null;
      myState.valid = false;
    }
  }, true);
  // double click for making new obstacles
  canvas.addEventListener('dblclick', function(e) {
    var mouse = myState.getMouse(e);
    myState.addObstacle(new Obstacle(mouse.x - 10, mouse.y - 10, 50, 50));
  }, true);

  this.selectionColor = 'red';
  this.selectionWidth = 5;  
  this.interval = 30;
  setInterval(function() { myState.draw(); }, myState.interval);
}
var addEvent = function(object, type, callback) {
  if (object == null || typeof(object) == 'undefined') return;
  if (object.addEventListener) {
      object.addEventListener(type, callback, false);
  } else if (object.attachEvent) {
      object.attachEvent("on" + type, callback);
  } else {
      object["on"+type] = callback;
  }
};

DocumentState.prototype.addObstacle = function(o) {
  this.obstacles.push(o);
  this.valid = false;
}

DocumentState.prototype.clear = function() {
  this.ctx.clearRect(0, 0, this.width, this.height);
  this.canvas_cspace.clear();
  this.canvas_qspace.clear();
}

DocumentState.prototype.draw = function() {
  // if our state is invalid, redraw and validate!
  if (!this.valid) {
    var ctx = this.ctx;
    var obstacles = this.obstacles;
    this.clear();
    
    // ** Add stuff you want drawn in the background all the time here **
    
    // draw all obstacles
    var l = obstacles.length;
    for (var i = 0; i < l; i++) {
      var obstacle = obstacles[i];
      // We can skip the drawing of elements that have moved off the screen:
      if (obstacle.x > this.width || obstacle.y > this.height ||
          obstacle.x + obstacle.w < 0 || obstacle.y + obstacle.h < 0) continue;
      obstacle.draw(ctx);
    }
    
    // draw selection
    // right now this is just a stroke along the edge of the selected obstacle
    if (this.selection != null) {
      ctx.strokeStyle = this.selectionColor;
      ctx.lineWidth = this.selectionWidth;
      var mySel = this.selection;
      ctx.strokeRect(mySel.x,mySel.y,mySel.w,mySel.h);
    }
    
    this.robot.draw(ctx);
    this.canvas_cspace.draw();
    this.canvas_qspace.draw();
    this.valid = true;
  }
}

DocumentState.prototype.getMouse = function(e) {
  var element = this.canvas, offsetX = 0, offsetY = 0, mx, my;
  if (element.offsetParent !== undefined) {
    do {
      offsetX += element.offsetLeft;
      offsetY += element.offsetTop;
    } while ((element = element.offsetParent));
  }
  offsetX += this.stylePaddingLeft + this.styleBorderLeft + this.htmlLeft;
  offsetY += this.stylePaddingTop + this.styleBorderTop + this.htmlTop;

  mx = e.pageX - offsetX;
  my = e.pageY - offsetY;
  outputD3.innerHTML = mx;
  outputD4.innerHTML = my;
  return {x: mx, y: my};
}

//Window Resize Event
DocumentState.prototype.windowResizeEvent = function() {
  outputD1.innerHTML = window.innerWidth;
  outputD2.innerHTML = window.innerHeight;
  workspace.width = 0.8*window.innerWidth;
  workspace.height = workspace.width;//0.6*window.innerHeight;
  if(workspace.height > 0.6*window.innerHeight){
    workspace.width = 0.6*window.innerHeight;
    workspace.height = workspace.width;//0.6*window.innerHeight;
  }
  cspace.width = workspace.width;
  cspace.height = workspace.height;
  qspace.width = workspace.width;
  qspace.height = workspace.height;

  this.width = workspace.width;
  this.height = workspace.height;
  this.canvas_cspace.width = workspace.width;
  this.canvas_cspace.height = workspace.height;
  this.canvas_qspace.width = workspace.width;
  this.canvas_qspace.height = workspace.height;
  this.valid = false;
}
//var addEvent = function(object, type, callback) {
DocumentState.prototype.addEvent = function(object, type, callback) {
  if (object == null || typeof(object) == 'undefined') return;
  if (object.addEventListener) {
      object.addEventListener(type, callback, false);
  } else if (object.attachEvent) {
      object.attachEvent("on" + type, callback);
  } else {
      object["on"+type] = callback;
  }
};


function init(){

  jointSize = 10;
  linkWidth = 10;
  fillColor = "#AAAAAA";

  cspace = document.getElementById("configuration-space");
  qspace = document.getElementById("quotient-space");
  workspace = document.getElementById("workspace");

  documentState = new DocumentState(workspace, cspace, qspace);
  outputD1 = document.getElementById("wSize");
  outputD2 = document.getElementById("hSize");
  outputD3 = document.getElementById("posCircleWorld");
  outputD4 = document.getElementById("posCircleCanvas");
  outputRobotPoseQ1 = document.getElementById("robot_q1");
  outputRobotPoseQ2 = document.getElementById("robot_q2");

  qL1 = CreateSlider("Joint1 Angle", -3.14, 3.14, 0.01, 0);
  qL2 = CreateSlider("Joint2 Angle", -3.14, 3.14, 0.01, 0);
  lengthL1 = CreateSlider("Link1 Length", 0.5, 1.5, 0.01, 1);
  lengthL2 = CreateSlider("Link2 Length", 0.5, 1.5, 0.01, 1);

  documentState.addObstacle(new Obstacle(300,200,50,50));
  documentState.robot.update(qL1.value, qL2.value);
  documentState.valid = false; 
  documentState.addEvent(window, "resize", documentState.windowResizeEvent);
  documentState.windowResizeEvent(); 
} 

