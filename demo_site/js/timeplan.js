$(function(){
  var courses = [];
  var subjects = [];
  var selectedSubjects = [];
  var excludedSubjects = [];

  var selectedCourse = "";
  var selectedSubject = "";
  var excludedSubject = "";

  $.getJSON("https://crypticcraft.eu/timeplan/2.0/courses/", function (data) {
	  for (c of data['courses']) {
		  courses.push({value: c['name'], data: c['code']});
	  }
  });

  $.getJSON("https://crypticcraft.eu/timeplan/2.0/subjects/", function (data) {
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

  $('#course-selection').keypress(function(event) {
	  if (event.which == 13 && selectedCourse.length == undefined) {
		$("#selected-course").text("Selected course: " + selectedCourse.value);
		$('#course-selection').val('');
	  }
  });


   $('#subject-selection').autocomplete({
	    lookup: subjects,
	    onSelect: function (suggestion) {
			selectedSubject = suggestion.value;
    }
 	});

   $('#subject-selection').keypress(function(event) {
	  if (event.which == 13 && selectedSubject.length > 0) {
	  	if (selectedSubjects.indexOf(selectedSubject) == -1 && selectedSubjects.length < 5) {
	  		selectedSubjects.push(selectedSubject);
	  		updateSubjects(selectedSubjects);
	  		$('#subject-selection').val('');
	  	}
	  }
  	});

   $('#excluded-subject-selection').autocomplete({
	    lookup: subjects,
	    onSelect: function (suggestion) {
			excludedSubject = suggestion.value;
    }
 	});

   $('#excluded-subject-selection').keypress(function(event) {   
	  if (event.which == 13 && excludedSubject.length > 0) {
	  	if (excludedSubjects.indexOf(excludedSubject) == -1) {
	  		excludedSubjects.push(excludedSubject);
	  		updateExcludedSubjects(excludedSubjects);
	  		$('#excluded-subject-selection').val('');
	  	}
	  }
  	});
  

  $('#getcourse').click(function () {
	  if (selectedCode.length == 0) {
		  noCode();
		  return;
	  }
	  window.location.href = "course.html?course=" + selectedCode;  
  });

  $('#go').click(function () {
	  window.location.href = buildUrl(selectedCourse.data, selectedSubjects, excludedSubjects);
  });
});

function noCode() {
	$('#out').text("No code selected!");
}

function updateSubjects(subjects) {
	$("#selected-subjects").html();
	newHtml = "";
	for (s of subjects) {
		newHtml += "<li>" + s + "</li>\n";
	}
	$("#selected-subjects").html(newHtml);
}

function updateExcludedSubjects(subjects) {
	$("#excluded-subjects").html();
	newHtml = "";
	for (s of subjects) {
		newHtml += "<li>" + s + "</li>\n";
	}
	$("#excluded-subjects").html(newHtml);
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