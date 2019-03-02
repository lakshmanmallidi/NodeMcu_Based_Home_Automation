//Prepare the global variable for the request
var myRequest;
//Write the getText(url) function
function sendcredits(url)
{
 //check support for the XMLHttpRequest object
 if (window.XMLHttpRequest)
 {
  myRequest = new XMLHttpRequest();
	}
 //else, create an ActiveXObject for IE6
 else
 {
  myRequest = new ActiveXObject("Microsoft.XMLHTTP");
	}
  if(localStorage.getItem("myhome_sessionid")!=null)
  {
	  url=url+"&"+"sessionid="+localStorage.getItem("myhome_sessionid");
	}
 //Call the open() method to make the request
 myRequest.open("GET", url, true);
 //Send the request
 myRequest.send(null);
 myRequest.onreadystatechange = gethomepage;		
}
		
		/**********************************************/
		
		//This function handles the server response
		
function gethomepage()		
{
 //Get a reference to the header element where
 //the returned result will be displayed
 //var myHeader = document.getElementById("myHeader");
 //Check the response is complete	
 if (myRequest.readyState ===4)		
 {
 //Check the status code of the response is successful
  if (myRequest.status === 200)
  {
   //Store the response
	   var text = myRequest.responseText;
	   if(text!="loginerror")
	   {
	   document.location.href = text.split(" ")[0]+"?"+"sessionid="+text.split(" ")[1];
	   localStorage.setItem("myhome_sessionid",text.split(" ")[1]);
	   }
	   else
	   {
		document.getElementById("signin-error").innerHTML="<h5>INVALID USERNAME OR PASSWORD</h5>"
	   }
   }
  }
 }		

		