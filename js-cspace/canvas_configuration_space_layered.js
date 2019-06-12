function CanvasConfigurationSpaceLayered(canvas1, canvas2)
{
  this.canvas = canvas2;
  this.background = canvas1;
  this.width = this.canvas.width;
  this.height = this.canvas.height;
  this.ctx = this.canvas.getContext('2d');
  this.ctx_background = this.background.getContext('2d');
  this.valid = false;
  this.qspace = false;
  this.resolution_step = 2; //higher => faster but coarser image

  // var stylePaddingLeft, stylePaddingTop, styleBorderLeft, styleBorderTop;
  if (document.defaultView && document.defaultView.getComputedStyle) {
    this.stylePaddingLeft = parseInt(document.defaultView.getComputedStyle(this.canvas, null)['paddingLeft'], 10)      || 0;
    this.stylePaddingTop  = parseInt(document.defaultView.getComputedStyle(this.canvas, null)['paddingTop'], 10)       || 0;
    this.styleBorderLeft  = parseInt(document.defaultView.getComputedStyle(this.canvas, null)['borderLeftWidth'], 10)  || 0;
    this.styleBorderTop   = parseInt(document.defaultView.getComputedStyle(this.canvas, null)['borderTopWidth'], 10)   || 0;
  }
  var html = document.body.parentNode;
  this.htmlTop = html.offsetTop;
  this.htmlLeft = html.offsetLeft;
  var myState = this;
  this.dragging = false;
  this.canvas.addEventListener('mousedown', function(e) {
    var mouse = myState.getMouse(e);
    var mx = mouse.x;
    var my = mouse.y;
    var cspaceCoords = myState.CanvasCspaceToConfiguration(mx, my);
    if(myState.qspace){
      myState.robot.update(cspaceCoords.q1, myState.robot.q2);
    }else{
      myState.robot.update(cspaceCoords.q1, cspaceCoords.q2);
    }
    documentState.valid = false;
    myState.dragging = true;
  }, true);

  this.canvas.addEventListener('mousemove', function(e) {
    if (myState.dragging){
      var mouse = myState.getMouse(e);
      var mx = mouse.x;
      var my = mouse.y;
      documentState.valid = false;
      var cspaceCoords = myState.CanvasCspaceToConfiguration(mx, my);
      if(myState.qspace){
        myState.robot.update(cspaceCoords.q1, myState.robot.q2);
      }else{
        myState.robot.update(cspaceCoords.q1, cspaceCoords.q2);
      }
    }
  }, true);
  this.canvas.addEventListener('mouseup', function(e) {
    myState.dragging = false;
  }, true);
}

CanvasConfigurationSpaceLayered.prototype.getMouse = function(e) {
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

CanvasConfigurationSpaceLayered.prototype.update = function(w, h) {
  this.canvas.width = w;
  this.canvas.height = h;
  this.width = this.canvas.width;
  this.height = this.canvas.height;
  this.valid = false;
}

CanvasConfigurationSpaceLayered.prototype.clear = function() {
  this.ctx.clearRect(0, 0, this.width, this.height);
  this.ctx_background.clearRect(0, 0, this.width, this.height);
  console.log("clear layered");

}
CanvasConfigurationSpaceLayered.prototype.CanvasCspaceToConfiguration = function(x,y){
  var q1 = ((x / this.width) * 2*Math.PI) - Math.PI;
  var q2 = (((y / this.height) * 2*Math.PI) - Math.PI);
  return{ 
    q1: q1, 
    q2: q2
  };
}
CanvasConfigurationSpaceLayered.prototype.ConfigurationToCanvasCspace = function(q1, q2){
  var x = ((Number(q1) + Math.PI)/(2*Math.PI))*this.width;
  var y = ((Number(q2) + Math.PI)/(2*Math.PI))*this.height;
  return{ 
    x: x, 
    y: y
  };
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

CanvasConfigurationSpaceLayered.prototype.drawLabels = function() {

}

CanvasConfigurationSpaceLayered.prototype.draw = function() {

  if(!this.valid){
    this.clear();
    console.log("redraw layered");
    var q1_old = this.robot.q1;
    var q2_old = this.robot.q2;
    for (var x = 0; x < this.width; x+=this.resolution_step) {
      for (var y = 0; y < this.height; y+=this.resolution_step) {
        var cspaceCoords = this.CanvasCspaceToConfiguration(x,y);
        this.robot.update(cspaceCoords.q1, cspaceCoords.q2);

        var color = "white";

        for (var i = 0; i < documentState.obstacles.length; i++)
        {
          var obstacle = documentState.obstacles[i];
          var block = { x1: obstacle.x, y1: obstacle.y, x2: obstacle.x+obstacle.w, y2: obstacle.y+obstacle.h };
          var cCoords = this.robot.CanvasToWorldCoordinates(block.x1, block.y1);
          block.x1 = cCoords.x;
          block.y1 = cCoords.y;
          cCoords = this.robot.CanvasToWorldCoordinates(block.x2, block.y2);
          block.x2 = cCoords.x;
          block.y2 = cCoords.y;

          var feasible = hitBlock(this.robot.L1, block);
          if (!this.qspace){
            feasible |= hitBlock(this.robot.L2, block);
          }
          if (feasible) {
            color = "lightgray";
          }

          this.ctx_background.save();
          this.ctx_background.beginPath();
          this.ctx_background.fillStyle = color;
          this.ctx_background.fillRect(x, y, this.resolution_step, this.resolution_step);
          this.ctx_background.fill();
          this.ctx_background.restore();
        }
      }
    }
    this.valid = true;
    this.robot.update(q1_old, q2_old);
  }

  console.log("redraw cross");
  var canvasCoords = this.ConfigurationToCanvasCspace(this.robot.q1, this.robot.q2);
  var x = canvasCoords.x;
  var y = canvasCoords.y;
  outputD3.innerHTML = x;
  outputD4.innerHTML = y;

  this.ctx.clearRect(0, 0, this.width, this.height);
  this.ctx.save();
  this.drawLabels();
  this.ctx.beginPath();
  this.ctx.fillStyle = "red";

  var lCross = 12;
  var wCross = 2;
  if(!this.qspace){
    this.ctx.fillRect(x - lCross, y - wCross, 2*lCross, 2*wCross);
    this.ctx.fillRect(x - wCross, y - lCross, 2*wCross, 2*lCross);
    this.ctx.fillStyle = "black";
    this.ctx.fillRect(x, y, 1, 1);
  }else{
    //horizontal
    this.ctx.fillRect(x - lCross, 0.5*this.height - wCross, 2*lCross, 2*wCross);
    //vertical
    this.ctx.fillRect(x - wCross, 0, 2*wCross, 2*Math.PI*this.height);
  }

  this.ctx.fill();
  this.ctx.restore();
}
