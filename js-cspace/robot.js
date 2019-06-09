function Robot()
{
  this.linkWidth = 10;
  this.jointSize = 10;
  this.q1 = 0;
  this.q2 = 0;
  this.l1 = 1;
  this.l2 = 1;
  this.color = "#000000"
  this.fillColor = "#DFDFDF"
}

Robot.prototype.update = function(q1, q2) {
  this.q1 = q1;
  this.q2 = q2;
  this.L1 = this.arm(0, 0, this.q1, this.l1);
  var q12 = Number(this.q2)+Number(this.q1);
  this.L2 = this.arm(this.L1.x2, this.L1.y2, q12, this.l2);
}

Robot.prototype.draw = function(context) {
  this.drawArmSegment(context, this.L2, "0x909090");
  this.drawArmSegment(context, this.L1, "0x909090");
};
Robot.prototype.drawArmSegment = function(ctx, a) {
  var canvasCoords = this.WorldToCanvasCoordinates(a.x1, a.y1);
  var cx1 = canvasCoords.x;
  var cy1 = canvasCoords.y;
  var canvasCoords = this.WorldToCanvasCoordinates(a.x2, a.y2);
  var cx2 = canvasCoords.x;
  var cy2 = canvasCoords.y;

  ctx.lineWidth = 1.5*this.linkWidth;
  ctx.save();
  ctx.strokeStyle = this.color;
  ctx.beginPath();
  ctx.moveTo(cx1, cy1);
  ctx.lineTo(cx2, cy2);
  ctx.stroke();
  ctx.restore();

  ctx.lineWidth = this.linkWidth;
  ctx.save();
  ctx.strokeStyle = this.fillColor;
  ctx.beginPath();
  ctx.moveTo(cx1, cy1);
  ctx.lineTo(cx2, cy2);
  ctx.stroke();
  ctx.restore();

  ctx.beginPath();
  ctx.lineWidth = 0.3*this.jointSize;
  ctx.strokeStyle = this.color;
  ctx.fillStyle = this.fillColor;
  ctx.arc(cx2, cy2, this.jointSize, 0, 2 * Math.PI, false);
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = 0.3*this.jointSize;
  ctx.strokeStyle = this.color;
  ctx.fillStyle = this.fillColor;
  ctx.arc(cx1, cy1, this.jointSize, 0, 2 * Math.PI, false);
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.strokeStyle = this.color;
  ctx.fillStyle = this.color;
  ctx.arc(cx2, cy2, 0.2*this.jointSize, 0, 2 * Math.PI, false);
  ctx.fill();
  ctx.stroke();
  ctx.beginPath();
  ctx.strokeStyle = this.color;
  ctx.fillStyle = this.color;
  ctx.arc(cx1, cy1, 0.2*this.jointSize, 0, 2 * Math.PI, false);
  ctx.fill();
  ctx.stroke();
}
Robot.prototype.arm = function (x1, y1, theta, len) {
  var dx = Math.cos(theta) * len;
  var dy = Math.sin(theta) * len;
  var x2 = x1 + dx;
  var y2 = y1 + dy;
  return { x1: x1, y1: y1, x2: x1 + dx, y2: y1 + dy };
}
Robot.prototype.WorldToCanvasCoordinates = function (x, y){
  var x_min = -3.14;
  var x_max = 3.14;
  var y_min = -3.14;
  var y_max = 3.14;

  var sx = x;
  var sy = y;

  if(sx < x_min){ 
    sx = x_min;
  }
  if(sx > x_max){ 
    sx = x_max;
  }

  if(sy < y_min){ 
    sy = y_min;
  }
  if(sy > y_max){ 
    sy = y_max;
  }
  sx = sx - x_min;
  sy = sy - y_min;
  if(sx>0) sx = sx / Math.abs(x_max - x_min);
  if(sy>0) sy = sy / Math.abs(y_max - y_min);

  //[0,1] to [0, workspace.width]
  return {
    x: sx*workspace.width, 
    y: workspace.height - sy*workspace.height
  };
}

Robot.prototype.CanvasToWorldCoordinates = function (x, y){
  var sx = ((x / workspace.width)*(2*Math.PI)) - Math.PI;
  var sy = ((y / workspace.height)*(2*Math.PI)) - Math.PI;

  return {
    x: sx,
    y: sy
  };
}
