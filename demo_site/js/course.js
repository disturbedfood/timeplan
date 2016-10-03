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
var week = 0;

$(function() {
	var excluded = [];
	var subjects = [];
	var course;

	var requestUrl = "";

	if ($.QueryString.excluded != undefined) excluded = $.QueryString.excluded.split(",");
	if ($.QueryString.subjects != undefined) subjects = $.QueryString.subjects.split(",");
	if ($.QueryString.course != undefined) course = $.QueryString.course;

	if (course === undefined) {
		$("#timeplan").text("Invalid course.");
		return;
	} else {requestUrl = "https://crypticcraft.eu/timeplan/2.0/course/" + course + ""}


	if ($.QueryString.week != undefined) {
		week = parseInt($.QueryString.week);
	}

	subjects.push(course);
	getTimetableData(subjects, excluded, week);

	$("#nextweek").click(function () {
		window.location.href = buildUrl(course, subjects, excluded) + "&week=" + (week + 1);
	});
	$("#prevweek").click(function () {
		window.location.href = buildUrl(course, subjects, excluded) + "&week=" + (week - 1);
	});
	
});

function subjectToUrl(s, week) {
	var requestUrl = "https://crypticcraft.eu/timeplan/2.0/";

	if (s.length == 6) requestUrl += "subject/" + s;
	else { requestUrl += "course/" + s; }

	if (week != 0) requestUrl += week + "";
	return requestUrl;
}

function getTimetableData(subjects, excluded, week) {
	var tt = [];
	var actualTt = [];

	$.each(subjects, function(index, url) {
		tt.push(
			$.ajax({
				url: subjectToUrl(url, week),
				type: 'GET'
			})
		);
	});
	$.when.apply($, tt).done(function() {
		generateHtml(excluded, tt);
	})

}

function generateHtml(excluded, data) {
	// console.log(data[0].responseJSON.timeplan);
	actualData = [];

	for (d of data) {
		for (r of d.responseJSON.timeplan) {
			actualData.push(r);
		}
	}

	actualData.sort(function(r1, r2) {
		var reg = /(\d{4})-(\d{2})-(\d{2}) (\d{2}).(\d{2})/;
		var d1T = reg.exec(r1.date + " " + r1.start_time);
		var d2T = reg.exec(r2.date + " " + r2.start_time);
		var d1 = new Date(d1T[1], d1T[2]-1, d1T[3], d1T[4], d1T[5]);
		var d2 = new Date(d2T[1], d2T[2]-1, d2T[3], d2T[4], d2T[5]);
		return d1.getTime() - d2.getTime();
	});
	newHtml = "";
	lastDay = "";

	$("#getweek").val(data[0].responseJSON.meta.week);

	week = parseInt(data[0].responseJSON.meta.week);
	newHtml = "";

	for (r of actualData) {
		if (!containsExcluded(excluded, r.subject)) continue;
		if (lastDay != r.week_day) {
			newHtml = newHtml.length === 0 ? "" : newHtml + "</tbody></table>";
			newHtml += "<h4>" + r.week_day + "</h4>\n<table>" + tableHead + "\n<tbody>";
			lastDay = r.week_day
		}
		newHtml += buildDataRow(r);
		}
	
	$("#timeplan").html(newHtml);
}

function buildDataRow(r) {
	return "<tr><td>" +r.start_time + "-" + r.end_time + "</td><td>" 
			+ r.subject + "</td><td>" + r.type + "</td><td>" + r.rooms + "</td></tr>";
}



function timeCompare(start_time) {
	return parseInt(start_time.split(".").join([separator = ""]));
}

function buildUrl(course, subjects, excludedSubjects) {
	url = "course.html";
	if (course.length != 0) {
		url += "?course=" + course;
	}
	if (subjects.length > 0) {
		url += url.length > 11 ? "&subjects=" : "?subjects=";
		for (s of subjects) {
			if (s.length == 6) url += s + ",";
		}
		if (url.substr(url.length - 1 ) == ",") url = url.slice(0, -1);
	}
	if (excludedSubjects.length > 0) {
		url += url.length > 11 ? "&excluded=" : "?excluded=";
		for (s of excludedSubjects) {
			url += s + ",";
		}
		url = url.slice(0, -1);
	}

	return url;
}

function containsExcluded(excluded, subject) {
	subjects = subject.split("/");
	for (s of subjects) {
		if (excluded.indexOf(s) != -1) {
			return false;
		}
	}
	return true;
}