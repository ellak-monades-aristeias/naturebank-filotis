var DDSPEED = 5;
var DDTIMER = 20;

// main function to handle the mouse events //
function ddMenu(id,d){
  var h = document.getElementById(id + '-ddheader');
  var c = document.getElementById(id + '-ddcontent');
  clearInterval(c.timer);
  if(d == 1){
    c.IsCollapsed=false;
    clearTimeout(h.timer);
    if(c.maxh && c.maxh <= c.offsetHeight){return}
    else if(!c.maxh){
      c.style.display = 'block';
      c.style.height = 'auto';
      c.maxh = c.offsetHeight;
      c.style.height = '0px';
    }
    c.timer = setInterval(function(){ddSlide(c,1)},DDTIMER);
  }else{
    h.timer = setTimeout(function(){ddCollapse(c)},125);
  }
}

// collapse the menu //
function ddCollapse(c){
  c.timer = setInterval(function(){ddSlide(c,-1)},DDTIMER);
}

// cancel the collapse if a user rolls over the dropdown //
function cancelHide(id){
  var h = document.getElementById(id + '-ddheader');
  var c = document.getElementById(id + '-ddcontent');
  clearTimeout(h.timer);
  clearInterval(c.timer);
  if("IsCollapsed" in c)
    if(c.IsCollapsed)
        return;
  if(c.offsetHeight < c.maxh){
    c.timer = setInterval(function(){ddSlide(c,1)},DDTIMER);
  }
}

// incrementally expand/contract the dropdown and change the opacity //
function ddSlide(c,d){
  var currh = c.offsetHeight;
  var dist;
  if(d == 1){
    dist = (Math.round((c.maxh - currh) / DDSPEED));
  }else{
    dist = (Math.round(2*currh / DDSPEED));
  }
  if(dist <= 1 && d == 1){
    dist = 1;
  }
  c.style.height = currh + (dist * d) + 'px';
  c.style.opacity = 0.90*currh / c.maxh;
  c.style.filter = 'alpha(opacity=' + (currh * 90 / c.maxh) + ')';
  if((currh/c.maxh<0.1 && d != 1) || (currh > (c.maxh - 2) && d == 1)){
    if(d!=1)c.IsCollapsed=true;
    clearInterval(c.timer);
  }
}
