var jointSize = 10;
var linkWidth = 10;
var fillColor = "#AAAAAA";
var cspace = document.getElementById("configuration-space");
var workspace = document.getElementById("workspace");
var workspaceState = new WorkspaceState(workspace, cspace);
////DEBUG
var outputD1 = document.getElementById("wSize");
var outputD2 = document.getElementById("hSize");
var outputD3 = document.getElementById("posCircleWorld");
var outputD4 = document.getElementById("posCircleCanvas");


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
//workspaceState
//*****************************************************************************
function WorkspaceState(canvas, cspaceCanvas) {
  this.canvas = canvas;
  this.width = canvas.width;
  this.height = canvas.height;
  this.ctx = canvas.getContext('2d');
  this.cspaceCanvas = cspaceCanvas;
  this.ctxCspace = cspaceCanvas.getContext('2d');
  this.ctxCspace.imageSmoothingEnabled = true;
  this.ctx.imageSmoothingEnabled = true;
  this.ctxCspace.translate(0.5, 0.5)


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
  this.shapes = [];
  this.robot = new Robot();
  this.dragging = false; // Keep track of when we are dragging
  this.selection = null;
  this.dragoffx = 0; // See mousedown and mousemove events for explanation
  this.dragoffy = 0;
  var myState = this;
  
  canvas.addEventListener('selectstart', function(e) { e.preventDefault(); return false; }, false);
  canvas.addEventListener('mousedown', function(e) {
    var mouse = myState.getMouse(e);
    var mx = mouse.x;
    var my = mouse.y;
    var shapes = myState.shapes;
    var l = shapes.length;
    for (var i = l-1; i >= 0; i--) {
      if (shapes[i].contains(mx, my)) {
        var mySel = shapes[i];
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
      myState.valid = false; // Need to clear the old selection border
    }
  }, true);
  canvas.addEventListener('mousemove', function(e) {
    if (myState.dragging){
      var mouse = myState.getMouse(e);
      // We don't want to drag the object by its top-left corner, we want to drag it
      // from where we clicked. Thats why we saved the offset and use it here
      myState.selection.x = mouse.x - myState.dragoffx;
      myState.selection.y = mouse.y - myState.dragoffy;   
      myState.valid = false; // Something's dragging so we must redraw
    }
  }, true);
  canvas.addEventListener('mouseup', function(e) {
    myState.dragging = false;
  }, true);
  // double click for making new shapes
  canvas.addEventListener('dblclick', function(e) {
    var mouse = myState.getMouse(e);
    myState.addShape(new Shape(mouse.x - 10, mouse.y - 10, 20, 20, 'rgba(0,255,0,.6)'));
  }, true);

  this.selectionColor = '#CC0000';
  this.selectionWidth = 3;  
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

WorkspaceState.prototype.addShape = function(shape) {
  this.shapes.push(shape);
  this.valid = false;
}

WorkspaceState.prototype.clear = function() {
  this.ctx.clearRect(0, 0, this.width, this.height);
  this.ctxCspace.clearRect(0, 0, this.width, this.height);
}

WorkspaceState.prototype.draw = function() {
  // if our state is invalid, redraw and validate!
  if (!this.valid) {
    var ctx = this.ctx;
    var shapes = this.shapes;
    this.clear();
    
    // ** Add stuff you want drawn in the background all the time here **
    
    // draw all shapes
    var l = shapes.length;
    for (var i = 0; i < l; i++) {
      var shape = shapes[i];
      // We can skip the drawing of elements that have moved off the screen:
      if (shape.x > this.width || shape.y > this.height ||
          shape.x + shape.w < 0 || shape.y + shape.h < 0) continue;
      shapes[i].draw(ctx);
    }
    
    // draw selection
    // right now this is just a stroke along the edge of the selected Shape
    if (this.selection != null) {
      ctx.strokeStyle = this.selectionColor;
      ctx.lineWidth = this.selectionWidth;
      var mySel = this.selection;
      ctx.strokeRect(mySel.x,mySel.y,mySel.w,mySel.h);
    }
    
    this.robot.draw(ctx);
    this.drawConfigurationSpace();
    this.valid = true;
  }
}


WorkspaceState.prototype.CanvasCspaceToConfiguration = function(x,y){
  var s = ((x / this.width) * 2*Math.PI) - Math.PI;
  var e = ((y / this.height) * 2*Math.PI) - Math.PI;
  return{ 
    q1: s, 
    q2: e
  };
}
WorkspaceState.prototype.ConfigurationToCanvasCspace = function(q1, q2){
  var x = ((Number(q1) + Math.PI)/(2*Math.PI))*this.width;
  var y = ((Number(q2) + Math.PI)/(2*Math.PI))*this.height;
  return{ 
    x: x, 
    y: y
  };
}
WorkspaceState.prototype.drawConfigurationSpace = function() {
  var step = 2;
  var q1_old = this.robot.q1;
  var q2_old = this.robot.q2;
  for (var x = 0; x < this.width; x+=step) {
    for (var y = 0; y < this.height; y+=step) {
      var cspaceCoords = this.CanvasCspaceToConfiguration(x,y);
      this.robot.update(cspaceCoords.q1, cspaceCoords.q2);

      var color = "white";

      var shape = this.shapes[0];
      var block = { x1: shape.x, y1: shape.y, x2: shape.x+shape.w, y2: shape.y+shape.h };
      var cCoords = this.robot.CanvasToWorldCoordinates(block.x1, block.y1);
      block.x1 = cCoords.x;
      block.y1 = cCoords.y;
      cCoords = this.robot.CanvasToWorldCoordinates(block.x2, block.y2);
      block.x2 = cCoords.x;
      block.y2 = cCoords.y;

      var feasible = hitBlock(this.robot.L2, block) | hitBlock(this.robot.L1, block);
      if (feasible) {
        color = "lightgray";
      }

      this.ctxCspace.save();
      this.ctxCspace.beginPath();
      this.ctxCspace.fillStyle = color;
      this.ctxCspace.fillRect(x, y, step, step);
      this.ctxCspace.fill();
      this.ctxCspace.restore();
    }
  }

  this.robot.update(q1_old, q2_old);

  var canvasCoords = this.ConfigurationToCanvasCspace(q1_old, q2_old);
  var x = canvasCoords.x;
  var y = canvasCoords.y;

  this.ctxCspace.save();
  this.ctxCspace.beginPath();
  this.ctxCspace.fillStyle = "red";
  var lCross = 10;
  this.ctxCspace.fillRect(x - lCross, y, 2*lCross, 1);
  this.ctxCspace.fillRect(x, y - lCross, 1, 2*lCross);
  this.ctxCspace.fillStyle = "black";
  this.ctxCspace.fillRect(x, y, 2, 2);
  this.ctxCspace.fill();
  this.ctxCspace.restore();
}
function intersects(a, b, c, d, p, q, r, s) {
  var det, gamma, lambda;
  det = (c - a) * (s - q) - (r - p) * (d - b);
  if (det === 0) {
    return false;
  } else {
    lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det;
    gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det;
    return 0 < lambda && lambda < 1 && (0 < gamma && gamma < 1);
  }
}
function hitBlock(segment, block) {
  var bottom = intersects(
    segment.x1,
    segment.y1,
    segment.x2,
    segment.y2,
    block.x1,
    block.y1,
    block.x2,
    block.y1
  );
  var top = intersects(
    segment.x1,
    segment.y1,
    segment.x2,
    segment.y2,
    block.x1,
    block.y2,
    block.x2,
    block.y2
  );
  var left = intersects(
    segment.x1,
    segment.y1,
    segment.x2,
    segment.y2,
    block.x1,
    block.y1,
    block.x1,
    block.y2
  );
  var right = intersects(
    segment.x1,
    segment.y1,
    segment.x2,
    segment.y2,
    block.x2,
    block.y1,
    block.x2,
    block.y2
  );
  return bottom | top | left | right;
}





WorkspaceState.prototype.getMouse = function(e) {
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
  return {x: mx, y: my};
}

function userEventSlider(event) {
  workspaceState.robot.l1 = lengthL1.value;
  workspaceState.robot.l2 = lengthL2.value;
  workspaceState.robot.update(qL1.value, qL2.value);
  workspaceState.valid = false;
}

function init(){
  qL1 = CreateSlider("Joint1 Angle", -3.14, 3.14, 0.01, 0);
  qL2 = CreateSlider("Joint2 Angle", -3.14, 3.14, 0.01, 0);
  lengthL1 = CreateSlider("Link1 Length", 0.5, 1.5, 0.01, 1);
  lengthL2 = CreateSlider("Link2 Length", 0.5, 1.5, 0.01, 1);

  workspaceState.addShape(new Shape(300,200,50,50));
  workspaceState.robot.update(qL1.value, qL2.value);
  workspaceState.valid = false; windowResizeEvent(); } function windowResizeEvent(){
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
  workspaceState.width = workspace.width;
  workspaceState.height = workspace.height;
  workspaceState.valid = false;
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
addEvent(window, "resize", windowResizeEvent);


