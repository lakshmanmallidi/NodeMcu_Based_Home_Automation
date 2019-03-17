var myRequest;
function initialize()
{
 sessionid=localStorage.getItem("myhome_sessionid");
 document.getElementById("myhomeid").href="myhome.html?sessionid="+sessionid;
 document.getElementById("livedataid").href="livedata.html?sessionid="+sessionid;
 document.getElementById("s2tid").href="voiceRecognition.html?sessionid="+sessionid;
 if (window.XMLHttpRequest)
 {
  myRequest = new XMLHttpRequest();
	}
 else
 {
  myRequest = new ActiveXObject("Microsoft.XMLHTTP");
	}
 myRequest.open("GET","?buttonstatus=true", true);
 myRequest.send(null);
 myRequest.onreadystatechange = getbuttonstate;		
}
			
function getbuttonstate()		
{
	
 if (myRequest.readyState ===4)		
 {
  if (myRequest.status === 200)
  {
	   var text = myRequest.responseText;
	   statusarray=text.split(" ");
	   for(var i=0;i<4;i++)
	   {
		   if(statusarray[i]=="True")
		   {
			   document.getElementById("switch"+(i+1).toString()).checked=true;
		   }
		   else
		   {
			   document.getElementById("switch"+(i+1).toString()).checked=false;
		   }
	   }
   }
  }
 }		

		