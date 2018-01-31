var val = [];
var postdata = {};
var senddata = {};
var testdata = {};
y= "discipline:SOCIAL SCIENCE";
testdata[y] = 1;
var senddata =  JSON.stringify(testdata);

d3.json(topicsurl, function(cdata) {
    var tophtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    topichtml = '<br><p>Discipline</p><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    for (k in cdata['order']) {
	tophtml + '<p><input type="checkbox" value="topic:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p>';
	for (x in cdata['topics'][k]) {
            tabnum = tabnum + 1;
            var k_data = cdata['topics'][k][x];
            tophtml = tophtml + '<p><input type="checkbox" value="topic:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k_data + '</p>';
        }
	}

    tophtml = tophtml + '</ul>';
})
.header("Content-Type","application/json")
.send("POST",senddata);

d3.json(principlesurl, function(pdata) {
    console.log(pdata['principles']);
  var polhtml = "<table>";
  for (k in pdata['principles']) {
	stringhtml = '<tr valign=top>';
	for (item in pdata['principles'][k]) {
	   stringhtml = stringhtml + '<td>' + pdata['principles'][k][item] + "</td><td width=5></td>\n"; 
	}
	polhtml = polhtml + stringhtml + "</tr>\n";
  }
  polhtml = polhtml + "</table>";
  $("#principles").empty();
  $("#principles").html("<h4><b>All Parthenos High-Level Principles</b></h4>");
  $(polhtml).appendTo('#principles');
})

function result (cdata, flag) {
var postdata = {};
var xcdata = ["community:RESEARCH COMMUNITY", "discipline:SOCIAL SCIENCE", "topic:LEGAL FRAMEWORK", "topic:PRIVACY AND SENSITIVE DATA"];
for (name in cdata) {
	postdata[cdata[name]] = 1;	
};

apiurl = "/webfilter";
var senddata = JSON.stringify(postdata);

d3.json(bestpracticesurl, function(bdata) {
    console.log(bdata['bestpractice']);
  var polhtml = "<table>";
  for (k in bdata['bestpractice']) {
        stringhtml = '<tr valign=top><td width=10></td>';
        stringhtml = stringhtml + '<td><li>' + bdata['bestpractice'][k] + "</td><td width=5></td>\n";
        polhtml = polhtml + stringhtml + "</tr>\n";
  }
  polhtml = polhtml + "</table>";
  console.log(polhtml);
  $("#bestpractice").empty();
  $("#bestpractice").html("<h4><b>Best Practices</b></h4>");
  $(polhtml).appendTo('#bestpractice');
})
.header("Content-Type","application/json")
.send("POST",senddata);

if (flag == 1) {
	d3.json(topicsurl, function(cdata) {
    	var tophtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    	topichtml = '<br><p>Discipline</p><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    	var tabnum = 0;
	var topics= {};
	var topicid = 0;
	for (showtopic in cdata['topics'])
	{
	   topics[showtopic] = topicid;
	   topicid = topicid + 1;
	}
    	for (k in cdata['order']) {
		showtopic = cdata['order'][k];
		tophtml = tophtml + '<p><b><font color=#3077e8>' + showtopic + '</font></b></p>';
		topicid = topics[showtopic];
		for (x in cdata['topics'][showtopic])
		{
        	tabnum = tabnum + 1;
        	var k_data = cdata['topics'][showtopic][x];
        	tophtml = tophtml + '<p><input type="checkbox" value="topic:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k_data + '</p>';
		}
        }

    	tophtml = tophtml + '</ul>';
    	$('#topicsdata').empty();
    	$(tophtml).appendTo('#topics');
	})
	.header("Content-Type","application/json")
	.send("POST",senddata);
};

d3.json(apiurl, function(data) {
    console.log(data);
    var polhtml = '';
    var firstvalue = '';
    for (thistopic in data['result']) {
	var found = 0;
        var topicdata = data['result'][thistopic];
	var firstvalue = 1;
	if (topicdata['status'] == 'ok') 
	{
	    polhtml = polhtml + '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
	    polhtml = polhtml + "<h4><font color=#3077e8>" + thistopic + "</font></h4>";
            console.log('Data:');
	    console.log(topicdata);

	    k_data = topicdata[thistopic];
            for (d in k_data) {
                var value = k_data[d];
                if (!value) {
                        value = '';
                }
		polurl = "#";
		found = 1;
		if (k_data[d]['POLICY LINK'])
		{
		   polurl = k_data[d]['POLICY LINK'];
		}

		if (k_data[d]['POLICY'])
		{
                    name = "<a href='" + polurl + "' target=_blank>" + k_data[d]['POLICY']  + "</a>";
                    polhtml = polhtml + '<li>' + k_data[d]['ORGANISATION'] + ' ' + name + '</li>';
		}
        	};
 	     polhtml = polhtml + "</ul>";
	}

	if (!found)
	{
            polhtml = polhtml + '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
            polhtml = polhtml + "<h4><font color=#3077e8>" + thistopic + "</font></h4>";

	    for (thistopic in data['other']) 
	    {
	        polhtml = polhtml + "<p>No results for this topic. Here you can find some suggestions from other disciplines:</p>";
	        for (thisdisc in data['other'][thistopic]) 
		{
		    polhtml = polhtml + "<h5>" + thisdisc + "</h5>";
	 	    var polvalue = data['other'][thistopic][thisdisc];
	            for (d in polvalue)
		    {
			k_data = data['other'][thistopic][thisdisc];
                	polurl = "#";
                	found = 1;
                	if (k_data[d]['POLICY LINK'])
                	{  
                   	    polurl = k_data[d]['POLICY LINK'];
                	}
	        	name = "<a href='" + polurl + "' target=_blank>" + k_data[d]['POLICY']  + "</a>";
                	polhtml = polhtml + '<li> ' + k_data[d]['ORGANISATION'] + ' ' + name + '</li>';
	            }
	        };
	    };
	    polhtml = polhtml + "</ul>";
	}
    };
  $("#policies").empty();
  $("#policies").html("<h4><b>Policies that match your selection</b></h4>");
  $(polhtml).appendTo('#policies');
})
.header("Content-Type","application/json")
.send("POST",senddata);
};

d3.json(contentsurl, function(cdata) {
    var conthtml = '<h4><b>Select your Community</b><div class="tab-pane active" id="godiscipline" style="float:right"><a class="btn btn-primary btnNext">Next</a></div></h4>';
    var conthtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';

    topichtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    var known = new Object();
    for (k in cdata['contents']) {
        tabnum = tabnum + 1;
        var k_data = cdata['contents'][k];
        if (!k_data) {
	    conthtml = conthtml + '<p><input name="comm" type="checkbox" value="community:' + k + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p>';
        }
        else
        {
	    var thisval = known[k_data];
	    if (!thisval) {
		conthtml = conthtml + '<p><input name="comm" type="checkbox" value="community:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k_data + '</p>';
	    };
            topichtml = topichtml + '<p><input name="disc" type="checkbox" value="discipline:' + k + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p>';
	    known[k_data] = k;
        }
    }
    conthtml = conthtml + "</ul>";
    topichtml = topichtml + '</ul>';
    $('#community').append(conthtml);

    $(topichtml).appendTo('#discipline');
});

$(function() {
$(document).on("click", '#community input:checkbox', function() {
    var group = ":checkbox[name='comm']";
    if($(this).is(':checked')){
       $(group).not($(this)).attr("checked",false);
    }
});
  });

$(function() {
$(document).on("click", '#discipline input:checkbox', function() {
    var group = ":checkbox[name='disc']";
    if($(this).is(':checked')){
       $(group).not($(this)).attr("checked",false);
    }
});
  });
