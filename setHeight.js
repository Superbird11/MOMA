function setGoodHeight (element) {
	if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
		var w = element.width;
		var h = element.height;
		element.setAttribute("style","width:88vw");
		var wn = element.width;
		var hn = h * wn / w;
		element.setAttribute("style","height:"+hn+"px");
	}
	else {		
		if(window.innerHeight-50 < element.height) {
			var h = element.height;
			var w = element.width;
			element.height = window.innerHeight - 50;
			element.width = w * element.height / h;
		}
		if (window.innerWidth-100 < element.width) {
			var h = element.height;
			var w = element.width;
			element.width = window.innerWidth - 100;
			element.height = h * element.width / w;
		}
		if(element.width < 540) {
			element.parentNode.setAttribute("style","width:" + 540 + "px");
		}
		else { 
			element.parentNode.setAttribute("style","width:" + (element.width + 40) + "px");
		}
	}
}

function newNoteHeight (element) {
	var h = element.height;
	element.parentNode.setAttribute("style","width:" + (h+40) + "px");
}

function setSmallHeight (element) {
	/*if(element.height > element.width) {
		var h = element.height;
		var w = element.width;
		element.height = 230;
		element.width = w * element.height/h;
	}
	else if(element.width > element.height) {
		var h = element.height;
		var w = element.width;
		element.width = 230;
		element.height = h * element.weight/w;
	}*/
	element.width = 230;
	element.height = 230;
}

/*
function eclipseScreen (element) {
	var h = element.height;
	var w = element.width;
	if(document.getElementByID("container").style.visibility == "hidden") {
		document.getElementByID("header").style.visibility = "visible";
		document.getElementByID("container").style.visibility = "visible";
		document.getElementByID("bigImage").z-index = 1
		document.getElementByID("bigImage").style.visibility = "hidden"
	}
	else{
		//then adjust height
		document.getElementByID("header").style.visibility = "hidden";
		document.getElementByID("container").style.visibility = "hidden";
		var bi = document.getElementByID("bigImage");
		bi.z-index = 6;
		bi.style.visibility = "visible";
		
		var childImage = bi.getElementsByTagName("img")[0];
		if(h * (window.innerWidth / w) > window.innerHeight) {
			bi.width = childImage.width * (window.innerHeight / childImage.height);
			bi.height = window.innerHeight;
			var horizBlankSpace = window.innerWidth - bi.width;
			bi.left = horizBlankSpace / 2;
		} else {
			bi.height = childImage.height * (window.innerWidth / childImage.width);
			bi.width = window.innerWidth;
			var vertBlankSpace = window.innerWidth - bi.width;
			bi.top = vertBlankSpace / 2;
		}
	}
}*/