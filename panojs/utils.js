// <![CDATA[

// Create a method callback on a javascript objects.
// Used for event handlers binding an object instance
// to a method invocation.  
// Usage:
//  on_event =  callback (m, 'some_method' [, arg1, ... ])
// When the event fires the callback will be called with 
// both the static arguments and the dynamic arguments provided
// by the event 
// Example:
//   m.some_method([arg1, arg,..., evt_arg1, evt_arg2, ...])
//

function callback (obj, method) {
    var thisobj = obj;
    var thismeth = (typeof method == "string")?thisobj[method]:method;
    var thisextra = Array.prototype.slice.call(arguments,2);
    
    return function () {
        var args = Array.prototype.slice.call(arguments);
        return thismeth.apply (thisobj, thisextra.concat(args));
    };
}

function isClientPhone () {
    // Apple
    if (navigator.userAgent.indexOf("iPhone")>=0) return true;
    if (navigator.userAgent.indexOf("iPod")>=0) return true;    

    // Google
    if (navigator.userAgent.toLowerCase().indexOf("android")>=0) return true;      
    
    // Nokia
    if (navigator.userAgent.toLowerCase().indexOf("series60")>=0 &&
        navigator.userAgent.toLowerCase().indexOf("webkit")>=0) return true;   
    if (navigator.userAgent.toLowerCase().indexOf("symbian")>=0 &&
        navigator.userAgent.toLowerCase().indexOf("webkit")>=0) return true; 
    
    // RIM
    if (navigator.userAgent.toLowerCase().indexOf("blackberry")>=0) return true;      
    
    // Palm/HP
    if (navigator.userAgent.toLowerCase().indexOf("palm")>=0) return true;      
    if (navigator.userAgent.toLowerCase().indexOf("webos")>=0) return true;      

    // Mcrosoft
    if (navigator.userAgent.indexOf("Windows Phone OS")>=0) return true;  
    if (navigator.userAgent.indexOf("IEMobile")>=0) return true;      
    
    return false;
}

function isClientTouch () {
    // Apple
    if (navigator.userAgent.indexOf("iPad")>=0) return true;
    if (navigator.userAgent.indexOf("iPhone")>=0) return true;
    if (navigator.userAgent.indexOf("iPod")>=0) return true;   
    
    // Google
    if (navigator.userAgent.toLowerCase().indexOf("android")>=0) return true;    

    // Nokia
    if (navigator.userAgent.toLowerCase().indexOf("series60")>=0 &&
        navigator.userAgent.toLowerCase().indexOf("webkit")>=0) return true;   
    if (navigator.userAgent.toLowerCase().indexOf("symbian")>=0 &&
        navigator.userAgent.toLowerCase().indexOf("webkit")>=0) return true; 
    
    // RIM
    if (navigator.userAgent.toLowerCase().indexOf("blackberry")>=0 &&
        navigator.userAgent.toLowerCase().indexOf("webkit")>=0) return true;   
    if (navigator.userAgent.toLowerCase().indexOf("playbook")>=0 &&
        navigator.userAgent.toLowerCase().indexOf("webkit")>=0) return true;   
        
    // Palm/HP    
    if (navigator.userAgent.toLowerCase().indexOf("webos")>=0) return true;      
    
    // Mcrosoft
    if (navigator.userAgent.indexOf("Windows Phone OS")>=0) return true;         
    
    return false;
}

function isIE () {
    if (navigator.appName == 'Microsoft Internet Explorer') return true;  
    return false;
}

function isAndroid () {
	if (navigator.userAgent.toLowerCase().indexOf("android")>=0) return true;
	return false;
}

function isMobileSafari () {
  if (navigator.userAgent.toLowerCase().indexOf("mobile")>=0 &&
      navigator.userAgent.toLowerCase().indexOf("safari")>=0
      ) return true; 
}

function positionAbsolute(x, y) {
    this.style.left = x + 'px';
    this.style.top = y + 'px';
}

function positionWebKitTranslate(x, y) {
    this.style.webkitTransform = 'translate(' + x + 'px, ' + y + 'px) translateZ(0)';
}

if ('webkitTransform' in document.documentElement.style)
    Element.prototype.positionAbsolutely = positionWebKitTranslate;
else
    Element.prototype.positionAbsolutely = positionAbsolute;

// ]]>
