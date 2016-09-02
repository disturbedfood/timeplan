$(function(){
  var currencies = [];
  var selectedCode = "";
  $.getJSON("https://crypticcraft.eu/timeplan/2.0/courses/", function (data) {
	  for (c of data['courses']) {
		  currencies.push({value: c['name'], data: c['code']});
	  }
  });
  
   $('#autocomplete').autocomplete({
    lookup: currencies,
    onSelect: function (suggestion) {
		selectedCode = suggestion.data;
    }
  });
  
  $('#autocomplete').keypress(function(event) {
	  
	  if (event.which == 13 && selectedCode.length > 0) {
		window.location.href = "course.html?course=" + selectedCode;  
	  }
  });
  
  $('#getcourse').click(function () {
	  if (selectedCode.length == 0) {
		  noCode();
		  return;
	  }
	  window.location.href = "course.html?course=" + selectedCode;  
  });
  
  
  
});

function noCode() {
	$('#out').text("No code selected!");
}