// var baseUrl = "https://crypticcraft.eu/timeplan/2.0/"
var baseUrl = "http://localhost:5000/timeplan/2.0/"

$(function(){
	var courses = [];
	var subjects = [];

	var selectedCourse = "";
	var selectedSubject = "";


  	$.getJSON(baseUrl + "courses", function (data) {
		for (c of data['courses']) {
		courses.push({value: c['name'], data: c['code']});
	  	}
  	});

  	$.getJSON(baseUrl + "subjects", function (data) {
		for (c of data['subjects']) {
		subjects.push({value: c['subject_code'], data: c['code']});
	  	}
  	});
  
   	$('#course-selection').autocomplete({
	    lookup: courses,
	    onSelect: function (suggestion) {
			selectedCourse = suggestion;
    	}
  	});

   $('#subject-selection').autocomplete({
	    lookup: subjects,
	    onSelect: function (suggestion) {
			selectedSubject = suggestion.value;
    	}
 	});

  	$('#course-selection').keypress(function(event) {
	  	selectCourse(event, selectedCourse);
 	});

   $('#subject-selection').keypress(function(event) {
	  	selectSubject(event, selectedSubject);
  	});

   $("#subjects-from-course").on('click', 'li', function() {
   		$(this).toggleClass("excluded");
   });

   $("#subjects-additional").on('click', 'li', function() {
   		$(this).remove();
   });
  

  	$('#getcourse').click(function () {
		selectCourse({which: 13}, selectedCourse); 
  	});

  	$('#getsubject').click(function () {
		selectSubject({which: 13}, selectedSubject); 
  	});

	$('#go').click(function () {
		window.location.href = buildUrl(selectedCourse.data, getAdditional(), getExcluded());
	});
});


function selectCourse(event, selectedCourse) {
	if (event.which == 13 && selectedCourse.length == undefined) {
		$("#selected-course").text("Selected course: " + selectedCourse.value);
		$('#course-selection').val('');

		$.getJSON(baseUrl + "course/" + selectedCourse.data, function (data) {
	  		subjectList = data['meta']['subjects'];
			subs = "";
			subsSorted = subjectList.sort();
			for (s of subsSorted) {
				subs += "<li>" + s + "</li>";
			}
			$('#subjects-from-course').html(subs);
  		});
  	}
}

function selectSubject(event, selectedSubject) {
	if (event.which == 13 && selectedSubject.length > 0) {
  		if (getAdditional().indexOf(selectedSubject) == -1) {
  			$('#subject-selection').val('');
  			var oldHtml = $("#subjects-additional").html();
  			$("#subjects-additional").html(oldHtml + "<li>" + selectedSubject + "</li>");
  		}
  	}
}

function noCode() {
	$('#out').text("No code selected!");
}

function getAdditional() {
	var additional = [];
	$("#subjects-additional li").each(function() {
		additional.push($(this).text());
	});
	return additional;
}

function getExcluded() {
	var excluded = [];
	$("#subjects-from-course li").each(function() {
		if ($(this).hasClass("excluded")) {
			excluded.push($(this).text());
		}
	});
	return excluded;
}

function buildUrl(course, subjects, excludedSubjects) {
	url = "course.html";
	if (course.length != 0) {
		url += "?course=" + course;
	}
	if (subjects.length > 0) {
		url += url.length > 11 ? "&subjects=" : "?subjects=";
		for (s of subjects) {
			url += s + ",";
		}
		url = url.slice(0, -1);
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