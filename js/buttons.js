
var myRequest;
function sendButton(url)
{
 if (window.XMLHttpRequest)
 {
  myRequest = new XMLHttpRequest();
	}
 else
 {
  myRequest = new ActiveXObject("Microsoft.XMLHTTP");
	}
 myRequest.open("GET", url, true);
 myRequest.send(null);
 myRequest.onreadystatechange = getstatus;		
}
		
function getstatus()		
{	
 if (myRequest.readyState ===4)		
 {
  if (myRequest.status === 200)
  {
   var text = myRequest.responseText;
   idname=text.split(" ")[0];
   var value;
   if(text.split(" ")[1]=="True")
	   value=true;
   else 
	   value=false;
   document.getElementById(idname).checked=value;
   }
  }
 }		
		
		
