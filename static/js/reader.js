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
  $("#principles").html("<h4><b>All PARTHENOS Guidelines</b></h4><div style='width:100%;float:center;'><a href='/'>Findable</a>&nbsp;<a href='/'>Accessable</a>&nbsp;<a href='/'>Interoperable</a>&nbsp;<a href='/'>Reusable</a>&nbsp;</div>");
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

flag = 1;
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
  $("#policies").empty();
  $("#policies").html("<img src='/static/loading.gif'>");
  $(polhtml).appendTo('#policies');
    var polhtml = '';
    var firstvalue = '';
    for (thistopic in data['topics']) {
	var found = 0;
	if (thistopic)
	{
            polhtml = polhtml + '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
            polhtml = polhtml + "<h2><font color=#3077e8>" + thistopic + "</font></h2>";
            console.log('Data:');
            console.log(topicdata);
	}

	var subtopics = data['topics'][thistopic];
	var firstvalue = 1;

	for (topid in subtopics)
        {
	    var subtopic = subtopics[topid];
	    var found = 0;
	    polhtml = polhtml + "<h4><font color=#3077e8>" + subtopic + "</font></h4>";
	    var topicdata = data['result'][subtopic];
	    if (topicdata) {
	       for (kindex in topicdata) 
	        {
	        keytopic = topicdata[kindex];
	        k_data = topicdata[kindex];
		if (k_data)
		{
                	var value = k_data;
                	if (!value) {
                            value = '';
                	}
			polurl = "#";
			if (k_data['policy link'])
			{
		   	    polurl = k_data['policy link'];
			    found = 1;
			}

			if (k_data['policy'])
			{
                    	    name = "<a href='" + polurl + "' target=_blank>" + k_data['policy']  + "</a>";
                    	    polhtml = polhtml + '<li>' + k_data['organisation'] + ' ' + name + '</li>';
			}
        	};
	     }
	   };

	   if (!found)
	   {
		    var keytopic = subtopic;
            	    polhtml = polhtml + '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';

		    if (data['other'])
	    	    {
	        	polhtml = polhtml + "No results for this topic.";
	        	for (thisdisc in data['other'][keytopic]) 
			{
			    polhtml = polhtml + " Here you can find some suggestions from other disciplines:";
		    	    polhtml = polhtml + "<h5>" + thisdisc + "</h5>";
	 	    	    var polvalue = data['other'][keytopic][thisdisc];
	             	    for (d in polvalue)
		    	    {
				k_data = polvalue[d];
                		polurl = "#";
                		if (k_data['policy link'])
                		{  
                   	    	    polurl = k_data['policy link'];
                		}
	        		name = "<a href='" + polurl + "' target=_blank>" + k_data['policy']  + "</a>";
                		polhtml = polhtml + '<li> ' + k_data['organisation'] + ' ' + name + '</li>';
	            	     }
	        	};
	    	    };

		polhtml = polhtml + "</ul>";
	     };
	 };
	 polhtml = polhtml + "</ul>";
    };
  $("#policies").empty();
  $("#policies").html("<h4><b>Policies that match your selection</b></h4>");
  $(polhtml).appendTo('#policies');
})
.header("Content-Type","application/json")
.send("POST",senddata);
};

d3.json(contentsurl, function(cdata) {
    var conthtml = '<h4><b>Select your Community</b></h4><div class="tab-pane active" id="godiscipline" style="float:right"><a class="btn btn-primary btnNext">Next</a></div><br /><br />';
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
		topichtml = topichtml + '<p>&nbsp;&nbsp;<b>' + k_data + '</b></p>';
	    };
            topichtml = topichtml + '<p><input name="disc" type="checkbox" value="discipline:' + k + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p>';
	    known[k_data] = k;
        }
    }
    conthtml = conthtml + "</ul>";
    topichtml = topichtml + '</ul>';
    conthtml = topichtml + conthtml;
    $("#communityload").empty();
    $('#communityload').html(conthtml);

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
