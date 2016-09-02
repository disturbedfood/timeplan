// http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/3855394#3855394 (jQuery plugin method)

(function($) {
    $.QueryString = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=', 2);
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'))
})(jQuery);

var tableHead = "<thead\
					<tr>\
					  <th>Time</th>\
					  <th>Subject</th>\
					  <th>Type</th>\
					  <th>Rooms</th>\
					</tr>\
				 </thead>";

$(function() {
	var course = $.QueryString.course;
	if (course === undefined) {
		$("#timeplan").text("Invalid course.");
	}
	$.getJSON("https://crypticcraft.eu/timeplan/2.0/course/" + course + "/", function (data) {
		newHtml = "";
		lastDay = "";
		for (r of data.timeplan) {
			if (lastDay != r.week_day) {
				newHtml = newHtml.length === 0 ? "" : newHtml + "</tbody></table>";
				newHtml += "<h4>" + r.week_day + "</h4>\n<table>" + tableHead + "\n<tbody>";
				lastDay = r.week_day
			}
			newHtml += "<tr><td>" +r.start_time + "-" + r.end_time + "</td><td>" 
			+ r.subject + "</td><td>" + r.type + "</td><td>" + r.rooms + "</td></tr>";
		}
		$("#timeplan").html(newHtml);
  });
  
  

	
});