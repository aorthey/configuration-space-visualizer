function CanvasConfigurationSpace(canvas)
{
  this.canvas = canvas;
  this.width = canvas.width;
  this.height = canvas.height;
  this.ctx = canvas.getContext('2d');
  this.valid = false;

  canvas.addEventListener('mousedown', function(e) {
    var mouse = documentState.getMouse(e);
    var mx = mouse.x;
    var my = mouse.y;
    outputD3.innerHTML = mx;
    outputD4.innerHTML = my;
  }, true);
}

CanvasConfigurationSpace.prototype.update = function(w, h) {
  this.canvas.width = w;
  this.canvas.height = h;
  this.width = canvas.width;
  this.height = canvas.height;
  this.valid = false;
}

CanvasConfigurationSpace.prototype.clear = function() {
  this.ctx.clearRect(0, 0, this.width, this.height);
}
CanvasConfigurationSpace.prototype.CanvasCspaceToConfiguration = function(x,y){
  var s = ((x / this.width) * 2*Math.PI) - Math.PI;
  var e = ((y / this.height) * 2*Math.PI) - Math.PI;
  return{ 
    q1: s, 
    q2: e
  };
}
CanvasConfigurationSpace.prototype.ConfigurationToCanvasCspace = function(q1, q2){
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
CanvasConfigurationSpace.prototype.draw = function() {
  var step = 2;
  var q1_old = this.robot.q1;
  var q2_old = this.robot.q2;
  for (var x = 0; x < this.width; x+=step) {
    for (var y = 0; y < this.height; y+=step) {
      var cspaceCoords = this.CanvasCspaceToConfiguration(x,y);
      this.robot.update(cspaceCoords.q1, cspaceCoords.q2);

      var color = "white";

      var obstacle = documentState.obstacles[0];
      var block = { x1: obstacle.x, y1: obstacle.y, x2: obstacle.x+obstacle.w, y2: obstacle.y+obstacle.h };
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

      this.ctx.save();
      this.ctx.beginPath();
      this.ctx.fillStyle = color;
      this.ctx.fillRect(x, y, step, step);
      this.ctx.fill();
      this.ctx.restore();
    }
  }

  this.robot.update(q1_old, q2_old);

  var canvasCoords = this.ConfigurationToCanvasCspace(q1_old, q2_old);
  var x = canvasCoords.x;
  var y = canvasCoords.y;

  this.ctx.save();
  this.ctx.beginPath();
  this.ctx.fillStyle = "red";
  var lCross = 10;
  this.ctx.fillRect(x - lCross, y, 2*lCross, 1);
  this.ctx.fillRect(x, y - lCross, 1, 2*lCross);
  this.ctx.fillStyle = "black";
  this.ctx.fillRect(x, y, 2, 2);
  this.ctx.fill();
  this.ctx.restore();
}
